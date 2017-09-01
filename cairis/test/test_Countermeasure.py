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
import cairis.core.GoalFactory
from cairis.core.Borg import Borg
from cairis.core.EnvironmentParameters import EnvironmentParameters
from cairis.core.RoleParameters import RoleParameters
from cairis.core.PersonaParameters import PersonaParameters
from cairis.core.PersonaEnvironmentProperties import PersonaEnvironmentProperties
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
from cairis.core.GoalAssociationParameters import GoalAssociationParameters
from cairis.core.CountermeasureParameters import CountermeasureParameters
from cairis.core.CountermeasureEnvironmentProperties import CountermeasureEnvironmentProperties
from cairis.core.Target import Target
import cairis.core.RequirementFactory
from cairis.core.ARM import DatabaseProxyException

__author__ = 'Shamal Faily'


class CountermeasureTest(unittest.TestCase):

  def setUp(self):
    call([os.environ['CAIRIS_CFG_DIR'] + "/initdb.sh"])
    cairis.core.BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/countermeasures.json')
    d = json.load(f)
    f.close()
    ienvs = d['environments']
    iep1 = EnvironmentParameters(ienvs[0]["theName"],ienvs[0]["theShortCode"],ienvs[0]["theDescription"])
    b = Borg()
    b.dbProxy.addEnvironment(iep1)
    iRoles = d['roles']
    irp = RoleParameters(iRoles[0]["theName"], iRoles[0]["theType"], iRoles[0]["theShortCode"], iRoles[0]["theDescription"],[])
    b.dbProxy.addRole(irp)
    iPersonas = d['personas']
    ipp = PersonaParameters(iPersonas[0]["theName"],iPersonas[0]["theActivities"],iPersonas[0]["theAttitudes"],iPersonas[0]["theAptitudes"],iPersonas[0]["theMotivations"],iPersonas[0]["theSkills"],iPersonas[0]["theIntrinsic"],iPersonas[0]["theContextual"],"","0",iPersonas[0]["thePersonaType"],[],[PersonaEnvironmentProperties(iPersonas[0]["theEnvironmentProperties"][0]["theName"],(iPersonas[0]["theEnvironmentProperties"][0]["theDirectFlag"] == "True"),iPersonas[0]["theEnvironmentProperties"][0]["theNarrative"],iPersonas[0]["theEnvironmentProperties"][0]["theRole"])],[])
    b.dbProxy.addPersona(ipp)
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
    iResponses = d['responses']
    iar1Name = iResponses[0]["theType"] + " " + iResponses[0]["theRisk"] 
    iaep1 = AcceptEnvironmentProperties(iResponses[0]["theEnvironmentProperties"][0],iResponses[0]["theEnvironmentProperties"][1],iResponses[0]["theEnvironmentProperties"][2])
    iar1 = ResponseParameters(iar1Name,iResponses[0]["theRisk"],[],[iaep1], iResponses[0]["theType"])

    iar2Name = iResponses[1]["theType"] + " " + iResponses[1]["theRisk"] 
    iaep2 = MitigateEnvironmentProperties(iResponses[1]["theEnvironmentProperties"],iResponses[1]["theType"])
    iar2 = ResponseParameters(iar2Name,iResponses[1]["theRisk"],[],[iaep2], iResponses[1]["theType"])

    b.dbProxy.addResponse(iar1)
    b.dbProxy.addResponse(iar2)

    ors = b.dbProxy.getResponses()
    oar1 = ors[iar1Name]
    oar2 = ors[iar2Name]

    rgp = cairis.core.GoalFactory.build(oar2)
    riskParameters = rgp[0]
    riskGoalId = b.dbProxy.addGoal(riskParameters)
    b.dbProxy.addTrace('response_goal',oar2.id(),riskGoalId)
    if (len(rgp) > 1):
      threatParameters = rgp[1]
      vulnerabilityParameters = rgp[2]
      b.dbProxy.addGoal(vulnerabilityParameters)
      b.dbProxy.addGoal(threatParameters)
    b.dbProxy.relabelGoals(iaep2.name())

    oGoals = b.dbProxy.getGoals()
    rg = oGoals['Deter' + oar2.risk()]
    vg = oGoals[vulnerabilityParameters.name()]
    tg = oGoals[threatParameters.name()]

    reqId = b.dbProxy.newId()
    irequirements = d['requirements']
    ireq = cairis.core.RequirementFactory.build(reqId,irequirements[0]["theLabel"],irequirements[0]["theName"],irequirements[0]["theDescription"],irequirements[0]["thePriority"],irequirements[0]["theRationale"],irequirements[0]["theFitCriterion"],irequirements[0]["theOriginator"],irequirements[0]["theType"],irequirements[0]["theReference"],1)
    b.dbProxy.addRequirement(ireq,irequirements[0]["theReference"],True)

    oreqs = b.dbProxy.getRequirements()
    oreq = oreqs[ireq.description()]

    iga = GoalAssociationParameters(iaep2.name(),vg.name(),'goal','and',oreq.name(),'requirement',0,'None')
    b.dbProxy.addGoalAssociation(iga)
    ogops = b.dbProxy.getGoalAssociations()
    self.ogop3 = ogops[iaep2.name() + '/' + vg.name() + '/' + oreq.name() + '/and']
    self.iCountermeasures = d['countermeasures']


  def testCountermeasure(self):

    icep = CountermeasureEnvironmentProperties(self.iCountermeasures[0]["theEnvironmentProperties"][0][0],[self.iCountermeasures[0]["theEnvironmentProperties"][0][2]],[Target(self.iCountermeasures[0]["theEnvironmentProperties"][0][3],self.iCountermeasures[0]["theEnvironmentProperties"][0][4],"None")],[0,0,0,0,0,0,0,0],['None','None','None','None','None','None','None','None'],self.iCountermeasures[0]["theEnvironmentProperties"][0][1],[self.iCountermeasures[0]["theEnvironmentProperties"][0][5]])
    icm = CountermeasureParameters(self.iCountermeasures[0]["theName"],self.iCountermeasures[0]["theDescription"],self.iCountermeasures[0]["theType"],[],[icep])

    b = Borg()
    b.dbProxy.addCountermeasure(icm)
    ocms = b.dbProxy.getCountermeasures()
    ocm = ocms[self.iCountermeasures[0]["theName"]]
    self.assertEqual(icm.name(), ocm.name())
    self.assertEqual(icm.type(),ocm.type())
    self.assertEqual(icm.description(),ocm.description())

    icm.theName = 'Updated countermeasure'
    icm.setId(ocm.id())
    b.dbProxy.updateCountermeasure(icm)
    ocms = b.dbProxy.getCountermeasures()
    ocm = ocms['Updated countermeasure']
    self.assertEqual('Updated countermeasure', ocm.name())
    self.assertEqual(icm.type(),ocm.type())
    self.assertEqual(icm.description(),ocm.description())

    b.dbProxy.deleteCountermeasure(ocm.id())
  
  def tearDown(self):
    pass


if __name__ == '__main__':
  unittest.main()
