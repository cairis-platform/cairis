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
from cairis.core.InternalDocumentParameters import InternalDocumentParameters
from cairis.core.CodeParameters import CodeParameters
from cairis.core.RoleParameters import RoleParameters
from cairis.core.EnvironmentParameters import EnvironmentParameters
from cairis.core.PersonaParameters import PersonaParameters
from cairis.core.PersonaEnvironmentProperties import PersonaEnvironmentProperties
from cairis.core.ImpliedCharacteristicParameters import ImpliedCharacteristicParameters
import sys

class ImpliedCharacteristicTest(unittest.TestCase):

  def setUp(self):
    call([os.environ['CAIRIS_CFG_DIR'] + "/initdb.sh"])
    cairis.core.BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/processes.json')
    d = json.load(f)
    f.close()

    b = Borg()
    iIntDocs = d['internaldocuments']
    i = InternalDocumentParameters(iIntDocs[0]["theName"],iIntDocs[0]["theDescription"], iIntDocs[0]["theContent"], [],[])
    b.dbProxy.addInternalDocument(i)

    iCodes = d['codes']
    i = CodeParameters(iCodes[0]["theName"], iCodes[0]["theType"],iCodes[0]["theDescription"], iCodes[0]["theInclusionCriteria"], iCodes[0]["theExample"])
    b.dbProxy.addCode(i)
    i = CodeParameters(iCodes[1]["theName"], iCodes[1]["theType"],iCodes[1]["theDescription"], iCodes[1]["theInclusionCriteria"], iCodes[1]["theExample"])
    b.dbProxy.addCode(i)
    iQs = d['quotations']
    i = (iQs[0]["theType"],iQs[0]["theCode"],iQs[0]["theArtifactType"],iQs[0]["theArtifactName"],iQs[0]["theEnvironment"],iQs[0]["theSection"],iQs[0]["theStartIdx"],iQs[0]["theEndIdx"],iQs[0]["theLabel"],iQs[0]["theSynopsis"])
    b.dbProxy.addQuotation(i)
    i = (iQs[2]['theType'],iQs[2]["theCode"],iQs[2]["theArtifactType"],iQs[2]["theArtifactName"],iQs[2]["theEnvironment"],iQs[2]["theSection"],iQs[2]["theStartIdx"],iQs[2]["theEndIdx"],iQs[2]["theLabel"],iQs[2]["theSynopsis"])
    b.dbProxy.addQuotation(i)
    iEnvironments = d['environments']
    iep1 = EnvironmentParameters(iEnvironments[0]["theName"],iEnvironments[0]["theShortCode"],iEnvironments[0]["theDescription"])
    b.dbProxy.addEnvironment(iep1)
    iRoles = d['roles']
    irp = RoleParameters(iRoles[0]["theName"], iRoles[0]["theType"], iRoles[0]["theShortCode"], iRoles[0]["theDescription"],[])
    b.dbProxy.addRole(irp)
    iPersonas = d['personas']
    ipp = PersonaParameters(iPersonas[0]["theName"],iPersonas[0]["theActivities"],iPersonas[0]["theAttitudes"],iPersonas[0]["theAptitudes"],iPersonas[0]["theMotivations"],iPersonas[0]["theSkills"],iPersonas[0]["theIntrinsic"],iPersonas[0]["theContextual"],"","0",iPersonas[0]["thePersonaType"],[],[PersonaEnvironmentProperties(iPersonas[0]["theEnvironmentProperties"][0]["theName"],(iPersonas[0]["theEnvironmentProperties"][0]["theDirectFlag"] == "True"),iPersonas[0]["theEnvironmentProperties"][0]["theNarrative"],iPersonas[0]["theEnvironmentProperties"][0]["theRole"])],[])
    b.dbProxy.addPersona(ipp)
    self.iCN = d['code_networks']
    b.dbProxy.addCodeRelationship(self.iCN[0]["thePersonaName"],self.iCN[0]["theFromCode"],self.iCN[0]["theToCode"],self.iCN[0]["theRshipType"])
    

  def testAddUpdateImpliedCharacteristic(self):
    b = Borg()

    p = ImpliedCharacteristicParameters(self.iCN[0]["thePersonaName"],self.iCN[0]["theFromCode"],self.iCN[0]["theToCode"],self.iCN[0]["theRshipType"],self.iCN[0]["theImpliedCharacteristic"]["theName"],self.iCN[0]["theImpliedCharacteristic"]["theQualifier"],[(self.iCN[0]["theImpliedCharacteristic"]["theFromLabel"],self.iCN[0]["theImpliedCharacteristic"]["theFromReferenceType"])],[(self.iCN[0]["theImpliedCharacteristic"]["theToLabel"],self.iCN[0]["theImpliedCharacteristic"]["theToReferenceType"])],self.iCN[0]["theImpliedCharacteristic"]["theType"])
    b.dbProxy.addImpliedCharacteristic(p)
    b.dbProxy.addIntention((self.iCN[0]["theImpliedCharacteristic"]["theName"],"implied_characteristic",self.iCN[0]["theImpliedCharacteristic"]["theIntentionName"],self.iCN[0]["theImpliedCharacteristic"]["theIntentionType"]))
#    b.dbProxy.addContribution((self.iCN[0]["theImpliedCharacteristic"]["theName"],self.iCN[0]["theImpliedCharacteristic"]["theFromLabel"],self.iCN[0]["theImpliedCharacteristic"]["theFromLabelContribution"],self.iCN[0]["theImpliedCharacteristic"]["theFromLabelValue"]))
#    b.dbProxy.addContribution((self.iCN[0]["theImpliedCharacteristic"]["theName"],self.iCN[0]["theImpliedCharacteristicName"]["theToLabel"],self.iCN[0]["theImpliedCharacteristic"]["theToLabelContribution"],self.iCN[0]["theImpliedCharacteristic"]["theToLabelValue"]))

    p.setIntention(self.iCN[0]["theImpliedCharacteristic"]["theIntentionName"])
    p.setIntentionType(self.iCN[0]["theImpliedCharacteristic"]["theIntentionType"])
    o = b.dbProxy.impliedCharacteristic(self.iCN[0]["thePersonaName"],self.iCN[0]["theFromCode"],self.iCN[0]["theToCode"],self.iCN[0]["theRshipType"])
    self.assertEqual(self.iCN[0]["theImpliedCharacteristic"]["theName"], o[0])
    self.assertEqual(self.iCN[0]["theImpliedCharacteristic"]["theQualifier"], o[1])
    self.assertEqual(self.iCN[0]["theImpliedCharacteristic"]["theType"], o[2])

    b.dbProxy.updateImpliedCharacteristic(p)
    o = b.dbProxy.impliedCharacteristic(self.iCN[0]["thePersonaName"],self.iCN[0]["theFromCode"],self.iCN[0]["theToCode"],self.iCN[0]["theRshipType"])
    self.assertEqual(self.iCN[0]["theImpliedCharacteristic"]["theName"], o[0])
    self.assertEqual(self.iCN[0]["theImpliedCharacteristic"]["theQualifier"], o[1])
    self.assertEqual(self.iCN[0]["theImpliedCharacteristic"]["theType"], o[2])

  
  def tearDown(self):
    b = Borg()
    b.dbProxy.close()
    call([os.environ['CAIRIS_CFG_DIR'] + "/dropdb.sh"])

if __name__ == '__main__':
  unittest.main()
