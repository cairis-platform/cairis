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
import BorgFactory
from Borg import Borg
from EnvironmentParameters import EnvironmentParameters

class EnvironmentTest(unittest.TestCase):

  def setUp(self):
    os.system("$CAIRIS_SRC/test/initdb.sh")
    BorgFactory.initialise()

  def testStandardEnvironment(self):
    envName = 'anEnvironment'
    shortCode = 'ENV'
    desc = 'An environment description'
    iep = EnvironmentParameters(envName,shortCode,desc)
    b = Borg()
    b.dbProxy.addEnvironment(iep)
    envs = b.dbProxy.getEnvironments()
    oep = envs[envName]
    self.assertEqual(iep.name(),oep.name())
    self.assertEqual(iep.shortCode(),oep.shortCode())
    self.assertEqual(iep.description(),oep.description())

  def tearDown(self):
    b = Borg()
    b.dbProxy.close()
    os.system("$CAIRIS_SRC/test/dropdb.sh")

if __name__ == '__main__':
  unittest.main()
