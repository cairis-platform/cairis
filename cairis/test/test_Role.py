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
from cairis.core.RoleParameters import RoleParameters
import sys

class RoleTest(unittest.TestCase):

  def setUp(self):
    call([os.environ['CAIRIS_CFG_DIR'] + "/initdb.sh"])
    cairis.core.BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/roles.json')
    d = json.load(f)
    f.close()
    self.iRoles = d['roles']
    

  def testRole(self):
    irp = RoleParameters(self.iRoles[0]["theName"], self.iRoles[0]["theType"], self.iRoles[0]["theShortCode"], self.iRoles[0]["theDescription"],[])
    b = Borg()
    b.dbProxy.addRole(irp)
    oRoles = b.dbProxy.getRoles()
    o = oRoles[self.iRoles[0]["theName"]]
    self.assertEqual(irp.name(), o.name())
    self.assertEqual(irp.shortCode(),o.shortCode())
    self.assertEqual(irp.description(),o.description())

    o.theShortCode = 'TESTROLE'
    b.dbProxy.updateRole(o)

    oRoles2 = b.dbProxy.getRoles(o.id())
    o2 = oRoles[self.iRoles[0]["theName"]]
    self.assertEqual(o2.shortCode(),"TESTROLE")

    b.dbProxy.deleteRole(o.id())
  
  def tearDown(self):
    pass

if __name__ == '__main__':
  unittest.main()
