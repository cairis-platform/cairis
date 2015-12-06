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
from ARM import DatabaseProxyException

class EnvironmentTest(unittest.TestCase):

  def setUp(self):
    os.system("$CAIRIS_SRC/test/initdb.sh")
    BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/environments.json')
    d = json.load(f)
    f.close()
    self.ienvs = d['environments']
    

  def testStandardEnvironment(self):
    iep1 = EnvironmentParameters(self.ienvs[0]["theName"],self.ienvs[0]["theShortCode"],self.ienvs[0]["theDescription"])
    iep2 = EnvironmentParameters(self.ienvs[1]["theName"],self.ienvs[1]["theShortCode"],self.ienvs[1]["theDescription"])
    iep3 = EnvironmentParameters(self.ienvs[2]["theName"],self.ienvs[2]["theShortCode"],self.ienvs[2]["theDescription"])
    b = Borg()
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

    b.dbProxy.deleteEnvironment(oep1.id())
    b.dbProxy.deleteEnvironment(oep2.id())
    b.dbProxy.deleteEnvironment(oep3.id())
  

  def tearDown(self):
    b = Borg()
    b.dbProxy.close()
    os.system("$CAIRIS_SRC/test/dropdb.sh")

if __name__ == '__main__':
  unittest.main()
