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
from cairis.core.ARM import DatabaseProxyException, AttributeTooBig

__author__ = 'Shamal Faily'

class EnvironmentTest(unittest.TestCase):

  def setUp(self):
    call([os.environ['CAIRIS_CFG_DIR'] + "/initdb.sh"])
    cairis.core.BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/environments.json')
    d = json.load(f)
    f.close()
    self.ienvs = d['environments']

  def testStandardEnvironment(self):
    iep1 = EnvironmentParameters(self.ienvs[0]["theName"],self.ienvs[0]["theShortCode"],self.ienvs[0]["theDescription"])
    iep2 = EnvironmentParameters(self.ienvs[1]["theName"],self.ienvs[1]["theShortCode"],self.ienvs[1]["theDescription"])
    iep3 = EnvironmentParameters(self.ienvs[2]["theName"],self.ienvs[2]["theShortCode"],self.ienvs[2]["theDescription"])
    b = Borg()
    iep1.theShortCode = '0' * 25
    with self.assertRaises(AttributeTooBig):
      b.dbProxy.addEnvironment(iep1)
    iep1.theShortCode = self.ienvs[0]["theShortCode"]
    b.dbProxy.addEnvironment(iep1)
    b.dbProxy.addEnvironment(iep2)
    b.dbProxy.addEnvironment(iep3)
    oenvs = b.dbProxy.getEnvironments()
    oep1 = oenvs[self.ienvs[0]["theName"]]
    self.assertEqual(iep1.name(), oep1.name())
    self.assertEqual(iep1.shortCode(),oep1.shortCode())
    self.assertEqual(iep1.description(),oep1.description())
    oep2 = oenvs[self.ienvs[1]["theName"]]
    self.assertEqual(iep2.name(), oep2.name())
    self.assertEqual(iep2.shortCode(),oep2.shortCode())
    self.assertEqual(iep2.description(),oep2.description())
    oep3 = oenvs[self.ienvs[2]["theName"]]
    self.assertEqual(iep3.name(), oep3.name())
    self.assertEqual(iep3.shortCode(),oep3.shortCode())
    self.assertEqual(iep3.description(),oep3.description())

    iep4 = EnvironmentParameters(self.ienvs[3]["Composite_name"],'COMP','Composite test',[iep1.name(),iep2.name(),iep3.name()],self.ienvs[4]["Duplication"])
    b.dbProxy.addEnvironment(iep4)

    oenvs = b.dbProxy.getEnvironments()
    oep4 = oenvs[self.ienvs[3]["Composite_name"]]
    self.assertEqual(iep4.name(), oep4.name())
    self.assertEqual(iep4.shortCode(),oep4.shortCode())
    self.assertEqual(iep4.description(),oep4.description())
    self.assertEqual(iep4.environments(),oep4.environments())
    self.assertEqual(iep4.duplicateProperty(),oep4.duplicateProperty())

    oep1 = oenvs[self.ienvs[0]["theName"]]
    oep2 = oenvs[self.ienvs[1]["theName"]]
    oep3 = oenvs[self.ienvs[2]["theName"]]

    self.assertRaises(DatabaseProxyException,b.dbProxy.deleteEnvironment,oep1.id())
    b.dbProxy.deleteEnvironment(oep4.id())
    b.dbProxy.deleteEnvironment(oep1.id())
    b.dbProxy.deleteEnvironment(oep2.id())
    b.dbProxy.deleteEnvironment(oep3.id())

  def tearDown(self):
    pass

if __name__ == '__main__':
  unittest.main()
