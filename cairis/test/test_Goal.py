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
    call([os.environ['CAIRIS_CFG_DIR'] + "/initdb.sh"])
    cairis.core.BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/goals.json')
    d = json.load(f)
    f.close()
    ienvs = d['environments']
    iep1 = EnvironmentParameters(ienvs[0]["theName"],ienvs[0]["theShortCode"],ienvs[0]["theDescription"])
    iep2 = EnvironmentParameters(ienvs[1]["theName"],ienvs[1]["theShortCode"],ienvs[1]["theDescription"])
    b = Borg()
    b.dbProxy.addEnvironment(iep1)
    b.dbProxy.addEnvironment(iep2)
    iassets = d['assets']
    iaeps1 = AssetEnvironmentProperties(iassets[0]["theEnvironmentProperties"][0][0],iassets[0]["theEnvironmentProperties"][0][1],iassets[0]["theEnvironmentProperties"][0][2])
    iaeps2 = AssetEnvironmentProperties(iassets[0]["theEnvironmentProperties"][1][0],iassets[0]["theEnvironmentProperties"][1][1],iassets[0]["theEnvironmentProperties"][1][2])
    iap1 = AssetParameters(iassets[0]["theName"],iassets[0]["theShortCode"],iassets[0]["theDescription"],iassets[0]["theSignificance"],iassets[0]["theType"],"0","N/A",[],[],[iaeps1,iaeps2])
    b.dbProxy.addAsset(iap1)
    iaeps1 = AssetEnvironmentProperties(iassets[1]["theEnvironmentProperties"][0][0],iassets[1]["theEnvironmentProperties"][0][1],iassets[1]["theEnvironmentProperties"][0][2])
    iaeps2 = AssetEnvironmentProperties(iassets[1]["theEnvironmentProperties"][1][0],iassets[1]["theEnvironmentProperties"][1][1],iassets[1]["theEnvironmentProperties"][1][2])
    iap2 = AssetParameters(iassets[1]["theName"],iassets[1]["theShortCode"],iassets[1]["theDescription"],iassets[1]["theSignificance"],iassets[1]["theType"],"0","N/A",[],[],[iaeps1,iaeps2])
    b.dbProxy.addAsset(iap2)
    self.iGoals = d['goals']

  def testGoal(self):
    b = Borg()
    igep1d = GoalEnvironmentProperties(self.iGoals[0]["theEnvironmentProperties"][0]["theName"],self.iGoals[0]["theEnvironmentProperties"][0]["theLabel"],self.iGoals[0]["theEnvironmentProperties"][0]["theDefinition"],self.iGoals[0]["theEnvironmentProperties"][0]["theCategory"],self.iGoals[0]["theEnvironmentProperties"][0]["thePriority"],self.iGoals[0]["theEnvironmentProperties"][0]["theFitCriterion"],self.iGoals[0]["theEnvironmentProperties"][0]["theIssue"],[],[],self.iGoals[0]["theEnvironmentProperties"][0]["theConcerns"],[],self.iGoals[0]["theEnvironmentProperties"][0]["thePolicy"])
    igep1n = GoalEnvironmentProperties(self.iGoals[0]["theEnvironmentProperties"][1]["theName"],self.iGoals[0]["theEnvironmentProperties"][1]["theLabel"],self.iGoals[0]["theEnvironmentProperties"][1]["theDefinition"],self.iGoals[0]["theEnvironmentProperties"][1]["theCategory"],self.iGoals[0]["theEnvironmentProperties"][1]["thePriority"],self.iGoals[0]["theEnvironmentProperties"][1]["theFitCriterion"],self.iGoals[0]["theEnvironmentProperties"][1]["theIssue"],[],[],self.iGoals[0]["theEnvironmentProperties"][1]["theConcerns"],[],self.iGoals[0]["theEnvironmentProperties"][0]["thePolicy"])

    igep2d = GoalEnvironmentProperties(self.iGoals[1]["theEnvironmentProperties"][0]["theName"],self.iGoals[1]["theEnvironmentProperties"][0]["theLabel"],self.iGoals[1]["theEnvironmentProperties"][0]["theDefinition"],self.iGoals[1]["theEnvironmentProperties"][0]["theCategory"],self.iGoals[1]["theEnvironmentProperties"][0]["thePriority"],self.iGoals[1]["theEnvironmentProperties"][0]["theFitCriterion"],self.iGoals[1]["theEnvironmentProperties"][0]["theIssue"],[],[],self.iGoals[1]["theEnvironmentProperties"][0]["theConcerns"],[])
    igep2n = GoalEnvironmentProperties(self.iGoals[1]["theEnvironmentProperties"][1]["theName"],self.iGoals[1]["theEnvironmentProperties"][1]["theLabel"],self.iGoals[1]["theEnvironmentProperties"][1]["theDefinition"],self.iGoals[1]["theEnvironmentProperties"][1]["theCategory"],self.iGoals[1]["theEnvironmentProperties"][1]["thePriority"],self.iGoals[1]["theEnvironmentProperties"][1]["theFitCriterion"],self.iGoals[1]["theEnvironmentProperties"][1]["theIssue"],[],[],self.iGoals[1]["theEnvironmentProperties"][1]["theConcerns"],[])

    igep3d = GoalEnvironmentProperties(self.iGoals[2]["theEnvironmentProperties"][0]["theName"],self.iGoals[2]["theEnvironmentProperties"][0]["theLabel"],self.iGoals[2]["theEnvironmentProperties"][0]["theDefinition"],self.iGoals[2]["theEnvironmentProperties"][0]["theCategory"],self.iGoals[2]["theEnvironmentProperties"][0]["thePriority"],self.iGoals[2]["theEnvironmentProperties"][0]["theFitCriterion"],self.iGoals[2]["theEnvironmentProperties"][0]["theIssue"],[],[],self.iGoals[2]["theEnvironmentProperties"][0]["theConcerns"],[])
    igep3n = GoalEnvironmentProperties(self.iGoals[2]["theEnvironmentProperties"][1]["theName"],self.iGoals[2]["theEnvironmentProperties"][1]["theLabel"],self.iGoals[2]["theEnvironmentProperties"][1]["theDefinition"],self.iGoals[2]["theEnvironmentProperties"][1]["theCategory"],self.iGoals[2]["theEnvironmentProperties"][1]["thePriority"],self.iGoals[2]["theEnvironmentProperties"][1]["theFitCriterion"],self.iGoals[2]["theEnvironmentProperties"][1]["theIssue"],[],[],self.iGoals[2]["theEnvironmentProperties"][1]["theConcerns"],[])
    igp1 = GoalParameters(self.iGoals[0]["theName"],self.iGoals[0]["theOriginator"],[],[igep1d,igep1n])
    igp2 = GoalParameters(self.iGoals[1]["theName"],self.iGoals[1]["theOriginator"],[],[igep2d,igep2n])
    igp3 = GoalParameters(self.iGoals[2]["theName"],self.iGoals[2]["theOriginator"],[],[igep3d,igep2n])
    b.dbProxy.addGoal(igp1)
    b.dbProxy.addGoal(igp2)
    b.dbProxy.addGoal(igp3)
    b.dbProxy.relabelGoals(igep1d.name())
    oGoals = b.dbProxy.getGoals()
    og1 = oGoals[self.iGoals[0]["theName"]]
    og2 = oGoals[self.iGoals[1]["theName"]]
    og3 = oGoals[self.iGoals[2]["theName"]]
    self.assertEqual(igp1.name(), og1.name())
    self.assertEqual(igp1.originator(), og1.originator())
    ogep1 = og1.environmentProperty(igep1d.name())
    ogep2 = og2.environmentProperty(igep1d.name())
    self.assertEqual(og1.refinements('Day'),False)

    self.assertEqual(igep1d.label(), ogep1.label())
    self.assertEqual(igep1d.definition(), ogep1.definition())
    self.assertEqual(igep1d.definition() + ' [Day].  ' + igep1d.definition() + ' [Night].  ', og1.definition('','Maximise'))
    self.assertEqual(igep1d.category(), ogep1.category())
    self.assertEqual(igep1d.category() + ' [Day].  ' + igep1d.category() + ' [Night].  ', og1.category('','Maximise'))
    self.assertEqual(igep1d.priority(), ogep1.priority())
    self.assertEqual(igep1d.priority() + ' [Day].  ' + igep1d.priority() + ' [Night].  ', og1.priority('','Maximise'))
    self.assertEqual(igep1d.fitCriterion(), ogep1.fitCriterion())
    self.assertEqual(igep1d.fitCriterion() + ' [Day].  ' + igep1d.fitCriterion() + ' [Night].  ', og1.fitCriterion('','Maximise'))
    self.assertEqual(igep1d.issue(), ogep1.issue())
    self.assertEqual(igep1d.issue() + ' [Day].  ' + igep1d.issue() + ' [Night].  ', og1.issue('','Maximise'))
    self.assertEqual(igep1d.goalRefinements(), ogep1.goalRefinements())
    self.assertEqual(igep1d.subGoalRefinements(), ogep1.subGoalRefinements())
    self.assertEqual(igep1d.concerns(), ogep1.concerns())
    self.assertEqual(igep1d.concernAssociations(), ogep1.concernAssociations())
    self.assertEqual(igep1d.policy(), ogep1.policy())

    envName = self.iGoals[0]["theEnvironmentProperties"][0]['theName']
    self.assertEqual(igep1d.label(), og1.label(envName))
    self.assertEqual(igep1d.definition(), og1.definition(envName,''))
    self.assertEqual(igep1d.category(), og1.category(envName,''))
    self.assertEqual(igep1d.priority(), og1.priority(envName,''))
    self.assertEqual(igep1d.fitCriterion(), og1.fitCriterion(envName,''))
    self.assertEqual(igep1d.issue(), og1.issue(envName,''))

    self.assertEqual(igep2d.label(), ogep2.label())
    self.assertEqual(igep2d.definition(), ogep2.definition())
    self.assertEqual(igep2d.category(), ogep2.category())
    self.assertEqual(igep2d.priority(), ogep2.priority())
    self.assertEqual(igep2d.fitCriterion(), ogep2.fitCriterion())
    self.assertEqual(igep2d.issue(), ogep2.issue())
    self.assertEqual(igep2d.goalRefinements(), ogep2.goalRefinements())
    self.assertEqual(igep2d.subGoalRefinements(), ogep2.subGoalRefinements())
    self.assertEqual(igep2d.concerns(), ogep2.concerns())
    self.assertEqual(igep2d.concernAssociations(), ogep2.concernAssociations())



    igop1 = GoalAssociationParameters(igep1d.name(),igp1.name(),'goal','and',igp2.name(),'goal',0,'None')
    igop2 = GoalAssociationParameters(igep1d.name(),igp1.name(),'goal','and',igp3.name(),'goal',0,'None')

    b.dbProxy.addGoalAssociation(igop1)
    b.dbProxy.addGoalAssociation(igop2)

    ogops = b.dbProxy.getGoalAssociations()
    ogop1 = ogops[igep1d.name() + '/' + igp1.name() + '/' + igp2.name() + '/and']
    ogop2 = ogops[igep2d.name() + '/' + igp1.name() + '/' + igp3.name() + '/and']

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
    pass


if __name__ == '__main__':
  unittest.main()
