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

class AttackerTest(unittest.TestCase):

  def setUp(self):
    BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/attackers.json')
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
    
  def testAttacker(self):
    iatkeps = [AttackerEnvironmentProperties(self.iAttackers[0]["theEnvironmentProperties"][0]["theName"],self.iAttackers[0]["theEnvironmentProperties"][0]["theRoles"],self.iAttackers[0]["theEnvironmentProperties"][0]["theMotives"],self.iAttackers[0]["theEnvironmentProperties"][0]["theCapabilities"])]
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
    self.assertEqual(str(iatkeps[0].motives()[0]), str(oatkeps[0].motives()[0]))
    self.assertEqual(str(iatkeps[0].capabilities()[0][0]), str(oatkeps[0].capabilities()[0][0]))
    self.assertEqual(str(iatkeps[0].capabilities()[0][1]), str(oatkeps[0].capabilities()[0][1]))

    b.dbProxy.deleteAttacker(o.id())
  
  def tearDown(self):
    b = Borg()
    
    b.dbProxy.deletePersonaCharacteristic(self.opcs[self.ipc1.pName()].id())
    b.dbProxy.deleteDocumentReference(self.odrs[self.idr1.name()].id())
    b.dbProxy.deleteDocumentReference(self.odrs[self.idr2.name()].id())
    b.dbProxy.deleteExternalDocument(self.oec[self.iec1.name()].id())
    b.dbProxy.deleteExternalDocument(self.oec[self.iec2.name()].id())
    b.dbProxy.deletePersona(self.opp[self.ipp.name()].id())
    b.dbProxy.deleteRole(self.oRoles[self.irp.name()].id())
    b.dbProxy.deleteEnvironment(self.oenvs[self.iep.name()].id())
    b.dbProxy.close()

if __name__ == '__main__':
  unittest.main()
