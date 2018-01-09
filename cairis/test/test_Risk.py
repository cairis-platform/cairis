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
from cairis.core.VulnerabilityParameters import VulnerabilityParameters
from cairis.core.VulnerabilityEnvironmentProperties import VulnerabilityEnvironmentProperties
from cairis.core.MisuseCase import MisuseCase
from cairis.core.MisuseCaseEnvironmentProperties import MisuseCaseEnvironmentProperties
from cairis.core.RiskParameters import RiskParameters
from cairis.core.ARM import DatabaseProxyException

__author__ = 'Shamal Faily'


class RiskTest(unittest.TestCase):

  def setUp(self):
    call([os.environ['CAIRIS_CFG_DIR'] + "/initdb.sh"])
    cairis.core.BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/risks.json')
    d = json.load(f)
    f.close()
    ienvs = d['environments']
    iep1 = EnvironmentParameters(ienvs[0]["theName"],ienvs[0]["theShortCode"],ienvs[0]["theDescription"])
    b = Borg()
    b.dbProxy.addEnvironment(iep1)
    iRoles = d['roles']
    irp = RoleParameters(iRoles[0]["theName"], iRoles[0]["theType"], iRoles[0]["theShortCode"], iRoles[0]["theDescription"],[])
    b.dbProxy.addRole(irp)
    iAttackers = d['attackers']
    iatkeps = [AttackerEnvironmentProperties(iAttackers[0]["theEnvironmentProperties"][0]["theName"],iAttackers[0]["theEnvironmentProperties"][0]["theRoles"],iAttackers[0]["theEnvironmentProperties"][0]["theMotives"],iAttackers[0]["theEnvironmentProperties"][0]["theCapabilities"])]
    iatk = AttackerParameters(iAttackers[0]["theName"], iAttackers[0]["theDescription"], iAttackers[0]["theImage"],[],iatkeps)
    b.dbProxy.addAttacker(iatk)
    iVtypes = d['valuetypes']
    ivt1 = ValueTypeParameters(iVtypes[0]["theName"], iVtypes[0]["theDescription"], iVtypes[0]["theType"])
    ivt2 = ValueTypeParameters(iVtypes[1]["theName"], iVtypes[1]["theDescription"], iVtypes[1]["theType"])
    b.dbProxy.addValueType(ivt1)
    b.dbProxy.addValueType(ivt2)
    iassets = d['assets']
    iaeps1 = [AssetEnvironmentProperties(iassets[0]["theEnvironmentProperties"][0][0],iassets[0]["theEnvironmentProperties"][0][1],iassets[0]["theEnvironmentProperties"][0][2])]
    iap1 = AssetParameters(iassets[0]["theName"],iassets[0]["theShortCode"],iassets[0]["theDescription"],iassets[0]["theSignificance"],iassets[0]["theType"],"0","N/A",[],[],iaeps1)
    iap2 = AssetParameters(iassets[1]["theName"],iassets[1]["theShortCode"],iassets[1]["theDescription"],iassets[1]["theSignificance"],iassets[1]["theType"],"0","N/A",[],[],iaeps1)
    iap3 = AssetParameters(iassets[2]["theName"],iassets[2]["theShortCode"],iassets[2]["theDescription"],iassets[2]["theSignificance"],iassets[2]["theType"],"0","N/A",[],[],iaeps1)
    b.dbProxy.addAsset(iap1)
    b.dbProxy.addAsset(iap2)
    b.dbProxy.addAsset(iap3)
    iThreats = d['threats']
    iteps = [ThreatEnvironmentProperties(iThreats[0]["theEnvironmentProperties"][0]["theName"],iThreats[0]["theEnvironmentProperties"][0]["theLikelihood"],iThreats[0]["theEnvironmentProperties"][0]["theAssets"],iThreats[0]["theEnvironmentProperties"][0]["theAttackers"],iThreats[0]["theEnvironmentProperties"][0]["theProperties"][0][1],iThreats[0]["theEnvironmentProperties"][0]["theProperties"][0][1])]
    itps = ThreatParameters(iThreats[0]["theName"],iThreats[0]["theType"],iThreats[0]["theMethod"],[],iteps)
    b.dbProxy.addThreat(itps)
    iVuln = d['vulnerabilities']
    iveps = [VulnerabilityEnvironmentProperties(iVuln[0]["theEnvironmentProperties"][0]["theName"],iVuln[0]["theEnvironmentProperties"][0]["theSeverity"],iVuln[0]["theEnvironmentProperties"][0]["theAssets"])]
    ivp = VulnerabilityParameters(iVuln[0]["theName"],iVuln[0]["theDescription"],iVuln[0]["theType"], [], iveps)
    b.dbProxy.addVulnerability(ivp)
    self.imc = d['misuseCase']
    self.iRisks = d['risks']

  def testRisk(self):
    imcep = [MisuseCaseEnvironmentProperties(self.imc[0]["theEnvironmentProperties"][0]["theName"],self.imc[0]["theEnvironmentProperties"][0]["theDescription"])]
    imcp = MisuseCase(int(0), self.imc[0]["theName"], imcep,self.imc[0]["theRisk"])
    irp = RiskParameters(self.iRisks[0]["theName"],self.iRisks[0]["threatName"],self.iRisks[0]["vulName"], imcp,[])
    b = Borg()
    b.dbProxy.addRisk(irp)
    oRisks = b.dbProxy.getRisks()
    o = oRisks[self.iRisks[0]["theName"]]
    self.assertEqual(irp.name(), o.name())
    self.assertEqual(irp.threat(),o.threat())
    self.assertEqual(irp.vulnerability(),o.vulnerability())

    scoreDetails = b.dbProxy.riskScore(self.iRisks[0]["threatName"],self.iRisks[0]["vulName"],imcep[0].name())
    preScore = scoreDetails[0][1]
    postScore = scoreDetails[0][2]
    self.assertEqual(preScore,9)
    self.assertEqual(postScore,9)

    imcp.theName = 'Updated risk'
    imcp.theId = o.misuseCase().id()
    irp.theRiskName = 'Updated risk'
    irp.theMisuseCase = imcp

    irp.setId(o.id())
    b.dbProxy.updateRisk(irp)
    oRisks = b.dbProxy.getRisks()
    o = oRisks['Updated risk']
    self.assertEqual(o.name(),'Updated risk')
    self.assertEqual(irp.threat(),o.threat())
    self.assertEqual(irp.vulnerability(),o.vulnerability())
    
    b.dbProxy.deleteRisk(o.id())
  
  def tearDown(self):
    pass


if __name__ == '__main__':
  unittest.main()
