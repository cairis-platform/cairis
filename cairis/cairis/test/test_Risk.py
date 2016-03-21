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
import BorgFactory
from Borg import Borg
from EnvironmentParameters import EnvironmentParameters
from RoleParameters import RoleParameters
from PersonaParameters import PersonaParameters
from PersonaEnvironmentProperties import PersonaEnvironmentProperties
from ExternalDocumentParameters import ExternalDocumentParameters
from DocumentReferenceParameters import DocumentReferenceParameters
from PersonaCharacteristicParameters import PersonaCharacteristicParameters
from AttackerParameters import AttackerParameters
from AttackerEnvironmentProperties import AttackerEnvironmentProperties
from ValueTypeParameters import ValueTypeParameters
from AssetParameters import AssetParameters
from AssetEnvironmentProperties import AssetEnvironmentProperties
from ThreatParameters import ThreatParameters
from ThreatEnvironmentProperties import ThreatEnvironmentProperties
from VulnerabilityParameters import VulnerabilityParameters
from VulnerabilityEnvironmentProperties import VulnerabilityEnvironmentProperties
from MisuseCase import MisuseCase
from MisuseCaseEnvironmentProperties import MisuseCaseEnvironmentProperties
from RiskParameters import RiskParameters
from ARM import DatabaseProxyException

class RiskTest(unittest.TestCase):

  def setUp(self):
    BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/risks.json')
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

  def testRisk(self):
    imcep = [MisuseCaseEnvironmentProperties(self.imc[0]["theEnvironmentProperties"][0]["theName"],self.imc[0]["theEnvironmentProperties"][0]["theDescription"])]
    imcp = MisuseCase(int(0), self.imc[0]["theName"], imcep,self.imc[0]["theRisk"])
    irp = RiskParameters(self.iRisks[0]["theName"],self.iRisks[0]["threatName"],self.iRisks[0]["vulName"], imcp,[])
    b = Borg()
    b.dbProxy.addRisk(irp)
    oRisks = b.dbProxy.getRisks()
    o = oRisks[self.iRisks[0]["theName"]]
    self.assertEqual(irp.name(), o.name())
    self.assertEqual(itps.threat(),o.threat())
    self.assertEqual(itps.vulnerability(),o.vulnerability())
    self.assertEqual(itps.misuseCase(),o.misuseCase())

    b.dbProxy.deleteRisk(o.id())
  
  def tearDown(self):
    b = Borg()
    
    b.dbProxy.deleteVulnerability(self.ovp[self.ivp.name()].id())
    b.dbProxy.deleteThreat(self.otps[self.itps.name()].id())
#   b.dbProxy.deletePersonaCharacteristic(self.opcs[self.ipc1.name()].id())
    b.dbProxy.deleteAsset(self.oap[self.iap3.name()].id())
    b.dbProxy.deleteAsset(self.oap[self.iap2.name()].id())
    b.dbProxy.deleteAsset(self.oap[self.iap1.name()].id())
    b.dbProxy.deleteVulnerabilityType(self.ovtv[self.ivt2.name()].id())
    b.dbProxy.deleteThreatType(self.ovtt[self.ivt1.name()].id())
    b.dbProxy.deleteAttacker(self.oAttackers[self.iatk.name()].id())
    b.dbProxy.deleteDocumentReference(self.odrs[self.idr1.name()].id())
    b.dbProxy.deleteDocumentReference(self.odrs[self.idr2.name()].id())
    b.dbProxy.deleteExternalDocument(self.oecs[self.iec1.name()].id())
    b.dbProxy.deleteExternalDocument(self.oecs[self.iec2.name()].id())
    b.dbProxy.deletePersona(self.opp[self.ipp.name()].id())
    b.dbProxy.deleteRole(self.oRoles[self.irp.name()].id())
    b.dbProxy.deleteEnvironment(self.oenvs[self.iep1.name()].id())
    b.dbProxy.close()

if __name__ == '__main__':
  unittest.main()
