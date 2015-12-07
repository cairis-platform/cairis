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
from RoleParameters import RoleParameters
from EnvironmentParameters import EnvironmentParameters
from PersonaParameters import PersonaParameters
from PersonaEnvironmentProperties import PersonaEnvironmentProperties

class PersonaTest(unittest.TestCase):

  def setUp(self):
    BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/personas.json')
    d = json.load(f)
    f.close()
    self.iEnvironments = d['environments']
    iep1 = EnvironmentParameters(self.iEnvironments[0]["theName"],self.iEnvironments[0]["theShortCode"],self.iEnvironments[0]["theDescription"])
    b = Borg()
    b.dbProxy.addEnvironment(iep1)
    self.theEnvironments = b.dbProxy.getEnvironments()

    self.iRoles = d['roles']
    irp = RoleParameters(self.iRoles[0]["theName"], self.iRoles[0]["theType"], self.iRoles[0]["theShortCode"], self.iRoles[0]["theDescription"],[])
    b.dbProxy.addRole(irp)
    self.theRoles = b.dbProxy.getRoles()
    self.iPersonas = d['personas']
    self.iExternalDocuments = d['external_documents']
    self.iDocumentReferences = d['document_references']
    self.iPersonaCharacteristics = d['persona_characteristics']
    

  def testPersona(self):
    ipp = PersonaParameters(self.iPersonas[0]["theName"],self.iPersonas[0]["theActivities"],self.iPersonas[0]["theAttitudes"],self.iPersonas[0]["theAptitudes"],self.iPersonas[0]["theMotivations"],self.iPersonas[0]["theSkills"],self.iPersonas[0]["theIntrinsic"],self.iPersonas[0]["theContextual"],"","0",self.iPersonas[0]["thePersonaType"],[],[PersonaEnvironmentProperties(self.iPersonas[0]["theEnvironmentProperties"][0]["theName"],self.iPersonas[0]["theEnvironmentProperties"][0]["theDirectFlag"],self.iPersonas[0]["theEnvironmentProperties"][0]["theNarrative"],self.iPersonas[0]["theEnvironmentProperties"][0]["theRole"])],[])
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


    b.dbProxy.deletePersona(op.id())

  def tearDown(self):
    b = Borg()
    b.dbProxy.deleteRole(self.theRoles[self.iRoles[0]["theName"]].id())
    b.dbProxy.deleteEnvironment(self.theEnvironments[self.iEnvironments[0]["theName"]].id())
    b.dbProxy.close()

if __name__ == '__main__':
  unittest.main()
