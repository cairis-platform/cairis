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
from cairis.core.EnvironmentParameters import EnvironmentParameters
from cairis.core.AssetParameters import AssetParameters
from cairis.core.AssetEnvironmentProperties import AssetEnvironmentProperties
from cairis.core.GoalParameters import GoalParameters
from cairis.core.GoalAssociationParameters import GoalAssociationParameters
from cairis.core.GoalEnvironmentProperties import GoalEnvironmentProperties
from cairis.core.ARM import DatabaseProxyException

__author__ = 'Shamal Faily'


class GoalTest(unittest.TestCase):

  def setUp(self):
    call([os.environ['CAIRIS_SRC'] + "/test/initdb.sh"])
    cairis.core.BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/goals.json')
    d = json.load(f)
    f.close()
    self.ienvs = d['environments']
    self.iep1 = EnvironmentParameters(self.ienvs[0]["theName"],self.ienvs[0]["theShortCode"],self.ienvs[0]["theDescription"])
    b = Borg()
    b.dbProxy.addEnvironment(self.iep1)
    self.oenvs = b.dbProxy.getEnvironments()

    self.iassets = d['assets']
    self.iaeps1 = [AssetEnvironmentProperties(self.iassets[0]["theEnvironmentProperties"][0][0],self.iassets[0]["theEnvironmentProperties"][0][1],self.iassets[0]["theEnvironmentProperties"][0][2])]
    self.iap1 = AssetParameters(self.iassets[0]["theName"],self.iassets[0]["theShortCode"],self.iassets[0]["theDescription"],self.iassets[0]["theSignificance"],self.iassets[0]["theType"],"0","N/A",[],[],self.iaeps1)
    b.dbProxy.addAsset(self.iap1)
    self.oap = b.dbProxy.getAssets()

    self.iGoals = d['goals']

  def testGoal(self):
    b = Borg()
    igep1 = GoalEnvironmentProperties(self.iGoals[0]["theEnvironmentProperties"][0],self.iGoals[0]["theEnvironmentProperties"][1],self.iGoals[0]["theEnvironmentProperties"][2],self.iGoals[0]["theEnvironmentProperties"][3],self.iGoals[0]["theEnvironmentProperties"][4],self.iGoals[0]["theEnvironmentProperties"][5],self.iGoals[0]["theEnvironmentProperties"][6],[],[],[self.iGoals[0]["theEnvironmentProperties"][7]],[])
    igep2 = GoalEnvironmentProperties(self.iGoals[1]["theEnvironmentProperties"][0],self.iGoals[1]["theEnvironmentProperties"][1],self.iGoals[1]["theEnvironmentProperties"][2],self.iGoals[1]["theEnvironmentProperties"][3],self.iGoals[1]["theEnvironmentProperties"][4],self.iGoals[1]["theEnvironmentProperties"][5],self.iGoals[1]["theEnvironmentProperties"][6],[],[],[self.iGoals[1]["theEnvironmentProperties"][7]],[])
    igep3 = GoalEnvironmentProperties(self.iGoals[2]["theEnvironmentProperties"][0],self.iGoals[2]["theEnvironmentProperties"][1],self.iGoals[2]["theEnvironmentProperties"][2],self.iGoals[2]["theEnvironmentProperties"][3],self.iGoals[2]["theEnvironmentProperties"][4],self.iGoals[2]["theEnvironmentProperties"][5],self.iGoals[2]["theEnvironmentProperties"][6],[],[],[self.iGoals[2]["theEnvironmentProperties"][7]],[])

    igp1 = GoalParameters(self.iGoals[0]["theName"],self.iGoals[0]["theOriginator"],[],[igep1])
    igp2 = GoalParameters(self.iGoals[1]["theName"],self.iGoals[1]["theOriginator"],[],[igep2])
    igp3 = GoalParameters(self.iGoals[2]["theName"],self.iGoals[2]["theOriginator"],[],[igep3])
    b.dbProxy.addGoal(igp1)
    b.dbProxy.addGoal(igp2)
    b.dbProxy.addGoal(igp3)
    b.dbProxy.relabelGoals(igep1.name())
    oGoals = b.dbProxy.getGoals()
    og1 = oGoals[self.iGoals[0]["theName"]]
    og2 = oGoals[self.iGoals[1]["theName"]]
    og3 = oGoals[self.iGoals[2]["theName"]]
    self.assertEqual(igp1.name(), og1.name())
    self.assertEqual(igp1.originator(), og1.originator())
    ogep1 = og1.environmentProperty(igep1.name())
    ogep2 = og2.environmentProperty(igep1.name())

    self.assertEqual(igep1.label(), ogep1.label())
    self.assertEqual(igep1.definition(), ogep1.definition())
    self.assertEqual(igep1.category(), ogep1.category())
    self.assertEqual(igep1.priority(), ogep1.priority())
    self.assertEqual(igep1.fitCriterion(), ogep1.fitCriterion())
    self.assertEqual(igep1.issue(), ogep1.issue())
    self.assertEqual(igep1.goalRefinements(), ogep1.goalRefinements())
    self.assertEqual(igep1.subGoalRefinements(), ogep1.subGoalRefinements())
    self.assertEqual(igep1.concerns(), ogep1.concerns())
    self.assertEqual(igep1.concernAssociations(), ogep1.concernAssociations())

    envName = self.iGoals[0]["theEnvironmentProperties"][0]
    self.assertEqual(igep1.label(), og1.label(envName))
    self.assertEqual(igep1.definition(), og1.definition(envName,''))
    self.assertEqual(igep1.category(), og1.category(envName,''))
    self.assertEqual(igep1.priority(), og1.priority(envName,''))
    self.assertEqual(igep1.fitCriterion(), og1.fitCriterion(envName,''))
    self.assertEqual(igep1.issue(), og1.issue(envName,''))

    self.assertEqual(igep2.label(), ogep2.label())
    self.assertEqual(igep2.definition(), ogep2.definition())
    self.assertEqual(igep2.category(), ogep2.category())
    self.assertEqual(igep2.priority(), ogep2.priority())
    self.assertEqual(igep2.fitCriterion(), ogep2.fitCriterion())
    self.assertEqual(igep2.issue(), ogep2.issue())
    self.assertEqual(igep2.goalRefinements(), ogep2.goalRefinements())
    self.assertEqual(igep2.subGoalRefinements(), ogep2.subGoalRefinements())
    self.assertEqual(igep2.concerns(), ogep2.concerns())
    self.assertEqual(igep2.concernAssociations(), ogep2.concernAssociations())



    igop1 = GoalAssociationParameters(igep1.name(),igp1.name(),'goal','and',igp2.name(),'goal',0,'None')
    igop2 = GoalAssociationParameters(igep1.name(),igp1.name(),'goal','and',igp3.name(),'goal',0,'None')

    b.dbProxy.addGoalAssociation(igop1)
    b.dbProxy.addGoalAssociation(igop2)

    ogops = b.dbProxy.getGoalAssociations()
    ogop1 = ogops[igep1.name() + '/' + igp1.name() + '/' + igp2.name() + '/and']
    ogop2 = ogops[igep2.name() + '/' + igp1.name() + '/' + igp3.name() + '/and']

    self.assertEqual(igop1.environment(), ogop1.environment())
    self.assertEqual(igop1.goal(), ogop1.goal())
    self.assertEqual(igop1.goalDimension(), ogop1.goalDimension())
    self.assertEqual(igop1.type(), ogop1.type())
    self.assertEqual(igop1.subGoal(), ogop1.subGoal())
    self.assertEqual(igop1.subGoalDimension(), ogop1.subGoalDimension())
    self.assertEqual(igop1.alternative(), ogop1.alternative())
    self.assertEqual(igop1.rationale(), ogop1.rationale())

    self.assertEqual(igop2.environment(), ogop2.environment())
    self.assertEqual(igop2.goal(), ogop2.goal())
    self.assertEqual(igop2.goalDimension(), ogop2.goalDimension())
    self.assertEqual(igop2.type(), ogop2.type())
    self.assertEqual(igop2.subGoal(), ogop2.subGoal())
    self.assertEqual(igop2.subGoalDimension(), ogop2.subGoalDimension())
    self.assertEqual(igop2.alternative(), ogop2.alternative())
    self.assertEqual(igop2.rationale(), ogop2.rationale())

    b.dbProxy.deleteGoalAssociation(ogop1.id(),ogop1.goal(),ogop1.subGoal())
    b.dbProxy.deleteGoalAssociation(ogop2.id(),ogop2.goal(),ogop2.subGoal())

    b.dbProxy.deleteGoal(og1.id())
    b.dbProxy.deleteGoal(og2.id())
    b.dbProxy.deleteGoal(og3.id())
  
  def tearDown(self):
    b = Borg()
    
    b.dbProxy.deleteAsset(self.oap[self.iap1.name()].id())
    b.dbProxy.deleteEnvironment(self.oenvs[self.iep1.name()].id())
    b.dbProxy.close()
    call([os.environ['CAIRIS_SRC'] + "/test/dropdb.sh"])


if __name__ == '__main__':
  unittest.main()
