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
import cairis.core.BorgFactory
import os
from subprocess import call
from cairis.core.Borg import Borg

class BorgFactoryTest(unittest.TestCase):

  def setUp(self):
    call([os.environ['CAIRIS_SRC'] + "/test/initdb.sh"])
    cairis.core.BorgFactory.initialise()

  def testProjectSettings(self):
    b = Borg()
    self.assertEqual(b.fontName,'Times New Roman')
    self.assertEqual(b.fontSize,'7.5')
    self.assertEqual(b.apFontSize,'13')

  def tearDown(self):
    b = Borg()
    b.dbProxy.close()
    call([os.environ['CAIRIS_SRC'] + "/test/dropdb.sh"])

if __name__ == '__main__':
  unittest.main()
