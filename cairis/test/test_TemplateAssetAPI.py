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

import logging
import json
import sys
if (sys.version_info > (3,)):
  from urllib.parse import quote
else:
  from urllib import quote
from io import StringIO
import os
import jsonpickle
import cairis.core.BorgFactory
from cairis.core.Borg import Borg
from cairis.core.TemplateAsset import TemplateAsset
from cairis.core.ValueTypeParameters import ValueTypeParameters
from cairis.core.TemplateAssetParameters import TemplateAssetParameters
from cairis.core.TemplateAssetParameters import TemplateAssetParameters
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
from cairis.mio.ModelImport import importModelFile
from cairis.tools.JsonConverter import json_deserialize

__author__ = 'Shamal Faily'

def addTestData():
  f = open(os.environ['CAIRIS_SRC'] + '/test/templateassets.json')
  d = json.load(f)
  f.close()
  iAccessRights = d['access_rights']
  iSurfaceTypes = d['surface_type']
  iTemplateAssets = d['template_assets']
  iPrivileges = d['privileges']
  cairis.core.BorgFactory.initialise()
  b = Borg()
  iar1 = ValueTypeParameters(iAccessRights[0]["theName"], iAccessRights[0]["theDescription"], 'access_right','',iAccessRights[0]["theValue"],iAccessRights[0]["theRationale"])
  iar2 = ValueTypeParameters(iAccessRights[1]["theName"], iAccessRights[1]["theDescription"], 'access_right','',iAccessRights[1]["theValue"],iAccessRights[1]["theRationale"])
  ist1 = ValueTypeParameters(iSurfaceTypes[0]["theName"], iSurfaceTypes[0]["theDescription"], 'surface_type','',iSurfaceTypes[0]["theValue"],iSurfaceTypes[0]["theRationale"])
  ipr1 = ValueTypeParameters(iPrivileges[0]["theName"], iPrivileges[0]["theDescription"], 'privilege','',iPrivileges[0]["theValue"],iPrivileges[0]["theRationale"])
  b.dbProxy.addValueType(iar1)
  b.dbProxy.addValueType(iar2)
  b.dbProxy.addValueType(ist1)
  b.dbProxy.addValueType(ipr1)
  spValues = [0,0,0,0,0,0,0,0]
  srValues = ['None','None','None','None','None','None','None','None']
  ifs = iTemplateAssets[0]
  iTap = TemplateAssetParameters(iTemplateAssets[0]["theName"], iTemplateAssets[0]["theShortCode"], iTemplateAssets[0]["theDescription"], iTemplateAssets[0]["theSignificance"],iTemplateAssets[0]["theType"],iTemplateAssets[0]["theSurfaceType"],iTemplateAssets[0]["theAccessRight"],spValues,srValues,[],[('anInterface','provided','trusted','privileged')])
  b.dbProxy.addTemplateAsset(iTap)

class TemplateAssetAPITests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/ACME_Water/ACME_Water.xml',1,'test')
    addTestData() 

  def setUp(self):
    self.logger = logging.getLogger(__name__)
    f = open(os.environ['CAIRIS_SRC'] + '/test/templateassets.json')
    d = json.load(f)
    f.close()
    iTemplateAssets = d['template_assets']
    self.new_ta = d['template_assets'][1]
    self.new_ta_dict = {
      'session_id' : 'test',
      'object': self.new_ta
    }
    self.existing_ta_name = 'Application Data'
    self.upd_ta = d['template_assets'][0]
    self.upd_ta_dict = {
      'session_id' : 'test',
      'object': self.new_ta
    }
    self.existing_ta_name = 'Application Data'

  def test_get_all(self):
    method = 'test_get'
    url = '/api/template_assets?session_id=test'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    tas = jsonpickle.decode(responseData)
    self.assertIsNotNone(tas, 'No results after deserialization')
    self.assertIsInstance(tas, list, 'The result is not a list as expected')
    self.assertGreater(len(tas), 0, 'No template assets in the list')
    self.logger.info('[%s] Template assets found: %d', method, len(tas))
    ta = tas[0]
    self.logger.info('[%s] First template asset: %s \n', method, ta['theName'])

  def test_get_by_name(self):
    method = 'test_get_by_name'
    url = '/api/template_assets/name/%s?session_id=test' % quote(self.existing_ta_name)
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    ta = jsonpickle.decode(responseData)
    self.assertIsNotNone(ta, 'No results after deserialization')
    self.logger.info('[%s] Template asset: %s \n', method, ta['theName'])

  def test_post(self):
    method = 'test_post_new'
    rv = self.app.post('/api/template_assets', content_type='application/json', data=jsonpickle.encode(self.new_ta_dict))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertGreater(ackMsg.find('created'), -1, 'Template asset not created')

  def test_put(self):
    method = 'test_put'
    self.upd_ta_dict['object']['theName'] = self.existing_ta_name
    self.upd_ta_dict['object']['theDescription'] = 'Updated description'
    url = '/api/template_assets/name/%s?session_id=test' % quote(self.existing_ta_name)
    rv = self.app.put(url, content_type='application/json', data=jsonpickle.encode(self.upd_ta_dict))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertGreater(ackMsg.find('updated'), -1, 'Template asset not updated')

  def test_delete(self):
    method = 'test_delete'

    rv = self.app.post('/api/template_assets', content_type='application/json', data=jsonpickle.encode(self.new_ta_dict))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)

    url = '/api/template_assets/name/%s?session_id=test' % quote(self.new_ta['theName'])
    rv = self.app.delete(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertGreater(ackMsg.find('deleted'), -1, 'Template asset not deleted')
