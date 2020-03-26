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
import sys
if (sys.version_info > (3,)):
  from urllib.parse import quote
else:
  from urllib import quote
import jsonpickle
from cairis.core.Asset import Asset
from cairis.core.ObjectSummary import ObjectSummary
from cairis.core.AssetEnvironmentProperties import AssetEnvironmentProperties
from cairis.core.ValueType import ValueType
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
from cairis.tools.JsonConverter import json_deserialize
from cairis.tools.ModelDefinitions import AssetEnvironmentPropertiesModel, SecurityAttribute
from cairis.tools.SessionValidator import check_required_keys
from cairis.mio.ModelImport import importModelFile
import os

__author__ = 'Robin Quetin, Shamal Faily'


class AssetAPITests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/NeuroGrid/NeuroGrid.xml',1,'test')

  def setUp(self):
    # region Class fields
    self.logger = logging.getLogger(__name__)
    self.existing_asset_name = 'Data node'
    self.new_asset = Asset(
      assetId=-1,
      assetName='Test',
      shortCode='TST',
      assetDescription='This is a new test asset',
      assetSig='Very significant',
      assetType='Hardware',
      cFlag=0,
      cRationale=None,
      tags=[],
      ifs=[],
      cProps=[]
    )
    self.new_asset_sec_attr = [
      SecurityAttribute(
        'Accountability',
        'Low',
        'None'
      ),
      SecurityAttribute(
        'Confidentiality',
        'Medium',
        'None'
      )
    ]
    self.new_asset_props = [
      AssetEnvironmentProperties(
        environmentName='Stroke',
        associations=[[0,"Association","1..*","","","1","Association",0,"Grid meta-data"]],
        syProperties=self.new_asset_sec_attr,
        pRationale=[]
      )
    ]
    self.new_asset_dict = {
      'session_id': 'test',
      'object': self.new_asset
    }
    # endregion


  def test_get_all(self):
    method = 'test_get_all'
    rv = self.app.get('/api/assets?session_id=test')
    if (sys.version_info > (3,)):
      assets = json_deserialize(rv.data.decode('utf-8'))
    else:
      assets = json_deserialize(rv.data)
    self.assertIsNotNone(assets, 'No results after deserialization')
    self.assertIsInstance(assets, list, 'The result is not a list as expected')
    self.assertGreater(len(assets), 0, 'No assets in the list')
    self.assertIsInstance(assets[0], dict)
    self.logger.info('[%s] Assets found: %d', method, len(assets))
    self.logger.info('[%s] First asset: %s\n', method, assets[0]['theName'])

  def test_get_all_summary(self):
    method = 'test_get_all_summary'
    rv = self.app.get('/api/assets/summary?session_id=test')
    if (sys.version_info > (3,)):
      assets = json_deserialize(rv.data.decode('utf-8'))
    else:
      assets = json_deserialize(rv.data)
    self.assertIsNotNone(assets, 'No results after deserialization')
    self.assertGreater(len(assets), 0, 'No asset summaries')
    self.assertIsInstance(assets[0], dict)
    self.logger.info('[%s] Assets found: %d', method, len(assets))
    self.logger.info('[%s] First asset summary: %s [%d]\n', method, assets[0]['theName'], assets[0]['theType'])

  def test_post(self):
    method = 'test_post_new'
    rv = self.app.post('/api/assets', content_type='application/json', data=jsonpickle.encode(self.new_asset_dict))
    if (sys.version_info > (3,)):
      postResponse = rv.data.decode('utf-8')
    else:
      postResponse = rv.data
    self.logger.debug('[%s] Response data: %s', method, postResponse)
    json_resp = json_deserialize(postResponse)
    self.assertIsNotNone(postResponse, 'No results after deserialization')
    url = '/api/assets/name/' + quote(self.new_asset_dict['object'].theName) + '?session_id=test'
    rv = self.app.get(url)
    if (sys.version_info > (3,)):
      asset = json_deserialize(rv.data.decode('utf-8'))
    else:
      asset = json_deserialize(rv.data)
    self.logger.info('[%s] Asset: %s\n', method, asset['theName'])


  def test_get_invalid_name(self):
    method = 'test_get_name'
    url = '/api/assets/name/invalidname?session_id=test'
    rv = self.app.get(url)
    msg = json_deserialize(rv.data.decode('utf-8'))
    self.assertIsNotNone(msg, 'No results after deserialization')
    self.assertEqual(msg['code'],404)
   

  def test_get_name(self):
    method = 'test_get_name'
    url = '/api/assets/name/%s?session_id=test' % quote(self.existing_asset_name)
    rv = self.app.get(url)
    if (sys.version_info > (3,)):
      asset = json_deserialize(rv.data.decode('utf-8'))
    else:
      asset = json_deserialize(rv.data)
    self.assertIsNotNone(asset, 'No results after deserialization')
    self.assertEqual(asset['theName'],self.existing_asset_name)

  def test_put_name(self):
    method = 'test_put_name'
    rv = self.app.post('/api/assets', content_type='application/json', data=jsonpickle.encode(self.new_asset_dict))

    url = '/api/assets/name/%s' % quote(self.new_asset.theName)
    upd_asset = self.new_asset
    upd_asset.theName = 'Test2'
    upd_asset_dict = self.new_asset_dict
    upd_asset_dict['object'] = upd_asset
    upd_asset_body = jsonpickle.encode(upd_asset_dict)
    self.logger.info('[%s] JSON data: %s', method, upd_asset_body)

    rv = self.app.put(url, content_type='application/json', data=upd_asset_body)
    if (sys.version_info > (3,)):
      putResponse = rv.data.decode('utf-8')
    else:
      putResponse = rv.data
    self.logger.debug('[%s] Response data: %s', method, putResponse)
    json_resp = json_deserialize(putResponse)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    message = json_resp.get('message', None)
    self.assertIsNotNone(message, 'No message returned')

    rv = self.app.get('/api/assets/name/Test2?session_id=test')
    if (sys.version_info > (3,)):
      asset = json_deserialize(rv.data.decode('utf-8'))
    else:
      asset = json_deserialize(rv.data)
    self.logger.info('[%s] Asset: %s\n', method, asset['theName'])

  def test_delete_name(self):
    method = 'test_delete_name'
    url = '/api/assets/name/{}?session_id=test'.format(quote(self.new_asset.theName))
    rv = self.app.delete(url)
    url = '/api/assets/name/Test2?session_id=test'.format(quote(self.new_asset.theName))
    rv = self.app.delete(url)
    if (sys.version_info > (3,)):
      delResponse = rv.data.decode('utf-8')
    else:
      delResponse = rv.data
    self.logger.debug('[%s] Response data: %s', method, delResponse)
    json_resp = json_deserialize(delResponse)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    message = json_resp.get('message', None)
    self.assertIsNotNone(message, 'No message returned')
    self.logger.info('[%s] Message: %s\n', method, message)

  def test_types_get(self):
    method = 'test_types_get'
    rv = self.app.get('/api/assets/types?session_id=test')
    if (sys.version_info > (3,)):
      assets = jsonpickle.decode(rv.data.decode('utf-8'))
    else:
      assets = jsonpickle.decode(rv.data)
    self.assertIsNotNone(assets, 'No results after deserialization')
    self.assertIsInstance(assets, list, 'The result is not a dictionary as expected')
    self.assertGreater(len(assets), 0, 'No assets in the dictionary')
    self.logger.info('[%s] Asset types found: %d', method, len(assets))
    asset_type = assets[0]
    self.logger.info('[%s] First asset types: %s\n', method, asset_type['theName'])

  def test_types_delete(self):
    method = 'test_types_delete'
    url = '/api/assets/types/name/%s?session_id=test' % quote(self.prepare_new_asset_type().theName)
    json_dict = {
      'session_id': 'test',
      'object': self.prepare_new_asset_type()
    }
    new_asset_type_body = jsonpickle.encode(json_dict, unpicklable=False)

    self.app.delete(url)
    self.logger.info('[%s] Object to delete: %s', method, new_asset_type_body)
    self.app.post('/api/assets/types', content_type='application/json', data=new_asset_type_body)
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.delete(url)
    if (sys.version_info > (3,)):
      delResponse = rv.data.decode('utf-8')
    else:
      delResponse = rv.data
    self.logger.info('[%s] Response data: %s', method, delResponse)
    self.assertIsNotNone(delResponse, 'No response')
    json_resp = jsonpickle.decode(delResponse)
    self.assertIsInstance(json_resp, dict, 'The response cannot be converted to a dictionary')
    message = json_resp.get('message', None)
    self.assertIsNotNone(message, 'No message in response')
    self.assertEqual(message,'Test asset type deleted')

  def test_types_post(self):
    method = 'test_types_post'
    url = '/api/assets/types'
    self.logger.info('[%s] URL: %s', method, url)
    json_dict = {'session_id': 'test', 'object': self.prepare_new_asset_type()}
    new_asset_type_body = jsonpickle.encode(json_dict, unpicklable=False)
    self.logger.info('JSON data: %s', new_asset_type_body)

    rv = self.app.post(url, content_type='application/json', data=new_asset_type_body)
    if (sys.version_info > (3,)):
      postResponse = rv.data.decode('utf-8')
    else:
      postResponse = rv.data
    self.logger.debug('[%s] Response data: %s', method, postResponse)
    json_resp = jsonpickle.decode(postResponse)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertEqual(ackMsg,'Test asset type created')

    rv = self.app.delete('/api/assets/types/name/%s?session_id=test' % quote(self.prepare_new_asset_type().theName))
    delResponse = rv.data.decode('utf-8')
    self.assertIsNotNone(delResponse, 'No response')
    json_resp = jsonpickle.decode(delResponse)
    self.assertIsInstance(json_resp, dict, 'The response cannot be converted to a dictionary')
    message = json_resp.get('message', None)
    self.assertIsNotNone(message, 'No message in response')
    self.assertEqual(message,'Test asset type deleted')

  def test_types_put(self):
    method = 'test_types_put'
    url = '/api/assets/types'
    self.logger.info('[%s] URL: %s', method, url)
    json_dict = {'session_id': 'test', 'object': self.prepare_new_asset_type()}
    new_asset_type_body = jsonpickle.encode(json_dict)
    self.logger.info('JSON data: %s', new_asset_type_body)

    rv = self.app.delete('/api/assets/types/name/%s?session_id=test' % quote(self.prepare_new_asset_type().theName))
    rv = self.app.post(url, content_type='application/json', data=new_asset_type_body)
    if (sys.version_info > (3,)):
      postResponse = rv.data.decode('utf-8')
    else:
      postResponse = rv.data
    self.logger.debug('[%s] Response data: %s', method, postResponse)
    json_resp = jsonpickle.decode(postResponse)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertEqual(ackMsg,'Test asset type created')

    type_to_update = self.prepare_new_asset_type()
    type_to_update.theName = 'Edited test asset type'
    json_dict = {'session_id': 'test', 'object': type_to_update}
    upd_type_body = jsonpickle.encode(json_dict)
    rv = self.app.put('/api/assets/types/name/%s?session_id=test' % quote(self.prepare_new_asset_type().theName), data=upd_type_body, content_type='application/json')
    if (sys.version_info > (3,)):
      putResponse = rv.data.decode('utf-8')
    else:
      putResponse = rv.data
    self.assertIsNotNone(rv.data, 'No response')
    json_resp = jsonpickle.decode(putResponse)
    self.assertIsNotNone(json_resp)
    self.assertIsInstance(json_resp, dict)
    message = json_resp.get('message', None)
    self.assertIsNotNone(message, 'No message in response')
    self.logger.info('[%s] Message: %s', method, message)
    self.assertEqual(message,'Edited test asset type updated')

    rv = self.app.get('/api/assets/types/name/%s?session_id=test' % quote(type_to_update.theName))
    if (sys.version_info > (3,)):
      getResponse = rv.data.decode('utf-8')
    else:
      getResponse = rv.data
    upd_asset_type = jsonpickle.decode(getResponse)
    self.assertIsNotNone(upd_asset_type, 'Unable to decode JSON data')
    self.logger.debug('[%s] Response data: %s', method, getResponse)
    self.logger.info('[%s] Asset type: %s\n', method, upd_asset_type['theName'])

    rv = self.app.delete('/api/assets/types/name/%s?session_id=test' % quote(type_to_update.theName))

  def prepare_new_asset_type(self):
    new_type = ValueType(
                 valueTypeId=-1,
                 valueTypeName='Test asset type',
                 valueTypeDescription='This is a test asset type',
                 vType='asset-type',
                 vEnv='all'
               )
    new_type.theEnvironmentName = 'all'
    return new_type
