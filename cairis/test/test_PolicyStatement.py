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
from cairis.core.PolicyStatement import PolicyStatement
from cairis.core.ARM import DatabaseProxyException

__author__ = 'Shamal Faily'


class PolicyStatementTest(unittest.TestCase):

  def setUp(self):
    call([os.environ['CAIRIS_CFG_DIR'] + "/initdb.sh"])
    cairis.core.BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/policy_statements.json')
    d = json.load(f)
    f.close()
    ienvs = d['environments']
    iep1 = EnvironmentParameters(ienvs[0]["theName"],ienvs[0]["theShortCode"],ienvs[0]["theDescription"])
    b = Borg()
    b.dbProxy.addEnvironment(iep1)
    iassets = d['assets']
    iaeps1 = AssetEnvironmentProperties(iassets[0]["theEnvironmentProperties"][0][0],iassets[0]["theEnvironmentProperties"][0][1],iassets[0]["theEnvironmentProperties"][0][2])
    iap1 = AssetParameters(iassets[0]["theName"],iassets[0]["theShortCode"],iassets[0]["theDescription"],iassets[0]["theSignificance"],iassets[0]["theType"],"0","N/A",[],[],[iaeps1])
    b.dbProxy.addAsset(iap1)
    iaeps1 = AssetEnvironmentProperties(iassets[1]["theEnvironmentProperties"][0][0],iassets[1]["theEnvironmentProperties"][0][1],iassets[1]["theEnvironmentProperties"][0][2])
    iap2 = AssetParameters(iassets[1]["theName"],iassets[1]["theShortCode"],iassets[1]["theDescription"],iassets[1]["theSignificance"],iassets[1]["theType"],"0","N/A",[],[],[iaeps1])
    b.dbProxy.addAsset(iap2)
    self.iGoals = d['goals']

    igep1d = GoalEnvironmentProperties(self.iGoals[0]["theEnvironmentProperties"][0]["theName"],self.iGoals[0]["theEnvironmentProperties"][0]["theLabel"],self.iGoals[0]["theEnvironmentProperties"][0]["theDefinition"],self.iGoals[0]["theEnvironmentProperties"][0]["theCategory"],self.iGoals[0]["theEnvironmentProperties"][0]["thePriority"],self.iGoals[0]["theEnvironmentProperties"][0]["theFitCriterion"],self.iGoals[0]["theEnvironmentProperties"][0]["theIssue"],[],[],self.iGoals[0]["theEnvironmentProperties"][0]["theConcerns"],[])
    igp1 = GoalParameters(self.iGoals[0]["theName"],self.iGoals[0]["theOriginator"],[],[igep1d])
    b.dbProxy.addGoal(igp1)
    self.iPs = d['policy_statements']

  def testPolicyStatement(self):
    b = Borg()
  
    ip = PolicyStatement(-1,self.iPs[0]['theGoalName'],self.iPs[0]['theEnvironmentName'],self.iPs[0]['theSubject'],self.iPs[0]['theAccessType'],self.iPs[0]['theResource'],self.iPs[0]['thePermission'])
    b.dbProxy.addPolicyStatement(ip)

    ops = b.dbProxy.getPolicyStatements()
    op = ops[0]
    self.assertEqual(ip.goal(), op.goal())
    self.assertEqual(ip.environment(), op.environment())
    self.assertEqual(ip.subject(), op.subject())
    self.assertEqual(ip.accessType(), op.accessType())
    self.assertEqual(ip.resource(), op.resource())
    self.assertEqual(ip.permission(), op.permission())

    ip.theId = op.id()
    ip.thePermission = 'deny'
    b.dbProxy.updatePolicyStatement(ip)

    ops = b.dbProxy.getPolicyStatements()
    op = ops[0]
    self.assertEqual(ip.goal(), op.goal())
    self.assertEqual(ip.environment(), op.environment())
    self.assertEqual(ip.subject(), op.subject())
    self.assertEqual(ip.accessType(), op.accessType())
    self.assertEqual(ip.resource(), op.resource())
    self.assertEqual(ip.permission(), op.permission())

    b.dbProxy.deletePolicyStatement(op.id())

    
  def tearDown(self):
    pass


if __name__ == '__main__':
  unittest.main()
