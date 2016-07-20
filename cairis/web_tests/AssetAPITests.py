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
from urllib import quote

import jsonpickle

from cairis.core.Asset import Asset
from cairis.core.AssetEnvironmentProperties import AssetEnvironmentProperties
from cairis.core.ValueType import ValueType
from cairis.web_tests.CairisDaemonTestCase import CairisDaemonTestCase
from cairis.tools.JsonConverter import json_deserialize
from cairis.tools.ModelDefinitions import AssetEnvironmentPropertiesModel, SecurityAttribute
from cairis.tools.SessionValidator import check_required_keys
from cairis.mio.ModelImport import importModelFile

class AssetAPITests(CairisDaemonTestCase):
    # region Class fields
    logger = logging.getLogger(__name__)
    existing_asset_name = 'Data node'
    new_asset = Asset(
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
    new_asset_sec_attr = [
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
    new_asset_props = [
        AssetEnvironmentProperties(
            environmentName='Stroke',
            associations=[[0,"Association","1..*","","","1","Association",0,"Grid meta-data"]],
            syProperties=new_asset_sec_attr,
            pRationale=[]
        )
    ]
    new_asset_dict = {
        'session_id': 'test',
        'object': new_asset
    }
    # endregion

#    def setUp(self):
#        importModelFile('../../examples/exemplars/NeuroGrid/NeuroGrid.xml',1,'test')

    def test_get_all(self):
        method = 'test_get_all'
        rv = self.app.get('/api/assets?session_id=test')
        assets = json_deserialize(rv.data)
        self.assertIsNotNone(assets, 'No results after deserialization')
        self.assertIsInstance(assets, dict, 'The result is not a dictionary as expected')
        self.assertGreater(len(assets), 0, 'No assets in the dictionary')
        self.assertIsInstance(assets.values()[0], Asset)
        self.logger.info('[%s] Assets found: %d', method, len(assets))
        self.logger.info('[%s] First asset: %s [%d]\n', method, assets.values()[0].theName, assets.values()[0].theId)

    def test_post(self):
        method = 'test_post_new'
        rv = self.app.post('/api/assets', content_type='application/json', data=jsonpickle.encode(self.new_asset_dict))
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        json_resp = json_deserialize(rv.data)
        self.assertIsNotNone(json_resp, 'No results after deserialization')
        asset_id = json_resp.get('asset_id', None)
        self.assertIsNotNone(asset_id, 'No asset ID returned')

        rv = self.app.get('/api/assets/id/%d?session_id=test' % asset_id)
        asset = json_deserialize(rv.data)
        self.logger.info('[%s] Asset: %s [%d]\n', method, asset.theName, asset.theId)

    def test_get_id(self):
        method = 'test_get_id'
        rv = self.app.get('/api/assets/id/127?session_id=test')
        asset = json_deserialize(rv.data)
        self.assertIsNotNone(asset, 'No results after deserialization')
        self.assertIsInstance(asset, Asset, 'The result is not an asset as expected')
        self.logger.info('[%s] Asset: %s [%d]\n', method, asset.theName, asset.theId)

    def test_get_name(self):
        method = 'test_get_name'
        url = '/api/assets/name/%s?session_id=test' % quote(self.existing_asset_name)
        rv = self.app.get(url)
        asset = json_deserialize(rv.data)
        self.assertIsNotNone(asset, 'No results after deserialization')
        self.assertIsInstance(asset, Asset, 'The result is not an asset as expected')
        self.logger.info('[%s] Asset: %s [%d]\n', method, asset.theName, asset.theId)

    def test_put_name(self):
        method = 'test_put_name'
        url = '/api/assets/name/%s' % quote(self.new_asset.theName)

        upd_asset = self.new_asset
        upd_asset.theName = 'Test2'
        upd_asset_dict = self.new_asset_dict
        upd_asset_dict['object'] = upd_asset
        upd_asset_body = jsonpickle.encode(upd_asset_dict)
        self.logger.info('[%s] JSON data: %s', method, upd_asset_body)

        rv = self.app.put(url, content_type='application/json', data=upd_asset_body)
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        json_resp = json_deserialize(rv.data)
        self.assertIsNotNone(json_resp, 'No results after deserialization')
        message = json_resp.get('message', None)
        self.assertIsNotNone(message, 'No message returned')

        rv = self.app.get('/api/assets/name/Test2?session_id=test')
        asset = json_deserialize(rv.data)
        print str(asset)
        self.logger.info('[%s] Asset: %s [%d]\n', method, asset.name(), asset.id())

    def test_delete_name(self):
        method = 'test_delete_name'
        url = '/api/assets/name/{}?session_id=test'.format(quote(self.new_asset.theName))
        rv = self.app.delete(url)
        url = '/api/assets/name/Test2?session_id=test'.format(quote(self.new_asset.theName))
        rv = self.app.delete(url)
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        json_resp = json_deserialize(rv.data)
        self.assertIsNotNone(json_resp, 'No results after deserialization')
        message = json_resp.get('message', None)
        self.assertIsNotNone(message, 'No message returned')
        self.logger.info('[%s] Message: %s\n', method, message)

    def test_get_props_name_get(self):
        method = 'test_get_props_name_get'
        url = '/api/assets/name/%s/properties?session_id=test' % quote(self.existing_asset_name)

        rv = self.app.get(url)
        asset_props = jsonpickle.decode(rv.data)
        self.assertIsNotNone(asset_props, 'No results after deserialization')
        self.assertIsInstance(asset_props, list, 'Result is not a list')
        self.assertGreater(len(asset_props), 0, 'List does not contain any elements')
        asset_prop = asset_props[0]
        self.logger.info('[%s] Asset property: %s\n', method, asset_prop['theEnvironmentName'])

    def test_update_props_name_put(self):
        method = 'test_update_props_name_put'
        url = '/api/assets/name/%s/properties' % quote(self.new_asset.theName)
        self.logger.info('[%s] Old asset property environment name: %s', method, self.new_asset_props[0].theEnvironmentName)

        upd_asset_props = self.new_asset_props
        upd_asset_props[0].theEnvironmentName = 'Psychosis'
        upd_asset_props_dict = {
            'session_id': 'test',
            'object': upd_asset_props
        }
        upd_asset_props_body = jsonpickle.encode(upd_asset_props_dict)
        self.logger.info('[%s] JSON data: %s', method, upd_asset_props_body)

        rv = self.app.put(url, content_type='application/json', data=upd_asset_props_body)
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        json_resp = json_deserialize(rv.data)
        self.assertIsNotNone(json_resp, 'No results after deserialization')
        message = json_resp.get('message', None)
        self.assertIsNotNone(message, 'No message returned')

        rv = self.app.get('/api/assets/name/Test2/properties?session_id=test')
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        asset_props = jsonpickle.decode(rv.data)
        print 'asset_props:' + str(asset_props)
        self.logger.info('[%s] Asset property environment: %s\n', method, asset_props[0]['theEnvironmentName'])

    def test_types_get(self):
        method = 'test_types_get'
        rv = self.app.get('/api/assets/types?session_id=test')
        assets = jsonpickle.decode(rv.data)
        self.assertIsNotNone(assets, 'No results after deserialization')
        self.assertIsInstance(assets, list, 'The result is not a dictionary as expected')
        self.assertGreater(len(assets), 0, 'No assets in the dictionary')
        self.logger.info('[%s] Asset types found: %d', method, len(assets))
        asset_type = assets[0]
        self.logger.info('[%s] First asset types: %s [%d]\n', method, asset_type['theName'], asset_type['theId'])

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
        self.logger.info('[%s] Response data: %s', method, rv.data)
        self.assertIsNotNone(rv.data, 'No response')
        json_resp = jsonpickle.decode(rv.data)
        self.assertIsInstance(json_resp, dict, 'The response cannot be converted to a dictionary')
        message = json_resp.get('message', None)
        self.assertIsNotNone(message, 'No message in response')
        self.logger.info('[%s] Message: %s\n', method, message)

    def test_types_post(self):
        method = 'test_types_post'
        url = '/api/assets/types'
        self.logger.info('[%s] URL: %s', method, url)
        json_dict = {'session_id': 'test', 'object': self.prepare_new_asset_type()}
        new_asset_type_body = jsonpickle.encode(json_dict, unpicklable=False)
        self.logger.info('JSON data: %s', new_asset_type_body)

        self.app.delete('/api/assets/types/name/%s?session_id=test' % quote(self.prepare_new_asset_type().theName))
        rv = self.app.post(url, content_type='application/json', data=new_asset_type_body)
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        json_resp = jsonpickle.decode(rv.data)
        self.assertIsNotNone(json_resp, 'No results after deserialization')
        type_id = json_resp.get('asset_type_id', None)
        self.assertIsNotNone(type_id, 'No asset type ID returned')
        self.assertGreater(type_id, 0, 'Invalid asset type ID returned [%d]' % type_id)
        self.logger.info('[%s] Asset type ID: %d\n', method, type_id)

        rv = self.app.delete('/api/assets/types/name/%s?session_id=test' % quote(self.prepare_new_asset_type().theName))

    def test_types_put(self):
        method = 'test_types_put'
        url = '/api/assets/types'
        self.logger.info('[%s] URL: %s', method, url)
        json_dict = {'session_id': 'test', 'object': self.prepare_new_asset_type()}
        new_asset_type_body = jsonpickle.encode(json_dict)
        self.logger.info('JSON data: %s', new_asset_type_body)

        rv = self.app.delete('/api/assets/types/name/%s?session_id=test' % quote(self.prepare_new_asset_type().theName))
        rv = self.app.post(url, content_type='application/json', data=new_asset_type_body)
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        json_resp = jsonpickle.decode(rv.data)
        self.assertIsNotNone(json_resp, 'No results after deserialization')
        type_id = json_resp.get('asset_type_id', None)
        self.assertIsNotNone(type_id, 'No asset type ID returned')
        self.assertGreater(type_id, 0, 'Invalid asset type ID returned [%d]' % type_id)
        self.logger.info('[%s] Asset type ID: %d', method, type_id)

        type_to_update = self.prepare_new_asset_type()
        type_to_update.theName = 'Edited test asset type'
        type_to_update.theId = type_id
        json_dict = {'session_id': 'test', 'object': type_to_update}
        upd_type_body = jsonpickle.encode(json_dict)
        rv = self.app.put('/api/assets/types/name/%s?session_id=test' % quote(self.prepare_new_asset_type().theName), data=upd_type_body, content_type='application/json')
        self.assertIsNotNone(rv.data, 'No response')
        json_resp = jsonpickle.decode(rv.data)
        self.assertIsNotNone(json_resp)
        self.assertIsInstance(json_resp, dict)
        message = json_resp.get('message', None)
        self.assertIsNotNone(message, 'No message in response')
        self.logger.info('[%s] Message: %s', method, message)
        self.assertGreater(message.find('successfully updated'), -1, 'The asset was not successfully updated')

        rv = self.app.get('/api/assets/types/name/%s?session_id=test' % quote(type_to_update.theName))
        upd_asset_type = jsonpickle.decode(rv.data)
        self.assertIsNotNone(upd_asset_type, 'Unable to decode JSON data')
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        self.logger.info('[%s] Asset type: %s [%d]\n', method, upd_asset_type['theName'], upd_asset_type['theId'])

        rv = self.app.delete('/api/assets/types/name/%s?session_id=test' % quote(type_to_update.theName))

    def prepare_new_asset_type(self):
        new_type = ValueType(
            valueTypeId=-1,
            valueTypeName='Test asset type',
            valueTypeDescription='This is a test asset type',
            vType='asset-type'
        )
        return new_type
