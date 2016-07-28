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
from cairis.core.ValueTypeParameters import ValueTypeParameters

__author__ = 'Shamal Faily'


class TemplateAssetTest(unittest.TestCase):

  def setUp(self):
    call([os.environ['CAIRIS_SRC'] + "/test/initdb.sh"])
    cairis.core.BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/templateassets.json')
    d = json.load(f)
    f.close()
    self.iAccessRights = d['access_rights']
    iar1 = ValueTypeParameters(self.iAccessRights[0]["theName"], self.iAccessRights[0]["theDescription"], 'access_right','',self.iAccessRights[0]["theValue"],self.iAccessRights[0]["theRationale"])
    self.iSurfaceTypes = d['surface_type']
    ist1 = ValueTypeParameters(self.iSurfaceTypes[0]["theName"], self.iSurfaceTypes[0]["theDescription"], 'surface_type','',self.iSurfaceTypes[0]["theValue"],self.iSurfaceTypes[0]["theRationale"])
    b = Borg()
    b.dbProxy.addValueType(iar1)
    b.dbProxy.addValueType(ist1)
    self.iTemplateAssets = d['template_assets']

  def testTemplateAsset(self):
    spValues = [(0,'None'),(0,'None'),(0,'None'),(0,'None'),(0,'None'),(0,'None'),(0,'None'),(0,'None')]
    iTap = TemplateAssetParameters(self.iTemplateAssets[0]["theName"], self.iTemplateAssets[0]["theShortCode"], self.iTemplateAssets[0]["theDescription"], self.iTemplateAssets[0]["theSignificance"],self.iTemplateAssets[0]["theType"],self.iTemplateAssets[0]["theSurfaceType"],self.iTemplateAssets[0]["theAccessRight"],spValues,[],[])
    b = Borg()
    b.dbProxy.addTemplateAsset(iTap)
    oTaps = b.dbProxy.getTemplateAssets()
    oTap = oTaps[self.iTemplateAssets[0]["theName"]]
    self.assertEqual(iTap.name(), oTap.name())
    self.assertEqual(iTap.properties(), oTap.properties())
    self.assertEqual(iTap.shortCode(),oTap.shortCode())
    self.assertEqual(iTap.description(),oTap.description())
    self.assertEqual(iTap.type(),oTap.type())
    self.assertEqual(iTap.surfaceType(),oTap.surfaceType())
    self.assertEqual(iTap.accessRight(),oTap.accessRight())

    b.dbProxy.deleteTemplateAsset(oTap.id())
  
  def tearDown(self):
    b = Borg()
    b.dbProxy.close()
    call([os.environ['CAIRIS_SRC'] + "/test/dropdb.sh"])

if __name__ == '__main__':
  unittest.main()
