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
from cairis.core.CodeParameters import CodeParameters
from cairis.core.RoleParameters import RoleParameters
from cairis.core.EnvironmentParameters import EnvironmentParameters
from cairis.core.PersonaParameters import PersonaParameters
from cairis.core.PersonaEnvironmentProperties import PersonaEnvironmentProperties
import sys

class CodeNetworkTest(unittest.TestCase):

  def setUp(self):
    call([os.environ['CAIRIS_CFG_DIR'] + "/initdb.sh"])
    cairis.core.BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/processes.json')
    d = json.load(f)
    f.close()
    iCodes = d['codes']
    i = CodeParameters(iCodes[0]["theName"], iCodes[0]["theType"],iCodes[0]["theDescription"], iCodes[0]["theInclusionCriteria"], iCodes[0]["theExample"])
    b = Borg()
    b.dbProxy.addCode(i)
    i = CodeParameters(iCodes[1]["theName"], iCodes[1]["theType"],iCodes[1]["theDescription"], iCodes[1]["theInclusionCriteria"], iCodes[1]["theExample"])
    b.dbProxy.addCode(i)
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
    

  def testAddUpdateCodeNetwork(self):
    b = Borg()
    b.dbProxy.addCodeRelationship(self.iCN[0]["thePersonaName"],self.iCN[0]["theFromCode"],self.iCN[0]["theToCode"],self.iCN[0]["theRshipType"])
    opn = b.dbProxy.personaCodeNetwork('Claire')
    o = opn[0]
    self.assertEqual(self.iCN[0]["theFromCode"], o[0])
    self.assertEqual('context', o[1])
    self.assertEqual(self.iCN[0]["theToCode"],o[2])
    self.assertEqual('context',o[3])
    self.assertEqual(self.iCN[0]["theRshipType"],o[4])

    updNet = [(self.iCN[0]["theFromCode"],self.iCN[0]["theToCode"],'conflict')]
    b.dbProxy.updateCodeNetwork('Claire',updNet)
    opn = b.dbProxy.personaCodeNetwork('Claire')
    self.assertEqual(len(opn),1)
    o = opn[0]
    self.assertEqual(self.iCN[0]["theFromCode"], o[0])
    self.assertEqual('context', o[1])
    self.assertEqual(self.iCN[0]["theToCode"],o[2])
    self.assertEqual('context',o[3])
    self.assertEqual('conflict',o[4])

    b.dbProxy.updateCodeNetwork('Claire',[])
    opn = b.dbProxy.personaCodeNetwork('Claire')
    self.assertEqual(len(opn),0)

  
  def tearDown(self):
    b = Borg()
    b.dbProxy.close()
    call([os.environ['CAIRIS_CFG_DIR'] + "/dropdb.sh"])

if __name__ == '__main__':
  unittest.main()
