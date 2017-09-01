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

__author__ = 'Shamal Faily'


import unittest
import os
import json
from subprocess import call
import cairis.core.BorgFactory
import cairis.core.GoalFactory
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
from cairis.core.ResponseParameters import ResponseParameters
from cairis.core.AcceptEnvironmentProperties import AcceptEnvironmentProperties
from cairis.core.MitigateEnvironmentProperties import MitigateEnvironmentProperties
from cairis.core.ARM import DatabaseProxyException

class ResponseTest(unittest.TestCase):

  def setUp(self):
    call([os.environ['CAIRIS_CFG_DIR'] + "/initdb.sh"])
    cairis.core.BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/responses.json')
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
    iaeps2 = [AssetEnvironmentProperties(iassets[1]["theEnvironmentProperties"][0][0],iassets[1]["theEnvironmentProperties"][0][1],iassets[1]["theEnvironmentProperties"][0][2])]
    iaeps3 = [AssetEnvironmentProperties(iassets[2]["theEnvironmentProperties"][0][0],iassets[2]["theEnvironmentProperties"][0][1],iassets[2]["theEnvironmentProperties"][0][2])]
    iap1 = AssetParameters(iassets[0]["theName"],iassets[0]["theShortCode"],iassets[0]["theDescription"],iassets[0]["theSignificance"],iassets[0]["theType"],"0","N/A",[],[],iaeps1)
    iap2 = AssetParameters(iassets[1]["theName"],iassets[1]["theShortCode"],iassets[1]["theDescription"],iassets[1]["theSignificance"],iassets[1]["theType"],"0","N/A",[],[],iaeps2)
    iap3 = AssetParameters(iassets[2]["theName"],iassets[2]["theShortCode"],iassets[2]["theDescription"],iassets[2]["theSignificance"],iassets[2]["theType"],"0","N/A",[],[],iaeps3)
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
    imc = d['misuseCase']
    iRisks = d['risks']

    imcep = [MisuseCaseEnvironmentProperties(imc[0]["theEnvironmentProperties"][0]["theName"],imc[0]["theEnvironmentProperties"][0]["theDescription"])]
    imcp = MisuseCase(int(0), imc[0]["theName"], imcep,imc[0]["theRisk"])
    irp = RiskParameters(iRisks[0]["theName"],iRisks[0]["threatName"],iRisks[0]["vulName"], imcp,[])
    b.dbProxy.addRisk(irp)
    self.iResponses = d['responses']

  def testResponse(self):
    iar1Name = self.iResponses[0]["theType"] + " " + self.iResponses[0]["theRisk"] 
    iaep1 = AcceptEnvironmentProperties(self.iResponses[0]["theEnvironmentProperties"][0],self.iResponses[0]["theEnvironmentProperties"][1],self.iResponses[0]["theEnvironmentProperties"][2])
    iar1 = ResponseParameters(iar1Name,self.iResponses[0]["theRisk"],[],[iaep1], self.iResponses[0]["theType"])

    iar2Name = self.iResponses[1]["theType"] + " " + self.iResponses[1]["theRisk"] 
    iaep2 = MitigateEnvironmentProperties(self.iResponses[1]["theEnvironmentProperties"],self.iResponses[1]["theType"])
    iar2 = ResponseParameters(iar2Name,self.iResponses[1]["theRisk"],[],[iaep2], self.iResponses[1]["theType"])

    b = Borg()
    b.dbProxy.addResponse(iar1)
    b.dbProxy.addResponse(iar2)

    self.ors = b.dbProxy.getResponses()
    self.oar1 = self.ors[iar1Name]
    self.oar2 = self.ors[iar2Name]

    self.assertEqual(iar1.name(),self.oar1.name())
    self.assertEqual(iar1.risk(),self.oar1.risk())
    self.assertEqual(iar1.responseType(),self.oar1.responseType())
    self.assertEqual(iar1.environmentProperties()[0].cost(),self.oar1.environmentProperties()[0].cost())
    self.assertEqual(iar1.environmentProperties()[0].description(),self.oar1.environmentProperties()[0].description())
    self.assertEqual(iar2.name(),self.oar2.name())
    self.assertEqual(iar2.risk(),self.oar2.risk())
    self.assertEqual(iar2.responseType(),self.oar2.responseType())

    self.assertEqual([],self.oar2.roles('Day','',''))
    self.assertEqual([],self.oar2.roles('','Maximise',''))
    self.assertEqual([],self.oar2.roles('','Override','Day'))
    self.assertEqual([],self.oar2.roleNames('Day','',''))
    self.assertEqual([],self.oar2.roleNames('','Maximise',''))
    self.assertEqual([],self.oar2.roleNames('','Override','Day'))
    self.assertEqual('',self.oar2.cost('Day','',''))
    self.assertEqual('',self.oar2.cost('','Maximise',''))
    self.assertEqual('',self.oar2.cost('','Override','Day'))
    rgp = cairis.core.GoalFactory.build(self.oar2)
    riskParameters = rgp[0]
    riskGoalId = b.dbProxy.addGoal(riskParameters)
    b.dbProxy.addTrace('response_goal',self.oar2.id(),riskGoalId)
    if (len(rgp) > 1):
      threatParameters = rgp[1]
      vulnerabilityParameters = rgp[2]
      b.dbProxy.addGoal(vulnerabilityParameters)
      b.dbProxy.addGoal(threatParameters)
    b.dbProxy.relabelGoals(iaep2.name())

    oGoals = b.dbProxy.getGoals()
    rg = oGoals['Deter' + self.oar2.risk()]
    vg = oGoals[vulnerabilityParameters.name()]
    tg = oGoals[threatParameters.name()]

    ogops = b.dbProxy.getGoalAssociations()
    ogop1 = ogops[iaep2.name() + '/' + riskParameters.name() + '/' + threatParameters.name() + '/or']
    ogop2 = ogops[iaep2.name() + '/' + riskParameters.name() + '/' + vulnerabilityParameters.name() + '/or']

    b.dbProxy.deleteGoalAssociation(ogop1.id(),ogop1.goal(),ogop1.subGoal())
    b.dbProxy.deleteGoalAssociation(ogop2.id(),ogop2.goal(),ogop2.subGoal())
    b.dbProxy.deleteTrace('response',self.oar2.name(),'goal',rg.name())

    b.dbProxy.deleteGoal(tg.id())
    b.dbProxy.deleteGoal(vg.id())
    b.dbProxy.deleteGoal(rg.id())

    b.dbProxy.deleteResponse(self.oar2.id())
    b.dbProxy.deleteResponse(self.oar1.id())
  
  def tearDown(self):
    pass


if __name__ == '__main__':
  unittest.main()
