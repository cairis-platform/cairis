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
from cairis.core.TemplateAssetParameters import TemplateAssetParameters
from cairis.core.TemplateGoalParameters import TemplateGoalParameters
from cairis.core.ValueTypeParameters import ValueTypeParameters

__author__ = 'Shamal Faily'


class TemplateGoalTest(unittest.TestCase):

  def setUp(self):
    call([os.environ['CAIRIS_CFG_DIR'] + "/initdb.sh"])
    cairis.core.BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/templategoals.json')
    d = json.load(f)
    f.close()
    iAccessRights = d['access_rights']
    iar1 = ValueTypeParameters(iAccessRights[0]["theName"], iAccessRights[0]["theDescription"], 'access_right','',iAccessRights[0]["theValue"],iAccessRights[0]["theRationale"])
    iSurfaceTypes = d['surface_type']
    ist1 = ValueTypeParameters(iSurfaceTypes[0]["theName"], iSurfaceTypes[0]["theDescription"], 'surface_type','',iSurfaceTypes[0]["theValue"],iSurfaceTypes[0]["theRationale"])
    b = Borg()
    b.dbProxy.addValueType(iar1)
    b.dbProxy.addValueType(ist1)
    iTemplateAssets = d['template_assets']
    spValues = [0,0,0,0,0,0,0,0]
    srValues = ['None','None','None','None','None','None','None','None']
    iTap = TemplateAssetParameters(iTemplateAssets[0]["theName"], iTemplateAssets[0]["theShortCode"], iTemplateAssets[0]["theDescription"], iTemplateAssets[0]["theSignificance"],iTemplateAssets[0]["theType"],iTemplateAssets[0]["theSurfaceType"],iTemplateAssets[0]["theAccessRight"],spValues,srValues,[],[])
    b.dbProxy.addTemplateAsset(iTap)
    self.iTemplateGoals = d['template_goals']

  def testTemplateGoal(self):
    b = Borg()
    iTag1 = TemplateGoalParameters(self.iTemplateGoals[0]["theName"],self.iTemplateGoals[0]["theDefinition"],self.iTemplateGoals[0]["theRationale"],self.iTemplateGoals[0]["theConcerns"],self.iTemplateGoals[0]["theResponsibilities"])
    iTag2 = TemplateGoalParameters(self.iTemplateGoals[1]["theName"],self.iTemplateGoals[1]["theDefinition"],self.iTemplateGoals[1]["theRationale"],self.iTemplateGoals[1]["theConcerns"],self.iTemplateGoals[1]["theResponsibilities"])
    b.dbProxy.addTemplateGoal(iTag1)
    b.dbProxy.addTemplateGoal(iTag2)

    oTags = b.dbProxy.getTemplateGoals()
    oTag1 = oTags[self.iTemplateGoals[0]["theName"]]
    oTag2 = oTags[self.iTemplateGoals[1]["theName"]]

    self.assertEqual(iTag1.name(), oTag1.name())
    self.assertEqual(iTag1.definition(), oTag1.definition())
    self.assertEqual(iTag1.rationale(),oTag1.rationale())
    self.assertEqual(iTag1.concerns(),oTag1.concerns())
    self.assertEqual(iTag1.responsibilities(),oTag1.responsibilities())

    self.assertEqual(iTag2.name(), oTag2.name())
    self.assertEqual(iTag2.definition(), oTag2.definition())
    self.assertEqual(iTag2.rationale(),oTag2.rationale())
    self.assertEqual(iTag2.concerns(),oTag2.concerns())
    self.assertEqual(iTag2.responsibilities(),oTag2.responsibilities())

    iTag1.theDefinition = 'updated definition'
    iTag1.setId(oTag1.id())
    b.dbProxy.updateTemplateGoal(iTag1)

    oTags = b.dbProxy.getTemplateGoals()
    oTag1 = oTags[self.iTemplateGoals[0]["theName"]]
    self.assertEqual(iTag1.definition(), oTag1.definition())


    b.dbProxy.deleteTemplateGoal(oTag1.id())
    b.dbProxy.deleteTemplateGoal(oTag2.id())
  
  def tearDown(self):
    pass

if __name__ == '__main__':
  unittest.main()
