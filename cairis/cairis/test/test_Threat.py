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
from ARM import DatabaseProxyException

class ThreatTest(unittest.TestCase):

  def setUp(self):
    BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/threats.json')
    d = json.load(f)
    f.close()
    self.ienvs = d['environments']
    self.iep = EnvironmentParameters(self.ienvs[0]["theName"],self.ienvs[0]["theShortCode"],self.ienvs[0]["theDescription"])
    b = Borg()
    b.dbProxy.addEnvironment(self.iep)
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
    self.ivt = ValueTypeParameters(self.iVtypes[0]["theName"], self.iVtypes[0]["theDescription"], self.iVtypes[0]["theType"])
    b.dbProxy.addValueType(self.ivt)
    self.ovt = b.dbProxy.getValueTypes('threat_type')
    self.iassets = d['assets']
    self.iaeps = [AssetEnvironmentProperties(self.iassets[0]["theEnvironmentProperties"][0][0],self.iassets[0]["theEnvironmentProperties"][0][1],self.iassets[0]["theEnvironmentProperties"][0][2])]
    self.iap = AssetParameters(self.iassets[0]["theName"],self.iassets[0]["theShortCode"],self.iassets[0]["theDescription"],self.iassets[0]["theSignificance"],self.iassets[0]["theType"],"0","N/A",[],[],self.iaeps)
    b.dbProxy.addAsset(self.iap)
    self.oap = b.dbProxy.getAssets()
    self.iThreats = d['threats']

  def testThreat(self):
    iteps = [ThreatEnvironmentProperties(self.iThreats[0]["theEnvironmentProperties"][0]["theName"],self.iThreats[0]["theEnvironmentProperties"][0]["theLikelihood"],self.iThreats[0]["theEnvironmentProperties"][0]["theAssets"],self.iThreats[0]["theEnvironmentProperties"][0]["theAttackers"],self.iThreats[0]["theEnvironmentProperties"][0]["theProperties"][0][0],self.iThreats[0]["theEnvironmentProperties"][0]["theProperties"][0][1])]
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
    self.assertEqual(iteps[0].likelihood()[0], oteps[0].likelihood()[0])
    self.assertEqual(str(iteps[0].assets()[0]), str(oteps[0].assets()[0]))
    self.assertEqual(str(iteps[0].attackers()[0]), str(oteps[0].attackers()[0]))
    self.assertEqual(str(iteps[0].properties()[0]), str(oteps[0].properties()[0][0]))
    self.assertEqual(str(iteps[0].properties()[2]), str(oteps[0].properties()[2]))

    b.dbProxy.deleteThreat(o.id())
  
  def tearDown(self):
    b = Borg()
    
#   b.dbProxy.deletePersonaCharacteristic(self.opcs[self.ipc1.name()].id())
    b.dbProxy.deleteAsset(self.oap[self.iap.name()].id())
    b.dbProxy.deleteThreatType(0)
    b.dbProxy.deleteAttacker(self.oAttackers[self.iatk.name()].id())
    b.dbProxy.deleteDocumentReference(self.odrs[self.idr1.name()].id())
    b.dbProxy.deleteDocumentReference(self.odrs[self.idr2.name()].id())
    b.dbProxy.deleteExternalDocument(self.oecs[self.iec1.name()].id())
    b.dbProxy.deleteExternalDocument(self.oecs[self.iec2.name()].id())
    b.dbProxy.deletePersona(self.opp[self.ipp.name()].id())
    b.dbProxy.deleteRole(self.oRoles[self.irp.name()].id())
    b.dbProxy.deleteEnvironment(self.oenvs[self.iep.name()].id())
    b.dbProxy.close()

if __name__ == '__main__':
  unittest.main()
