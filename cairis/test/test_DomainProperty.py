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
from cairis.core.DomainPropertyParameters import DomainPropertyParameters
from cairis.core.ARM import AttributeTooBig

__author__ = 'Shamal Faily'


class DomainPropertyTest(unittest.TestCase):

  def setUp(self):
    call([os.environ['CAIRIS_CFG_DIR'] + "/initdb.sh"])
    cairis.core.BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/domainproperties.json')
    d = json.load(f)
    f.close()
    self.iDomainProperties = d['domain_properties']
    
  def testDomainProperty(self):
    idp = DomainPropertyParameters(self.iDomainProperties[0]["theName"], self.iDomainProperties[0]["theDefinition"], self.iDomainProperties[0]["theType"],self.iDomainProperties[0]["theOriginator"],[])
    b = Borg()
    idp.theOriginator = '0' * 200
    with self.assertRaises(AttributeTooBig):
      b.dbProxy.addDomainProperty(idp)
    idp.theOriginator = self.iDomainProperties[0]["theOriginator"]
    b.dbProxy.addDomainProperty(idp)
    odps = b.dbProxy.getDomainProperties()
    odp = odps[self.iDomainProperties[0]["theName"]]
    self.assertEqual(idp.name(), odp.name())
    self.assertEqual(idp.description(),odp.description())
    self.assertEqual(idp.type(),odp.type())
    self.assertEqual(idp.originator(),odp.originator())

    idp.theName = 'Updated name'
    idp.setId(odp.id())
    b.dbProxy.updateDomainProperty(idp)
    odps = b.dbProxy.getDomainProperties()
    odp = odps['Updated name']
    self.assertEqual(odp.name(),'Updated name')
    self.assertEqual(idp.description(),odp.description())
    self.assertEqual(idp.type(),odp.type())
    self.assertEqual(idp.originator(),odp.originator())

    b.dbProxy.deleteDomainProperty(odp.id())
  
  def tearDown(self):
    pass

if __name__ == '__main__':
  unittest.main()
