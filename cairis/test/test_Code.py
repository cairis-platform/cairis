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
from cairis.core.CodeParameters import CodeParameters
import sys

class CodeTest(unittest.TestCase):

  def setUp(self):
    call([os.environ['CAIRIS_CFG_DIR'] + "/initdb.sh"])
    cairis.core.BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/processes.json')
    d = json.load(f)
    f.close()
    self.iCodes = d['codes']
    

  def testAddUpdateCode(self):
    i = CodeParameters(self.iCodes[0]["theName"], self.iCodes[0]["theType"],self.iCodes[0]["theDescription"], self.iCodes[0]["theInclusionCriteria"], self.iCodes[0]["theExample"])
    b = Borg()
    b.dbProxy.addCode(i)
    ocs = b.dbProxy.getCodes()
    o = ocs[self.iCodes[0]["theName"]]
    self.assertEqual(i.name(), o.name())
    self.assertEqual(i.type(), o.type())
    self.assertEqual(i.description(),o.description())
    self.assertEqual(i.inclusionCriteria(),o.inclusionCriteria())
    self.assertEqual(i.example(),o.example())

    o.theDescription = 'Updated description'
    b.dbProxy.updateCode(o)

    ocs2 = b.dbProxy.getCodes(o.id())
    o2 = ocs2[self.iCodes[0]["theName"]]
    self.assertEqual(i.name(), o2.name())
    self.assertEqual(i.type(), o2.type())
    self.assertEqual('Updated description',o2.description())
    self.assertEqual(i.inclusionCriteria(),o2.inclusionCriteria())
    self.assertEqual(i.example(),o2.example())

    b.dbProxy.deleteCode(o.id())
  
  def tearDown(self):
    b = Borg()
    b.dbProxy.close()
    call([os.environ['CAIRIS_CFG_DIR'] + "/dropdb.sh"])

if __name__ == '__main__':
  unittest.main()
