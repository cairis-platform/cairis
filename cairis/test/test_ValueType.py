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
from cairis.core.ValueTypeParameters import ValueTypeParameters

__author__ = 'Ashley Ritchie, Shamal Faily'


class ValueTypeTest(unittest.TestCase):

  def setUp(self):
    call([os.environ['CAIRIS_CFG_DIR'] + "/initdb.sh"])
    cairis.core.BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/valuetypes.json')
    d = json.load(f)
    f.close()
    self.iVtypes = d['vulnerability_type'] + d['threat_type']
    
  def testValueType(self):
    ivt1 = ValueTypeParameters(self.iVtypes[0]["theName"], self.iVtypes[0]["theDescription"], self.iVtypes[0]["theType"],self.iVtypes[0]['theEnvironmentName'])
    ivt2 = ValueTypeParameters(self.iVtypes[1]["theName"], self.iVtypes[1]["theDescription"], self.iVtypes[1]["theType"],self.iVtypes[1]['theEnvironmentName'])
    b = Borg()
    b.dbProxy.addValueType(ivt1)
    b.dbProxy.addValueType(ivt2)
    oVVtypes = b.dbProxy.getValueTypes('vulnerability_type')
    ovt1 = oVVtypes[ivt1.id()]
    self.assertEqual(ivt1.name(), ovt1.name())
    self.assertEqual(ivt1.description(),ovt1.description())
    self.assertEqual(ivt1.type(),ovt1.type())
    oVTtypes = b.dbProxy.getValueTypes('threat_type')
    ovt2 = oVTtypes[ivt2.id()]
    self.assertEqual(ivt2.name(), ovt2.name())
    self.assertEqual(ivt2.description(),ovt2.description())
    self.assertEqual(ivt2.type(),ovt2.type())

    b.dbProxy.deleteVulnerabilityType(ovt1.id())
    b.dbProxy.deleteThreatType(ovt2.id())
  
  def tearDown(self):
    pass

if __name__ == '__main__':
  unittest.main()
