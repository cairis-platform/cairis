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
from cairis.core.RoleParameters import RoleParameters
from cairis.core.AttackerParameters import AttackerParameters
from cairis.core.AttackerEnvironmentProperties import AttackerEnvironmentProperties

__author__ = 'Shamal Faily'


class AttackerTest(unittest.TestCase):

  def setUp(self):
    call([os.environ['CAIRIS_CFG_DIR'] + "/initdb.sh"])
    cairis.core.BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/attackers.json')
    d = json.load(f)
    f.close()
    ienvs = d['environments']
    iep = EnvironmentParameters(ienvs[0]["theName"],ienvs[0]["theShortCode"],ienvs[0]["theDescription"])
    iep1 = EnvironmentParameters(ienvs[1]["theName"],ienvs[1]["theShortCode"],ienvs[1]["theDescription"])
    b = Borg()
    b.dbProxy.addEnvironment(iep)
    b.dbProxy.addEnvironment(iep1)
    iRoles = d['roles']
    irp = RoleParameters(iRoles[0]["theName"], iRoles[0]["theType"], iRoles[0]["theShortCode"], iRoles[0]["theDescription"],[])
    b.dbProxy.addRole(irp)
    self.iAttackers = d['attackers']
    
  def testAttacker(self):
    iatkeps = [AttackerEnvironmentProperties(self.iAttackers[0]["theEnvironmentProperties"][0]["theName"],self.iAttackers[0]["theEnvironmentProperties"][0]["theRoles"],self.iAttackers[0]["theEnvironmentProperties"][0]["theMotives"],self.iAttackers[0]["theEnvironmentProperties"][0]["theCapabilities"]),AttackerEnvironmentProperties(self.iAttackers[0]["theEnvironmentProperties"][1]["theName"],self.iAttackers[0]["theEnvironmentProperties"][1]["theRoles"],self.iAttackers[0]["theEnvironmentProperties"][1]["theMotives"],self.iAttackers[0]["theEnvironmentProperties"][1]["theCapabilities"])]
    iatk = AttackerParameters(self.iAttackers[0]["theName"], self.iAttackers[0]["theDescription"], self.iAttackers[0]["theImage"],[],iatkeps)
    b = Borg()
    b.dbProxy.addAttacker(iatk)
    oAttackers = b.dbProxy.getAttackers()
    o = oAttackers[self.iAttackers[0]["theName"]]
    self.assertEqual(iatk.name(), o.name())
    self.assertEqual(iatk.description(),o.description())
    self.assertEqual(iatk.image(),o.image())
    oatkeps = o.environmentProperties()
    self.assertEqual(iatkeps[0].name(), oatkeps[0].name())
    self.assertEqual(str(iatkeps[0].roles()[0]), str(oatkeps[0].roles()[0]))
    self.assertEqual(str(iatkeps[0].roles()[0]), o.roles('Day','')[0])
    self.assertEqual(iatkeps[0].roles(), list(o.roles('','Maximise')))
    self.assertEqual(str(iatkeps[0].motives()[0]), str(oatkeps[0].motives()[0]))
    self.assertEqual(str(iatkeps[0].motives()[0]), str(o.motives('Day','')[0]))
    self.assertEqual(iatkeps[0].motives(), list(o.motives('','Maximise')))
    self.assertEqual(str(iatkeps[0].capabilities()[0][0]), str(oatkeps[0].capabilities()[0][0]))
    self.assertEqual(str(iatkeps[0].capabilities()[0][1]), str(oatkeps[0].capabilities()[0][1]))
    self.assertEqual(iatkeps[0].capabilities()[0][0], o.capability('Day','')[0][0])
    self.assertEqual(iatkeps[0].capabilities()[0][0], list(o.capability('','Maximise'))[0][0])

    iatk.theName = 'Updated name'
    iatk.setId(o.id())
    b.dbProxy.updateAttacker(iatk)
    oAttackers = b.dbProxy.getAttackers()
    o = oAttackers["Updated name"]
    self.assertEqual(o.name(),'Updated name')


    b.dbProxy.deleteAttacker(o.id())
  
  def tearDown(self):
    pass

if __name__ == '__main__':
  unittest.main()

