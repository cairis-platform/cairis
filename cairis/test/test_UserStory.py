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
from cairis.core.ReferenceSynopsis import ReferenceSynopsis
from cairis.core.UserStory import UserStory

__author__ = 'Shamal Faily'


class UserStoryTest(unittest.TestCase):

  def setUp(self):
    call([os.environ['CAIRIS_CFG_DIR'] + "/initdb.sh"])
    cairis.core.BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/userstories.json')
    d = json.load(f)
    f.close()
    self.iEnvironments = d['environments']
    iep1 = EnvironmentParameters(self.iEnvironments[0]["theName"],self.iEnvironments[0]["theShortCode"],self.iEnvironments[0]["theDescription"])
    b = Borg()
    b.dbProxy.addEnvironment(iep1)
    iRoles = d['roles']
    irp = RoleParameters(iRoles[0]["theName"], iRoles[0]["theType"], iRoles[0]["theShortCode"], iRoles[0]["theDescription"],[])
    b.dbProxy.addRole(irp)
    
    iPersonas = d['personas']
    ipp = PersonaParameters(iPersonas[0]["theName"],iPersonas[0]["theActivities"],iPersonas[0]["theAttitudes"],iPersonas[0]["theAptitudes"],iPersonas[0]["theMotivations"],iPersonas[0]["theSkills"],iPersonas[0]["theIntrinsic"],iPersonas[0]["theContextual"],"","0",iPersonas[0]["thePersonaType"],[],[PersonaEnvironmentProperties(iPersonas[0]["theEnvironmentProperties"][0]["theName"],(iPersonas[0]["theEnvironmentProperties"][0]["theDirectFlag"] == "True"),iPersonas[0]["theEnvironmentProperties"][0]["theNarrative"],iPersonas[0]["theEnvironmentProperties"][0]["theRole"])],[])
    b.dbProxy.addPersona(ipp)

    edData = d['external_documents'][0]
    ied = ExternalDocumentParameters(edData['theName'],edData['theVersion'],edData['thePublicationDate'],edData['theAuthors'],edData['theDescription'])
    b.dbProxy.addExternalDocument(ied)

    drData = d['document_references'][0]
    idr = DocumentReferenceParameters(drData['theName'],drData['theDocName'],drData['theContributor'],drData['theExcerpt'])
    b.dbProxy.addDocumentReference(idr)

    ugData = d['user_goals'][0]
    iug = ReferenceSynopsis(-1,ugData['theReference'],ugData['theSynopsis'],ugData['theDimension'],'persona',ugData['thePersona'],ugData['theInitialSatisfaction'])
    b.dbProxy.addUserGoal(iug)

    self.iUserStories = d['user_stories']


  def testUserStory(self):
    usName = self.iUserStories[0]['theName']
    usAuth = self.iUserStories[0]['theAuthor']
    usRole = self.iUserStories[0]['theRole']
    usDesc = self.iUserStories[0]['theDescription']
    ugName = self.iUserStories[0]['theUserGoal']
    ugAc = self.iUserStories[0]['theAcceptanceCriteria']
    ugTags = self.iUserStories[0]['theTags']
    ius = UserStory(-1,usName,usAuth,usRole,usDesc,ugName,ugAc,ugTags)
    b = Borg()
    b.dbProxy.addUserStory(ius) 

    theUserStories = b.dbProxy.getUserStories()
    ous = theUserStories[0]
    self.assertEqual(ius.name(),ous.name())
    self.assertEqual(ius.author(),ous.author())
    self.assertEqual(ius.role(),ous.role())
    self.assertEqual(ius.description(),ous.description())
    self.assertEqual(ius.userGoal(),ous.userGoal())
    self.assertEqual(ius.acceptanceCriteria(),ous.acceptanceCriteria())
    self.assertEqual(ius.tags(),ous.tags())

    ius.theName = 'Updated name'
    ius.theId = ous.id()
    b.dbProxy.updateUserStory(ius) 
    theUserStories = b.dbProxy.getUserStories()
    ous = theUserStories[0]
    self.assertEqual(ius.name(),ous.name())
    self.assertEqual(ius.author(),ous.author())
    self.assertEqual(ius.role(),ous.role())
    self.assertEqual(ius.description(),ous.description())
    self.assertEqual(ius.userGoal(),ous.userGoal())
    self.assertEqual(ius.acceptanceCriteria(),ous.acceptanceCriteria())
    self.assertEqual(ius.tags(),ous.tags())
    b.dbProxy.deleteUserStory(ous.id())

  def tearDown(self):
    pass

if __name__ == '__main__':
  unittest.main()
