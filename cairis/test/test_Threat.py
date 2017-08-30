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
from cairis.core.ValueTypeParameters import ValueTypeParameters
from cairis.core.AssetParameters import AssetParameters
from cairis.core.AssetEnvironmentProperties import AssetEnvironmentProperties
from cairis.core.ThreatParameters import ThreatParameters
from cairis.core.ThreatEnvironmentProperties import ThreatEnvironmentProperties
from cairis.core.ARM import DatabaseProxyException

__author__ = 'Shamal Faily'


class ThreatTest(unittest.TestCase):

  def setUp(self):
    call([os.environ['CAIRIS_CFG_DIR'] + "/initdb.sh"])
    cairis.core.BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/threats.json')
    d = json.load(f)
    f.close()
    self.ienvs = d['environments']
    self.iep = EnvironmentParameters(self.ienvs[0]["theName"],self.ienvs[0]["theShortCode"],self.ienvs[0]["theDescription"])
    self.iep1 = EnvironmentParameters(self.ienvs[1]["theName"],self.ienvs[1]["theShortCode"],self.ienvs[1]["theDescription"])
    b = Borg()
    b.dbProxy.addEnvironment(self.iep)
    b.dbProxy.addEnvironment(self.iep1)
    self.oenvs = b.dbProxy.getEnvironments()
    self.iRoles = d['roles']
    self.irp = RoleParameters(self.iRoles[0]["theName"], self.iRoles[0]["theType"], self.iRoles[0]["theShortCode"], self.iRoles[0]["theDescription"],[])
    b.dbProxy.addRole(self.irp)
    self.oRoles = b.dbProxy.getRoles()

    self.iAttackers = d['attackers']
    self.iatkeps = [AttackerEnvironmentProperties(self.iAttackers[0]["theEnvironmentProperties"][0]["theName"],self.iAttackers[0]["theEnvironmentProperties"][0]["theRoles"],self.iAttackers[0]["theEnvironmentProperties"][0]["theMotives"],self.iAttackers[0]["theEnvironmentProperties"][0]["theCapabilities"]),AttackerEnvironmentProperties(self.iAttackers[0]["theEnvironmentProperties"][1]["theName"],self.iAttackers[0]["theEnvironmentProperties"][1]["theRoles"],self.iAttackers[0]["theEnvironmentProperties"][1]["theMotives"],self.iAttackers[0]["theEnvironmentProperties"][1]["theCapabilities"])]
    self.iatk = AttackerParameters(self.iAttackers[0]["theName"], self.iAttackers[0]["theDescription"], self.iAttackers[0]["theImage"],[],self.iatkeps)
    b.dbProxy.addAttacker(self.iatk)
    self.oAttackers = b.dbProxy.getAttackers()
    self.iVtypes = d['valuetypes']
    self.ivt = ValueTypeParameters(self.iVtypes[0]["theName"], self.iVtypes[0]["theDescription"], self.iVtypes[0]["theType"])
    b.dbProxy.addValueType(self.ivt)
    self.ovt = b.dbProxy.getValueTypes('threat_type')
    self.iassets = d['assets']
    self.iaeps = [AssetEnvironmentProperties(self.iassets[0]["theEnvironmentProperties"][0][0],self.iassets[0]["theEnvironmentProperties"][0][1],self.iassets[0]["theEnvironmentProperties"][0][2]),AssetEnvironmentProperties(self.iassets[0]["theEnvironmentProperties"][1][0],self.iassets[0]["theEnvironmentProperties"][1][1],self.iassets[0]["theEnvironmentProperties"][1][2])]
    self.iap = AssetParameters(self.iassets[0]["theName"],self.iassets[0]["theShortCode"],self.iassets[0]["theDescription"],self.iassets[0]["theSignificance"],self.iassets[0]["theType"],"0","N/A",[],[],self.iaeps)
    b.dbProxy.addAsset(self.iap)
    self.oap = b.dbProxy.getAssets()
    self.iThreats = d['threats']

  def testThreat(self):
    iteps = [ThreatEnvironmentProperties(self.iThreats[0]["theEnvironmentProperties"][0]["theName"],self.iThreats[0]["theEnvironmentProperties"][0]["theLikelihood"],self.iThreats[0]["theEnvironmentProperties"][0]["theAssets"],self.iThreats[0]["theEnvironmentProperties"][0]["theAttackers"],self.iThreats[0]["theEnvironmentProperties"][0]["theProperties"][0][1],self.iThreats[0]["theEnvironmentProperties"][0]["theProperties"][0][1]),ThreatEnvironmentProperties(self.iThreats[0]["theEnvironmentProperties"][1]["theName"],self.iThreats[0]["theEnvironmentProperties"][1]["theLikelihood"],self.iThreats[0]["theEnvironmentProperties"][1]["theAssets"],self.iThreats[0]["theEnvironmentProperties"][1]["theAttackers"],self.iThreats[0]["theEnvironmentProperties"][1]["theProperties"][0][1],self.iThreats[0]["theEnvironmentProperties"][1]["theProperties"][0][1])]
    itps = ThreatParameters(self.iThreats[0]["theName"],self.iThreats[0]["theType"],self.iThreats[0]["theMethod"],[],iteps)
    b = Borg()
    b.dbProxy.addThreat(itps)
    oThreats = b.dbProxy.getThreats()
    o = oThreats[self.iThreats[0]["theName"]]
    self.assertEqual(itps.name(), o.name())
    self.assertEqual(itps.type(),o.type())
    self.assertEqual(itps.method(),o.method())
    oteps = o.environmentProperties()
    self.assertEqual(iteps[0].name(), oteps[0].name())

    self.assertEqual(iteps[0].likelihood(), oteps[0].likelihood())
    self.assertEqual(iteps[0].likelihood(),o.likelihood('Day','Maximise','None'))
    self.assertEqual(iteps[0].likelihood(),o.likelihood('','Maximise','None'))
    self.assertEqual(iteps[0].likelihood(),o.likelihood('','Override','Day'))
    self.assertEqual(iteps[0].assets(), oteps[0].assets())
    self.assertEqual(iteps[0].attackers(), oteps[0].attackers())
    self.assertEqual(iteps[0].attackers(), o.attackers('Day',''))
    self.assertEqual(iteps[0].attackers(), list(o.attackers('','Maximise')))
    self.assertEqual(str(iteps[0].rationale()[0]), oteps[0].rationale()[0])
    self.assertEqual(str(iteps[0].rationale()[1]), oteps[0].rationale()[1])
    self.assertEqual(str(iteps[0].rationale()[2]), oteps[0].rationale()[2])
    self.assertEqual(str(iteps[0].rationale()[3]), oteps[0].rationale()[3])
    self.assertEqual(str(iteps[0].rationale()[4]), oteps[0].rationale()[4])
    self.assertEqual(str(iteps[0].rationale()[5]), oteps[0].rationale()[5])
    self.assertEqual(str(iteps[0].rationale()[6]), oteps[0].rationale()[6])
    self.assertEqual(str(iteps[0].rationale()[7]), oteps[0].rationale()[7])

    envName = self.iThreats[0]["theEnvironmentProperties"][0]["theName"]
    self.assertEqual(iteps[0].likelihood(), o.likelihood(envName,'',envName))
    self.assertEqual(iteps[0].assets(), o.assets(envName,''))
    self.assertEqual(iteps[0].attackers(), o.attackers(envName,''))


    itps.theName = 'Updated threat'
    itps.setId(o.id())
    b.dbProxy.updateThreat(itps)
    oThreats = b.dbProxy.getThreats()
    o = oThreats['Updated threat']
    self.assertEqual(o.name(),'Updated threat')


    b.dbProxy.deleteThreat(o.id())
  
  def tearDown(self):
    b = Borg()
    b.dbProxy.close()

if __name__ == '__main__':
  unittest.main()
