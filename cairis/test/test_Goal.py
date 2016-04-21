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
from cairis.core.GoalEnvironmentProperties import GoalEnvironmentProperties
from cairis.core.ARM import DatabaseProxyException

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
    igp1 = GoalParameters(self.iGoals[0]["theName"],self.iGoals[0]["theOriginator"],[],[igep1])
    b.dbProxy.addGoal(igp1)
    oGoals = b.dbProxy.getGoals()
    og = oGoals[self.iGoals[0]["theName"]]
    self.assertEqual(igp1.name(), og.name())
    self.assertEqual(igp1.originator(), og.originator())

    b.dbProxy.deleteGoal(og.id())
  
  def tearDown(self):
    b = Borg()
    
    b.dbProxy.deleteAsset(self.oap[self.iap1.name()].id())
    b.dbProxy.deleteEnvironment(self.oenvs[self.iep1.name()].id())
    b.dbProxy.close()
    call([os.environ['CAIRIS_SRC'] + "/test/dropdb.sh"])


if __name__ == '__main__':
  unittest.main()
