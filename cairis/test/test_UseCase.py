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

import unittest
import os
import json
from subprocess import call
import cairis.core.BorgFactory
from cairis.core.Borg import Borg
from cairis.core.RoleParameters import RoleParameters
from cairis.core.EnvironmentParameters import EnvironmentParameters
from cairis.core.Step import Step
from cairis.core.Steps import Steps
from cairis.core.UseCaseEnvironmentProperties import UseCaseEnvironmentProperties
from cairis.core.UseCaseParameters import UseCaseParameters

class UseCaseTest(unittest.TestCase):

  def setUp(self):
    call([os.environ['CAIRIS_SRC'] + "/test/initdb.sh"])
    cairis.core.BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/usecases.json')
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

    self.iUseCases = d['use_cases']
    

  def testUseCase(self):
    ucName = self.iUseCases[0]["theName"]
    ucAuthor = self.iUseCases[0]["theAuthor"]
    ucCode = self.iUseCases[0]["theCode"]
    ucDesc = self.iUseCases[0]["theDescription"]
    ucActor = self.iUseCases[0]["theActor"]
    ucEnv = self.iUseCases[0]["theEnvironments"][0]
    ucEnvName = ucEnv["theName"]
    ucPre = ucEnv["thePreconditions"]
    ucPost = ucEnv["thePostconditions"]
    ss = Steps()
    for ucStep in ucEnv["theFlow"]:
      ss.append(Step(ucStep["theDescription"]))  
    ucep = UseCaseEnvironmentProperties(ucEnvName,ucPre,ss,ucPost)
    iuc = UseCaseParameters(ucName,ucAuthor,ucCode,[ucActor],ucDesc,[],[ucep])
    b = Borg()
    b.dbProxy.addUseCase(iuc) 

    theUseCases = b.dbProxy.getUseCases()
    ouc = theUseCases[self.iUseCases[0]["theName"]]
    self.assertEqual(iuc.name(),ouc.name())
    self.assertEqual(iuc.tags(),ouc.tags())
    self.assertEqual(iuc.author(),ouc.author())
    self.assertEqual(iuc.code(),ouc.code())
    self.assertEqual(iuc.actors(),ouc.actors())
    self.assertEqual(iuc.description(),ouc.description())
    self.assertEqual(iuc.author(),ouc.author())
    self.assertEqual(iuc.environmentProperties()[0].preconditions(),ouc.environmentProperties()[0].preconditions())
    self.assertEqual(iuc.environmentProperties()[0].postconditions(),ouc.environmentProperties()[0].postconditions())

    iuc.theName = 'Updated name'
    iuc.setId(ouc.id())
    b.dbProxy.updateUseCase(iuc) 
    theUseCases = b.dbProxy.getUseCases()
    ouc = theUseCases['Updated name']
    self.assertEqual(iuc.name(),ouc.name())
    self.assertEqual(iuc.tags(),ouc.tags())
    self.assertEqual(iuc.author(),ouc.author())
    self.assertEqual(iuc.code(),ouc.code())
    self.assertEqual(iuc.actors(),ouc.actors())
    self.assertEqual(iuc.description(),ouc.description())
    self.assertEqual(iuc.author(),ouc.author())
    self.assertEqual(iuc.environmentProperties()[0].preconditions(),ouc.environmentProperties()[0].preconditions())
    self.assertEqual(iuc.environmentProperties()[0].postconditions(),ouc.environmentProperties()[0].postconditions())

    b.dbProxy.deleteUseCase(ouc.id())

  def tearDown(self):
    b = Borg()
    b.dbProxy.deleteRole(self.theRoles[self.iRoles[0]["theName"]].id())
    b.dbProxy.deleteEnvironment(self.theEnvironments[self.iEnvironments[0]["theName"]].id())
    b.dbProxy.close()
    call([os.environ['CAIRIS_SRC'] + "/test/dropdb.sh"])

if __name__ == '__main__':
  unittest.main()
