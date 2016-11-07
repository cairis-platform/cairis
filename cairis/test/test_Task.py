#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

__author__ = 'Shamal Faily'


import unittest
import os
import json
from subprocess import call
import cairis.core.BorgFactory
from cairis.core.Borg import Borg
from cairis.core.RoleParameters import RoleParameters
from cairis.core.EnvironmentParameters import EnvironmentParameters
from cairis.core.AssetEnvironmentProperties import AssetEnvironmentProperties
from cairis.core.AssetParameters import AssetParameters
from cairis.core.PersonaEnvironmentProperties import PersonaEnvironmentProperties
from cairis.core.PersonaParameters import PersonaParameters
from cairis.core.TaskEnvironmentProperties import TaskEnvironmentProperties
from cairis.core.TaskParameters import TaskParameters

class TaskTest(unittest.TestCase):

  def setUp(self):
    call([os.environ['CAIRIS_SRC'] + "/test/initdb.sh"])
    cairis.core.BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/tasks.json')
    d = json.load(f)
    f.close()
    self.iEnvironments = d['environments']
    iep1 = EnvironmentParameters(self.iEnvironments[0]["theName"],self.iEnvironments[0]["theShortCode"],self.iEnvironments[0]["theDescription"])
    b = Borg()
    b.dbProxy.addEnvironment(iep1)
    self.theEnvironments = b.dbProxy.getEnvironments()

    self.iRoles = d['roles']
    irp = RoleParameters(self.iRoles[0]["theName"], self.iRoles[0]["theType"], self.iRoles[0]["theShortCode"], self.iRoles[0]["theDescription"],[])
    b.dbProxy.addRole(irp)
    self.theRoles = b.dbProxy.getRoles()
    self.iPersonas = d['personas']
    ipp = PersonaParameters(self.iPersonas[0]["theName"],self.iPersonas[0]["theActivities"],self.iPersonas[0]["theAttitudes"],self.iPersonas[0]["theAptitudes"],self.iPersonas[0]["theMotivations"],self.iPersonas[0]["theSkills"],self.iPersonas[0]["theIntrinsic"],self.iPersonas[0]["theContextual"],"","0",self.iPersonas[0]["thePersonaType"],[],[PersonaEnvironmentProperties(self.iPersonas[0]["theEnvironmentProperties"][0]["theName"],(self.iPersonas[0]["theEnvironmentProperties"][0]["theDirectFlag"] == "True"),self.iPersonas[0]["theEnvironmentProperties"][0]["theNarrative"],self.iPersonas[0]["theEnvironmentProperties"][0]["theRole"])],[])
    b.dbProxy.addPersona(ipp) 
    self.thePersonas = b.dbProxy.getPersonas()
    
    self.iAssets = d['assets']
    iaeps = [AssetEnvironmentProperties(self.iAssets[0]["theEnvironmentProperties"][0][0],self.iAssets[0]["theEnvironmentProperties"][0][1],self.iAssets[0]["theEnvironmentProperties"][0][2])]
    iap = AssetParameters(self.iAssets[0]["theName"],self.iAssets[0]["theShortCode"],self.iAssets[0]["theDescription"],self.iAssets[0]["theSignificance"],self.iAssets[0]["theType"],"0","N/A",[],[],iaeps)
    b = Borg()
    b.dbProxy.addAsset(iap)
    self.theAssets = b.dbProxy.getAssets()

    self.iTasks = d['tasks']

  def testTask(self):
    t = self.iTasks[0]
    taskName = t["theName"]
    taskTags = t["theTaskTags"]
    taskShortCode = t["theShortCode"]
    taskObjective = t["theObjective"]
    taskAuthor = t["theAuthor"]
    isAssumptionTask = int(t["isAssumption"])
    tEnv = t["theEnvironments"][0]
    envName = tEnv["theName"]
    deps = tEnv["theDependencies"]
    taskPersona = tEnv["theTaskPersonas"][0]["thePersona"]
    taskDuration = tEnv["theTaskPersonas"][0]["theDuration"]
    taskFreq = tEnv["theTaskPersonas"][0]["theFrequency"]
    taskDemands = tEnv["theTaskPersonas"][0]["theDemands"]
    taskGoalConflict = tEnv["theTaskPersonas"][0]["theGoalConflict"]
    taskAssets = tEnv["theTaskAssets"]
    taskConcerns = []
    taskNarrative = tEnv["theNarrative"]
    taskConsequences = tEnv["theConsequences"]
    taskBenefits = tEnv["theBenefits"]
    iteps = [TaskEnvironmentProperties(envName,deps,[(taskPersona,taskDuration,taskFreq,taskDemands,taskGoalConflict)],taskAssets,taskConcerns,taskNarrative,taskConsequences,taskBenefits)]
    iTask = TaskParameters(taskName,taskShortCode,taskObjective,isAssumptionTask,taskAuthor,taskTags,iteps)
    b = Borg()
    b.dbProxy.addTask(iTask)
    theTasks = b.dbProxy.getTasks()
    oTask = theTasks[self.iTasks[0]["theName"]] 

    self.assertEqual(iTask.name(),oTask.name())
    self.assertEqual(iTask.tags(),oTask.tags())
    self.assertEqual(iTask.shortCode(),oTask.shortCode())
    self.assertEqual(iTask.objective(),oTask.objective())
    self.assertEqual(iTask.assumption(),oTask.assumption())
    self.assertEqual(iTask.author(),oTask.author())
    self.assertEqual(iTask.environmentProperties()[0].personas(),oTask.personas(envName,'',envName))
    self.assertEqual(iTask.environmentProperties()[0].assets(),oTask.assets(envName,''))
    self.assertEqual(iTask.environmentProperties()[0].narrative(),oTask.narrative(envName,''))
    self.assertEqual(iTask.environmentProperties()[0].consequences(),oTask.environmentProperties()[0].consequences())
    self.assertEqual(iTask.environmentProperties()[0].benefits(),oTask.environmentProperties()[0].benefits())
    self.assertEqual(iTask.environmentProperties()[0].dependencies(),oTask.environmentProperties()[0].dependencies())
    self.assertEqual(oTask.usability(envName,''),5)

    self.assertEqual(b.dbProxy.taskLoad(oTask.id(),104),5)

    iTask.theName = 'Updated name'
    iTask.setId(oTask.id())
    b.dbProxy.updateTask(iTask)
    theTasks = b.dbProxy.getTasks()
    oTask = theTasks['Updated name'] 
    self.assertEqual(oTask.name(),'Updated name')
    self.assertEqual(iTask.tags(),oTask.tags())
    self.assertEqual(iTask.shortCode(),oTask.shortCode())
    self.assertEqual(iTask.objective(),oTask.objective())
    self.assertEqual(iTask.assumption(),oTask.assumption())
    self.assertEqual(iTask.author(),oTask.author())
    self.assertEqual(iTask.environmentProperties()[0].personas(),oTask.environmentProperties()[0].personas())
    self.assertEqual(iTask.environmentProperties()[0].assets(),oTask.environmentProperties()[0].assets())
    self.assertEqual(iTask.environmentProperties()[0].narrative(),oTask.environmentProperties()[0].narrative())
    self.assertEqual(iTask.environmentProperties()[0].consequences(),oTask.environmentProperties()[0].consequences())
    self.assertEqual(iTask.environmentProperties()[0].benefits(),oTask.environmentProperties()[0].benefits())
    self.assertEqual(iTask.environmentProperties()[0].dependencies(),oTask.environmentProperties()[0].dependencies())

    b.dbProxy.deleteTask(oTask.id())

  def tearDown(self):
    b = Borg()
    b.dbProxy.deleteAsset(self.theAssets[self.iAssets[0]["theName"]].id())
    b.dbProxy.deletePersona(self.thePersonas[self.iPersonas[0]["theName"]].id())
    b.dbProxy.deleteRole(self.theRoles[self.iRoles[0]["theName"]].id())
    b.dbProxy.deleteEnvironment(self.theEnvironments[self.iEnvironments[0]["theName"]].id())
    b.dbProxy.close()
    call([os.environ['CAIRIS_SRC'] + "/test/dropdb.sh"])

if __name__ == '__main__':
  unittest.main()
