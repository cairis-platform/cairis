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
from cairis.core.RoleParameters import RoleParameters
from cairis.core.EnvironmentParameters import EnvironmentParameters
from cairis.core.PersonaParameters import PersonaParameters
from cairis.core.PersonaEnvironmentProperties import PersonaEnvironmentProperties
from cairis.core.ExternalDocumentParameters import ExternalDocumentParameters
from cairis.core.DocumentReferenceParameters import DocumentReferenceParameters
from cairis.core.PersonaCharacteristicParameters import PersonaCharacteristicParameters

__author__ = 'Shamal Faily'


class PersonaTest(unittest.TestCase):

  def setUp(self):
    call([os.environ['CAIRIS_CFG_DIR'] + "/initdb.sh"])
    cairis.core.BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/personas.json')
    d = json.load(f)
    f.close()
    iEnvironments = d['environments']
    iep1 = EnvironmentParameters(iEnvironments[0]["theName"],iEnvironments[0]["theShortCode"],iEnvironments[0]["theDescription"])
    b = Borg()
    b.dbProxy.addEnvironment(iep1)

    iRoles = d['roles']
    irp = RoleParameters(iRoles[0]["theName"], iRoles[0]["theType"], iRoles[0]["theShortCode"], iRoles[0]["theDescription"],[])
    b.dbProxy.addRole(irp)
    self.iPersonas = d['personas']
    self.iExternalDocuments = d['external_documents']
    self.iDocumentReferences = d['document_references']
    self.iPersonaCharacteristics = d['persona_characteristics']
    

  def testPersona(self):
    ipp = PersonaParameters(self.iPersonas[0]["theName"],self.iPersonas[0]["theActivities"],self.iPersonas[0]["theAttitudes"],self.iPersonas[0]["theAptitudes"],self.iPersonas[0]["theMotivations"],self.iPersonas[0]["theSkills"],self.iPersonas[0]["theIntrinsic"],self.iPersonas[0]["theContextual"],"","0",self.iPersonas[0]["thePersonaType"],[],[PersonaEnvironmentProperties(self.iPersonas[0]["theEnvironmentProperties"][0]["theName"],(self.iPersonas[0]["theEnvironmentProperties"][0]["theDirectFlag"] == "True"),self.iPersonas[0]["theEnvironmentProperties"][0]["theNarrative"],self.iPersonas[0]["theEnvironmentProperties"][0]["theRole"])],[])
    b = Borg()
    b.dbProxy.addPersona(ipp) 

    thePersonas = b.dbProxy.getPersonas()
    op = thePersonas[self.iPersonas[0]["theName"]]
    self.assertEqual(ipp.name(),op.name())
    self.assertEqual(ipp.activities(),op.activities())
    self.assertEqual(ipp.attitudes(),op.attitudes())
    self.assertEqual(ipp.aptitudes(),op.aptitudes())
    self.assertEqual(ipp.motivations(),op.motivations())
    self.assertEqual(ipp.skills(),op.skills())
    self.assertEqual(ipp.intrinsic(),op.intrinsic())
    self.assertEqual(ipp.contextual(),op.contextual())
    self.assertEqual(op.roles('Psychosis','')[0],'Researcher')
    self.assertEqual('Researcher' in op.roles('Psychosis','override'),True)
    self.assertEqual(op.directFlag('Psychosis',''),'False')
    self.assertEqual(op.directFlag('Psychosis','override'),'False')
    self.assertEqual(op.narrative('Psychosis',''),'Nothing stipulated')
    self.assertEqual(op.narrative('Psychosis','override'),'Nothing stipulated')
    
    self.assertEqual(self.iPersonas[0]["theEnvironmentProperties"][0]["theDirectFlag"],op.environmentProperties()[0].directFlag())
    self.assertEqual(self.iPersonas[0]["theEnvironmentProperties"][0]["theNarrative"],op.environmentProperties()[0].narrative())
    self.assertEqual(self.iPersonas[0]["theEnvironmentProperties"][0]["theRole"],op.environmentProperties()[0].roles())

    iec1 = ExternalDocumentParameters(self.iExternalDocuments[0]["theName"],self.iExternalDocuments[0]["theVersion"],self.iExternalDocuments[0]["thePublicationDate"],self.iExternalDocuments[0]["theAuthors"],self.iExternalDocuments[0]["theDescription"])
    iec2 = ExternalDocumentParameters(self.iExternalDocuments[1]["theName"],self.iExternalDocuments[1]["theVersion"],self.iExternalDocuments[1]["thePublicationDate"],self.iExternalDocuments[1]["theAuthors"],self.iExternalDocuments[1]["theDescription"])
    b.dbProxy.addExternalDocument(iec1)
    b.dbProxy.addExternalDocument(iec2)
    oecs = b.dbProxy.getExternalDocuments()
    oec1 = oecs[self.iExternalDocuments[0]["theName"]]
    oec2 = oecs[self.iExternalDocuments[1]["theName"]]

    self.assertEqual(self.iExternalDocuments[0]["theName"],oec1.name())
    self.assertEqual(self.iExternalDocuments[0]["theVersion"],oec1.version())
    self.assertEqual(self.iExternalDocuments[0]["thePublicationDate"],oec1.date())
    self.assertEqual(self.iExternalDocuments[0]["theAuthors"],oec1.authors())
    self.assertEqual(self.iExternalDocuments[0]["theDescription"],oec1.description())
    self.assertEqual(self.iExternalDocuments[1]["theName"],oec2.name())
    self.assertEqual(self.iExternalDocuments[1]["theVersion"],oec2.version())
    self.assertEqual(self.iExternalDocuments[1]["thePublicationDate"],oec2.date())
    self.assertEqual(self.iExternalDocuments[1]["theAuthors"],oec2.authors())
    self.assertEqual(self.iExternalDocuments[1]["theDescription"],oec2.description())

    idr1 = DocumentReferenceParameters(self.iDocumentReferences[0]["theName"],self.iDocumentReferences[0]["theDocName"],self.iDocumentReferences[0]["theContributor"],self.iDocumentReferences[0]["theExcerpt"])
    idr2 = DocumentReferenceParameters(self.iDocumentReferences[1]["theName"],self.iDocumentReferences[1]["theDocName"],self.iDocumentReferences[1]["theContributor"],self.iDocumentReferences[1]["theExcerpt"])
    idr3 = DocumentReferenceParameters(self.iDocumentReferences[2]["theName"],self.iDocumentReferences[2]["theDocName"],self.iDocumentReferences[2]["theContributor"],self.iDocumentReferences[2]["theExcerpt"])
    
    b.dbProxy.addDocumentReference(idr1)
    b.dbProxy.addDocumentReference(idr2)
    b.dbProxy.addDocumentReference(idr3)

    odrs = b.dbProxy.getDocumentReferences()
    odr1 = odrs[self.iDocumentReferences[0]["theName"]]
    odr2 = odrs[self.iDocumentReferences[1]["theName"]]
    odr3 = odrs[self.iDocumentReferences[2]["theName"]]

    self.assertEqual(self.iDocumentReferences[0]["theName"],odr1.name())
    self.assertEqual(self.iDocumentReferences[0]["theDocName"],odr1.document())
    self.assertEqual(self.iDocumentReferences[0]["theContributor"],odr1.contributor())
    self.assertEqual(self.iDocumentReferences[0]["theExcerpt"],odr1.excerpt())
    self.assertEqual(self.iDocumentReferences[1]["theName"],odr2.name())
    self.assertEqual(self.iDocumentReferences[1]["theDocName"],odr2.document())
    self.assertEqual(self.iDocumentReferences[1]["theContributor"],odr2.contributor())
    self.assertEqual(self.iDocumentReferences[1]["theExcerpt"],odr2.excerpt())
    self.assertEqual(self.iDocumentReferences[2]["theName"],odr3.name())
    self.assertEqual(self.iDocumentReferences[2]["theDocName"],odr3.document())
    self.assertEqual(self.iDocumentReferences[2]["theContributor"],odr3.contributor())
    self.assertEqual(self.iDocumentReferences[2]["theExcerpt"],odr3.excerpt())

    ipc1 = PersonaCharacteristicParameters(self.iPersonaCharacteristics[0]["thePersonaName"],self.iPersonaCharacteristics[0]["theModQual"],self.iPersonaCharacteristics[0]["theVariable"],self.iPersonaCharacteristics[0]["theCharacteristic"],[(self.iPersonaCharacteristics[0]["ground"],'','document')],[(self.iPersonaCharacteristics[0]["warrant"],'','document')],[],[(self.iPersonaCharacteristics[0]["rebuttal"],'','document')])

    b.dbProxy.addPersonaCharacteristic(ipc1)
    opcs = b.dbProxy.getPersonaCharacteristics()
    opc1 = opcs[self.iPersonaCharacteristics[0]["thePersonaName"] + '/' + self.iPersonaCharacteristics[0]["theVariable"] + '/' + self.iPersonaCharacteristics[0]["theCharacteristic"]]

    self.assertEqual(self.iPersonaCharacteristics[0]["thePersonaName"],opc1.persona())
    self.assertEqual(self.iPersonaCharacteristics[0]["theModQual"],opc1.qualifier())
    self.assertEqual(self.iPersonaCharacteristics[0]["theVariable"],opc1.behaviouralVariable())
    self.assertEqual(self.iPersonaCharacteristics[0]["theCharacteristic"],opc1.characteristic())
    self.assertEqual(self.iPersonaCharacteristics[0]["ground"],opc1.grounds()[0][0])
    self.assertEqual(self.iPersonaCharacteristics[0]["warrant"],opc1.warrant()[0][0])
    self.assertEqual(self.iPersonaCharacteristics[0]["rebuttal"],opc1.rebuttal()[0][0])

    cGrounds = b.dbProxy.getGrounds(opc1.grounds()[0][0])
    self.assertEqual(opc1.grounds()[0][1],cGrounds[2])

    cWarrant = b.dbProxy.getWarrant(opc1.warrant()[0][0])
    self.assertEqual(opc1.warrant()[0][1],cWarrant[2])

    cRebuttal = b.dbProxy.getRebuttal(opc1.rebuttal()[0][0])
    self.assertEqual(opc1.rebuttal()[0][1],cRebuttal[2])


    ipp2 = PersonaParameters('Changed name',self.iPersonas[0]["theActivities"],self.iPersonas[0]["theAttitudes"],self.iPersonas[0]["theAptitudes"],self.iPersonas[0]["theMotivations"],self.iPersonas[0]["theSkills"],self.iPersonas[0]["theIntrinsic"],self.iPersonas[0]["theContextual"],"","0",self.iPersonas[0]["thePersonaType"],[],[PersonaEnvironmentProperties(self.iPersonas[0]["theEnvironmentProperties"][0]["theName"],(self.iPersonas[0]["theEnvironmentProperties"][0]["theDirectFlag"] == "True"),self.iPersonas[0]["theEnvironmentProperties"][0]["theNarrative"],self.iPersonas[0]["theEnvironmentProperties"][0]["theRole"])],[])

    ipp2.setId(op.id())
    b.dbProxy.updatePersona(ipp2) 
    theUpdatedPersonas = b.dbProxy.getPersonas()
    op2 = theUpdatedPersonas['Changed name']
    self.assertEqual(ipp2.name(),op2.name())

    b.dbProxy.deletePersonaCharacteristic(opc1.id())
    b.dbProxy.deleteDocumentReference(odr1.id())
    b.dbProxy.deleteDocumentReference(odr2.id())
    b.dbProxy.deleteDocumentReference(odr3.id())
    b.dbProxy.deleteExternalDocument(oec1.id())
    b.dbProxy.deleteExternalDocument(oec2.id())
    b.dbProxy.deletePersona(op.id())

  def tearDown(self):
    pass

if __name__ == '__main__':
  unittest.main()
