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
import BorgFactory
from Borg import Borg
from EnvironmentParameters import EnvironmentParameters
from AttackerParameters import AttackerParameters
from AttackerEnvironmentProperties import AttackerEnvironmentProperties

class AttackerTest(unittest.TestCase):

  def setUp(self):
    BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/attackers.json')
    d = json.load(f)
    f.close()
    ienvs = d['environments']
    self.iep = EnvironmentParameters(ienvs[0]["theName"],ienvs[0]["theShortCode"],ienvs[0]["theDescription"])
    b = Borg()
    b.dbProxy.addEnvironment(self.iep)
    self.oenvs = b.dbProxy.getEnvironments()
    self.iAttackers = d['attackers']
    
  def testAttacker(self):
    iatkeps = AttackerEnvironmentProperties(self.iAttackers[0]["theEnvironmentProperties"][0]["theName"],self.iAttackers[0]["theEnvironmentProperties"][0]["theRole"],self.iAttackers[0]["theEnvironmentProperties"][0]["theMotives"],self.iAttackers[0]["theEnvironmentProperties"][0]["theCapabilities"])
    iatk = AttackerParameters(self.iAttackers[0]["theName"], self.iAttackers[0]["theDescription"], self.iAttackers[0]["theImage"],[],ieatk)
    b = Borg()
    b.dbProxy.addAttacker(iatk)
    oAttackers = b.dbProxy.getAttacker()
    o = oAttackers[0]
    self.assertEqual(iatk.name(), o.name())
    self.assertEqual(iatk.description(),o.description())
    self.assertEqual(iatk.type(),o.image())
    oatkeps = o.environmentProperties()
    self.assertEqual(iatkeps[0].name(), oatkeps[0].name())
    self.assertEqual(iatkeps[0].roles(), oatkeps[0].roles())
    self.assertEqual(str(iatkeps[0].motives()[1]), str(oatkeps[0].motives()[0]))
    self.assertEqual(str(iatkeps[0].capabilities()[0]), str(oatkeps[0].capabilities()[0]))
    self.assertEqual(str(iatkeps[0].capabilities()[1]), str(oatkeps[0].capabilities()[1]))

    b.dbProxy.deleteAttacker(o.id())
  
  def tearDown(self):
    b = Borg()
    b.dbProxy.deleteEnvironment(self.oenvs[self.iep.name()].id())
    b.dbProxy.close()

if __name__ == '__main__':
  unittest.main()
