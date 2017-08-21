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
from cairis.core.ExternalDocumentParameters import ExternalDocumentParameters
from cairis.core.DocumentReferenceParameters import DocumentReferenceParameters
from cairis.core.PersonaCharacteristicParameters import PersonaCharacteristicParameters
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
    self.ienvs = d['environments']
    self.iep1 = EnvironmentParameters(self.ienvs[0]["theName"],self.ienvs[0]["theShortCode"],self.ienvs[0]["theDescription"])
    b = Borg()
    b.dbProxy.addEnvironment(self.iep1)
    self.oenvs = b.dbProxy.getEnvironments()
    self.iRoles = d['roles']
    self.irp = RoleParameters(self.iRoles[0]["theName"], self.iRoles[0]["theType"], self.iRoles[0]["theShortCode"], self.iRoles[0]["theDescription"],[])
    b.dbProxy.addRole(self.irp)
    self.oRoles = b.dbProxy.getRoles()
    self.iPersonas = d['personas']
    self.ipp = PersonaParameters(self.iPersonas[0]["theName"],self.iPersonas[0]["theActivities"],self.iPersonas[0]["theAttitudes"],self.iPersonas[0]["theAptitudes"],self.iPersonas[0]["theMotivations"],self.iPersonas[0]["theSkills"],self.iPersonas[0]["theIntrinsic"],self.iPersonas[0]["theContextual"],"","0",self.iPersonas[0]["thePersonaType"],[],[PersonaEnvironmentProperties(self.iPersonas[0]["theEnvironmentProperties"][0]["theName"],(self.iPersonas[0]["theEnvironmentProperties"][0]["theDirectFlag"] == "True"),self.iPersonas[0]["theEnvironmentProperties"][0]["theNarrative"],self.iPersonas[0]["theEnvironmentProperties"][0]["theRole"])],[])
    b.dbProxy.addPersona(self.ipp)
    self.opp = b.dbProxy.getPersonas()
    self.iExternalDocuments = d['external_documents']
    self.iec1 = ExternalDocumentParameters(self.iExternalDocuments[0]["theName"],self.iExternalDocuments[0]["theVersion"],self.iExternalDocuments[0]["thePublicationDate"],self.iExternalDocuments[0]["theAuthors"],self.iExternalDocuments[0]["theDescription"])
    self.iec2 = ExternalDocumentParameters(self.iExternalDocuments[1]["theName"],self.iExternalDocuments[1]["theVersion"],self.iExternalDocuments[1]["thePublicationDate"],self.iExternalDocuments[1]["theAuthors"],self.iExternalDocuments[1]["theDescription"])
    b.dbProxy.addExternalDocument(self.iec1)
    b.dbProxy.addExternalDocument(self.iec2)
    self.oecs = b.dbProxy.getExternalDocuments()
    self.iDocumentReferences = d['document_references']
    self.idr1 = DocumentReferenceParameters(self.iDocumentReferences[0]["theName"],self.iDocumentReferences[0]["theDocName"],self.iDocumentReferences[0]["theContributor"],self.iDocumentReferences[0]["theExcerpt"])
    self.idr2 = DocumentReferenceParameters(self.iDocumentReferences[1]["theName"],self.iDocumentReferences[1]["theDocName"],self.iDocumentReferences[1]["theContributor"],self.iDocumentReferences[1]["theExcerpt"])
    b.dbProxy.addDocumentReference(self.idr1)
    b.dbProxy.addDocumentReference(self.idr2)
    self.odrs = b.dbProxy.getDocumentReferences()
    self.iPersonaCharacteristics = d['persona_characteristics']
    self.ipc1 = PersonaCharacteristicParameters(self.iPersonaCharacteristics[0]["thePersonaName"],self.iPersonaCharacteristics[0]["theModQual"],self.iPersonaCharacteristics[0]["theVariable"],self.iPersonaCharacteristics[0]["theCharacteristic"],[(self.iPersonaCharacteristics[0]["ground"],'','document')],[(self.iPersonaCharacteristics[0]["warrant"],'','document')],[],[])
    b.dbProxy.addPersonaCharacteristic(self.ipc1)
    self.opcs = b.dbProxy.getPersonaCharacteristics()
    self.iAttackers = d['attackers']
    self.iatkeps = [AttackerEnvironmentProperties(self.iAttackers[0]["theEnvironmentProperties"][0]["theName"],self.iAttackers[0]["theEnvironmentProperties"][0]["theRoles"],self.iAttackers[0]["theEnvironmentProperties"][0]["theMotives"],self.iAttackers[0]["theEnvironmentProperties"][0]["theCapabilities"])]
    self.iatk = AttackerParameters(self.iAttackers[0]["theName"], self.iAttackers[0]["theDescription"], self.iAttackers[0]["theImage"],[],self.iatkeps)
    b.dbProxy.addAttacker(self.iatk)
    self.oAttackers = b.dbProxy.getAttackers()
    self.iVtypes = d['valuetypes']
    self.ivt1 = ValueTypeParameters(self.iVtypes[0]["theName"], self.iVtypes[0]["theDescription"], self.iVtypes[0]["theType"])
    self.ivt2 = ValueTypeParameters(self.iVtypes[1]["theName"], self.iVtypes[1]["theDescription"], self.iVtypes[1]["theType"])
    b.dbProxy.addValueType(self.ivt1)
    b.dbProxy.addValueType(self.ivt2)
    self.ovtt = b.dbProxy.getValueTypes('threat_type')
    self.ovtv = b.dbProxy.getValueTypes('vulnerability_type')
    self.iassets = d['assets']
    self.iaeps1 = [AssetEnvironmentProperties(self.iassets[0]["theEnvironmentProperties"][0][0],self.iassets[0]["theEnvironmentProperties"][0][1],self.iassets[0]["theEnvironmentProperties"][0][2])]
    self.iaeps2 = [AssetEnvironmentProperties(self.iassets[1]["theEnvironmentProperties"][0][0],self.iassets[1]["theEnvironmentProperties"][0][1],self.iassets[1]["theEnvironmentProperties"][0][2])]
    self.iaeps3 = [AssetEnvironmentProperties(self.iassets[2]["theEnvironmentProperties"][0][0],self.iassets[2]["theEnvironmentProperties"][0][1],self.iassets[2]["theEnvironmentProperties"][0][2])]
    self.iap1 = AssetParameters(self.iassets[0]["theName"],self.iassets[0]["theShortCode"],self.iassets[0]["theDescription"],self.iassets[0]["theSignificance"],self.iassets[0]["theType"],"0","N/A",[],[],self.iaeps1)
    self.iap2 = AssetParameters(self.iassets[1]["theName"],self.iassets[1]["theShortCode"],self.iassets[1]["theDescription"],self.iassets[1]["theSignificance"],self.iassets[1]["theType"],"0","N/A",[],[],self.iaeps2)
    self.iap3 = AssetParameters(self.iassets[2]["theName"],self.iassets[2]["theShortCode"],self.iassets[2]["theDescription"],self.iassets[2]["theSignificance"],self.iassets[2]["theType"],"0","N/A",[],[],self.iaeps3)
    b.dbProxy.addAsset(self.iap1)
    b.dbProxy.addAsset(self.iap2)
    b.dbProxy.addAsset(self.iap3)
    self.oap = b.dbProxy.getAssets()
    self.iThreats = d['threats']
    self.iteps = [ThreatEnvironmentProperties(self.iThreats[0]["theEnvironmentProperties"][0]["theName"],self.iThreats[0]["theEnvironmentProperties"][0]["theLikelihood"],self.iThreats[0]["theEnvironmentProperties"][0]["theAssets"],self.iThreats[0]["theEnvironmentProperties"][0]["theAttackers"],self.iThreats[0]["theEnvironmentProperties"][0]["theProperties"][0][1],self.iThreats[0]["theEnvironmentProperties"][0]["theProperties"][0][1])]
    self.itps = ThreatParameters(self.iThreats[0]["theName"],self.iThreats[0]["theType"],self.iThreats[0]["theMethod"],[],self.iteps)
    b.dbProxy.addThreat(self.itps)
    self.otps = b.dbProxy.getThreats()
    self.iVuln = d['vulnerabilities']
    self.iveps = [VulnerabilityEnvironmentProperties(self.iVuln[0]["theEnvironmentProperties"][0]["theName"],self.iVuln[0]["theEnvironmentProperties"][0]["theSeverity"],self.iVuln[0]["theEnvironmentProperties"][0]["theAssets"])]
    self.ivp = VulnerabilityParameters(self.iVuln[0]["theName"],self.iVuln[0]["theDescription"],self.iVuln[0]["theType"], [], self.iveps)
    b.dbProxy.addVulnerability(self.ivp)
    self.ovp = b.dbProxy.getVulnerabilities()
    self.imc = d['misuseCase']
    self.iRisks = d['risks']

    imcep = [MisuseCaseEnvironmentProperties(self.imc[0]["theEnvironmentProperties"][0]["theName"],self.imc[0]["theEnvironmentProperties"][0]["theDescription"])]
    imcp = MisuseCase(int(0), self.imc[0]["theName"], imcep,self.imc[0]["theRisk"])
    irp = RiskParameters(self.iRisks[0]["theName"],self.iRisks[0]["threatName"],self.iRisks[0]["vulName"], imcp,[])
    b.dbProxy.addRisk(irp)
    oRisks = b.dbProxy.getRisks()
    self.r = oRisks[self.iRisks[0]["theName"]]
    self.iResponses = d['responses']
    iar1Name = self.iResponses[0]["theType"] + " " + self.iResponses[0]["theRisk"] 
    iaep1 = AcceptEnvironmentProperties(self.iResponses[0]["theEnvironmentProperties"][0],self.iResponses[0]["theEnvironmentProperties"][1],self.iResponses[0]["theEnvironmentProperties"][2])
    iar1 = ResponseParameters(iar1Name,self.iResponses[0]["theRisk"],[],[iaep1], self.iResponses[0]["theType"])

    iar2Name = self.iResponses[1]["theType"] + " " + self.iResponses[1]["theRisk"] 
    iaep2 = MitigateEnvironmentProperties(self.iResponses[1]["theEnvironmentProperties"],self.iResponses[1]["theType"])
    iar2 = ResponseParameters(iar2Name,self.iResponses[1]["theRisk"],[],[iaep2], self.iResponses[1]["theType"])

    b.dbProxy.addResponse(iar1)
    b.dbProxy.addResponse(iar2)

    self.ors = b.dbProxy.getResponses()
    self.oar1 = self.ors[iar1Name]
    self.oar2 = self.ors[iar2Name]

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
    self.rg = oGoals['Deter' + self.oar2.risk()]
    self.vg = oGoals[vulnerabilityParameters.name()]
    self.tg = oGoals[threatParameters.name()]

    ogops = b.dbProxy.getGoalAssociations()
    self.ogop1 = ogops[iaep2.name() + '/' + riskParameters.name() + '/' + threatParameters.name() + '/or']
    self.ogop2 = ogops[iaep2.name() + '/' + riskParameters.name() + '/' + vulnerabilityParameters.name() + '/or']

    self.reqId = b.dbProxy.newId()
    self.irequirements = d['requirements']
    self.ireq = cairis.core.RequirementFactory.build(self.reqId,self.irequirements[0]["theLabel"],self.irequirements[0]["theName"],self.irequirements[0]["theDescription"],self.irequirements[0]["thePriority"],self.irequirements[0]["theRationale"],self.irequirements[0]["theFitCriterion"],self.irequirements[0]["theOriginator"],self.irequirements[0]["theType"],self.irequirements[0]["theReference"],1)
    b.dbProxy.addRequirement(self.ireq,self.irequirements[0]["theReference"],True)
    oreqs = b.dbProxy.getRequirements()
    self.oreq = oreqs[self.ireq.description()]

    iga = GoalAssociationParameters(iaep2.name(),self.vg.name(),'goal','and',self.oreq.name(),'requirement',0,'None')
    b.dbProxy.addGoalAssociation(iga)
    ogops = b.dbProxy.getGoalAssociations()
    self.ogop3 = ogops[iaep2.name() + '/' + self.vg.name() + '/' + self.oreq.name() + '/and']


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
    b = Borg()
    
    b.dbProxy.deleteGoalAssociation(self.ogop3.id(),self.ogop3.goal(),self.ogop3.subGoal())
    b.dbProxy.deleteRequirement(self.reqId)
    b.dbProxy.deleteGoalAssociation(self.ogop1.id(),self.ogop1.goal(),self.ogop1.subGoal())
    b.dbProxy.deleteGoalAssociation(self.ogop2.id(),self.ogop2.goal(),self.ogop2.subGoal())
    b.dbProxy.deleteTrace('response',self.oar2.name(),'goal',self.rg.name())
    b.dbProxy.deleteGoal(self.tg.id())
    b.dbProxy.deleteGoal(self.vg.id())
    b.dbProxy.deleteGoal(self.rg.id())
    b.dbProxy.deleteResponse(self.oar2.id())
    b.dbProxy.deleteResponse(self.oar1.id())
    b.dbProxy.deleteRisk(self.r.id())
    b.dbProxy.deleteVulnerability(self.ovp[self.ivp.name()].id())
    b.dbProxy.deleteThreat(self.otps[self.itps.name()].id())
    b.dbProxy.deleteAsset(self.oap[self.iap3.name()].id())
    b.dbProxy.deleteAsset(self.oap[self.iap2.name()].id())
    b.dbProxy.deleteAsset(self.oap[self.iap1.name()].id())
    b.dbProxy.deleteVulnerabilityType(0)
    b.dbProxy.deleteThreatType(0)
    b.dbProxy.deleteAttacker(self.oAttackers[self.iatk.name()].id())
    b.dbProxy.deleteDocumentReference(self.odrs[self.idr1.name()].id())
    b.dbProxy.deleteDocumentReference(self.odrs[self.idr2.name()].id())
    b.dbProxy.deleteExternalDocument(self.oecs[self.iec1.name()].id())
    b.dbProxy.deleteExternalDocument(self.oecs[self.iec2.name()].id())
    b.dbProxy.deletePersona(self.opp[self.ipp.name()].id())
    b.dbProxy.deleteRole(self.oRoles[self.irp.name()].id())
    b.dbProxy.deleteEnvironment(self.oenvs[self.iep1.name()].id())
    b.dbProxy.close()
    call([os.environ['CAIRIS_CFG_DIR'] + "/dropdb.sh"])


if __name__ == '__main__':
  unittest.main()
