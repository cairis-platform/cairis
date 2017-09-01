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
from cairis.core.TemplateRequirementParameters import TemplateRequirementParameters
from cairis.core.ValueTypeParameters import ValueTypeParameters

__author__ = 'Shamal Faily'


class TemplateRequirementTest(unittest.TestCase):

  def setUp(self):
    call([os.environ['CAIRIS_CFG_DIR'] + "/initdb.sh"])
    cairis.core.BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/templaterequirements.json')
    d = json.load(f)
    f.close()
    iAccessRights = d['access_rights']
    iar1 = ValueTypeParameters(iAccessRights[0]["theName"], iAccessRights[0]["theDescription"], 'access_right','',iAccessRights[0]["theValue"],iAccessRights[0]["theRationale"])
    iSurfaceTypes = d['surface_types']
    ist1 = ValueTypeParameters(iSurfaceTypes[0]["theName"], iSurfaceTypes[0]["theDescription"], 'surface_type','',iSurfaceTypes[0]["theValue"],iSurfaceTypes[0]["theRationale"])
    b = Borg()
    b.dbProxy.addValueType(iar1)
    b.dbProxy.addValueType(ist1)
    iTemplateAssets = d['template_assets']
    spValues = [0,0,0,0,0,0,0,0]
    srValues = ['None','None','None','None','None','None','None','None']
    iTap = TemplateAssetParameters(iTemplateAssets[0]["theName"], iTemplateAssets[0]["theShortCode"], iTemplateAssets[0]["theDescription"], iTemplateAssets[0]["theSignificance"],iTemplateAssets[0]["theType"],iTemplateAssets[0]["theSurfaceType"],iTemplateAssets[0]["theAccessRight"],spValues,srValues,[],[])
    b.dbProxy.addTemplateAsset(iTap)
    self.iTemplateReqs = d["template_requirements"]

  def testTemplateRequirement(self):
    b = Borg()
    iTar = TemplateRequirementParameters(self.iTemplateReqs[0]["theName"],self.iTemplateReqs[0]["theAsset"],self.iTemplateReqs[0]["theType"],self.iTemplateReqs[0]["theDescription"],self.iTemplateReqs[0]["theRationale"],self.iTemplateReqs[0]["theFitCriterion"])
    b.dbProxy.addTemplateRequirement(iTar)

    oTars = b.dbProxy.getTemplateRequirements()
    oTar = oTars[self.iTemplateReqs[0]["theName"]]

    self.assertEqual(iTar.name(), oTar.name())
    self.assertEqual(iTar.asset(), oTar.asset())
    self.assertEqual(iTar.type(), oTar.type())
    self.assertEqual(iTar.description(), oTar.description())
    self.assertEqual(iTar.rationale(), oTar.rationale())
    self.assertEqual(iTar.fitCriterion(), oTar.fitCriterion())

    iTar.theName = 'Updated name'
    iTar.setId(oTar.id())
    b.dbProxy.updateTemplateRequirement(iTar)
    oTars = b.dbProxy.getTemplateRequirements()
    oTar = oTars['Updated name']
    self.assertEqual(oTar.name(),'Updated name')

    b.dbProxy.deleteTemplateRequirement(oTar.id())
  
  def tearDown(self):
    pass

if __name__ == '__main__':
  unittest.main()
