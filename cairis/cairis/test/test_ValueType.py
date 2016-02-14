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
from ValueTypeParameters import ValueTypeParameters

class ValueTypeTest(unittest.TestCase):

  def setUp(self):
    BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/valuetypes.json')
    d = json.load(f)
    f.close()
    self.iVtypes = d['types']
    

  def testValueType(self):
    ivt1 = ValueTypeParameters(self.iVtypes[0]["theName"], self.iVtypes[0]["theDescription"], self.iVtypes[0]["theType"])
    ivt2 = ValueTypeParameters(self.iVtypes[1]["theName"], self.iVtypes[1]["theDescription"], self.iVtypes[1]["theType"])
    b = Borg()
    b.dbProxy.addValueType(ivt1)
    b.dbProxy.addValueType(ivt2)
    oVtypes = b.dbProxy.getValueTypes()
    ovt1 = oVtypes[self.iVtypes[0]["theName"]]
    self.assertEqual(ivt1.name(), ovt1.name())
    self.assertEqual(ivt1.shortCode(),ovt1.description())
    self.assertEqual(ivt1.description(),ovt1.type())
    ovt2 = oVtypes[self.iVtypes[1]["theName"]]
    self.assertEqual(ivt2.name(), ovt2.name())
    self.assertEqual(ivt2.shortCode(),ovt2.description())
    self.assertEqual(ivt2.description(),ovt2.type())

    b.dbProxy.deleteVulnerabilityType(ovt1.id())
    b.dbProxy.deleteThreatType(ovt2.id())
  
  def tearDown(self):
    b = Borg()
    b.dbProxy.close()

if __name__ == '__main__':
  unittest.main()
