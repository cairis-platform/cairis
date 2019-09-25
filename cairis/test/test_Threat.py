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
from numpy import array

__author__ = 'Shamal Faily'


class ThreatTest(unittest.TestCase):

  def setUp(self):
    call([os.environ['CAIRIS_CFG_DIR'] + "/initdb.sh"])
    cairis.core.BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/threats.json')
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
    iAttackers = d['attackers']
    iatkeps = [AttackerEnvironmentProperties(iAttackers[0]["theEnvironmentProperties"][0]["theName"],iAttackers[0]["theEnvironmentProperties"][0]["theRoles"],iAttackers[0]["theEnvironmentProperties"][0]["theMotives"],iAttackers[0]["theEnvironmentProperties"][0]["theCapabilities"]),AttackerEnvironmentProperties(iAttackers[0]["theEnvironmentProperties"][1]["theName"],iAttackers[0]["theEnvironmentProperties"][1]["theRoles"],iAttackers[0]["theEnvironmentProperties"][1]["theMotives"],iAttackers[0]["theEnvironmentProperties"][1]["theCapabilities"])]
    iatk = AttackerParameters(iAttackers[0]["theName"], iAttackers[0]["theDescription"], iAttackers[0]["theImage"],[],iatkeps)
    b.dbProxy.addAttacker(iatk)
    iVtypes = d['valuetypes']
    ivt = ValueTypeParameters(iVtypes[0]["theName"], iVtypes[0]["theDescription"], iVtypes[0]["theType"])
    b.dbProxy.addValueType(ivt)
    iassets = d['assets']
    iaeps = [AssetEnvironmentProperties(iassets[0]["theEnvironmentProperties"][0][0],iassets[0]["theEnvironmentProperties"][0][1],iassets[0]["theEnvironmentProperties"][0][2]),AssetEnvironmentProperties(iassets[0]["theEnvironmentProperties"][1][0],iassets[0]["theEnvironmentProperties"][1][1],iassets[0]["theEnvironmentProperties"][1][2])]
    iap = AssetParameters(iassets[0]["theName"],iassets[0]["theShortCode"],iassets[0]["theDescription"],iassets[0]["theSignificance"],iassets[0]["theType"],"0","N/A",[],[],iaeps)
    b.dbProxy.addAsset(iap)
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
    self.assertEqual(iteps[0].assets(), o.assets('Day',''))
    self.assertEqual(iteps[0].assets(), list(o.assets('','Maximise')))
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
    self.assertEqual(array([0,2,0,0,0,0,0,0]).tolist(),o.securityProperties('','Maximise','').tolist())
    self.assertEqual(array([0,2,0,0,0,0,0,0]).tolist(),o.securityProperties('','Override','Day').tolist())
    self.assertEqual([['Integrity','Medium','None']],o.propertyList('','Maximise',''))
    self.assertEqual([['Integrity','Medium','None']],o.propertyList('','Override','Day'))

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
    pass

if __name__ == '__main__':
  unittest.main()
