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

import json
import logging
import sys
if (sys.version_info > (3,)):
  from urllib.parse import quote
else:
  from urllib import quote
import jsonpickle
from cairis.core.TrustBoundary import TrustBoundary
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
import os
from cairis.mio.ModelImport import importModelFile
from cairis.tools.ModelDefinitions import TrustBoundaryModel

__author__ = 'Shamal Faily'


class TrustBoundaryAPITests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    importModelFile(os.environ['CAIRIS_SRC'] + '/test/DFDTestModel.xml',1,'test')


  
  def setUp(self):
    # region Class fields
    self.logger = logging.getLogger(__name__)
    f = open(os.environ['CAIRIS_SRC'] + '/test/trust_boundaries.json')
    d = json.load(f)
    f.close()
    self.iTrustBoundaries = d['trust_boundaries']
    # endregion

  def test_post(self):
    method = 'test_post'
    url = '/api/trust_boundaries'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.post(url, content_type='application/json', data=self.prepare_json())
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    self.assertEqual(json_resp['message'],'Shibboleth created')
    rv = self.app.delete('/api/trust_boundaries/name/Shibboleth?session_id=test')


  def test_get_all(self):
    method = 'test_get_all'
    rv = self.app.get('/api/trust_boundaries?session_id=test')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    tbs = jsonpickle.decode(responseData)
    self.assertIsNotNone(tbs, 'No results after deserialization')
    self.assertIsInstance(tbs, list, 'The result is not a list as expected')
    self.assertGreater(len(tbs), 0, 'No trust_boundaries in the dictionary')
    self.logger.info('[%s] TrustBoundaries found: %d', method, len(tbs))
    tb = tbs[0]
    self.assertEqual(len(tbs),1)

  def test_get_by_name(self):
    method = 'test_get_by_name'
    rv = self.app.post('/api/trust_boundaries?session_id=test', content_type='application/json', data=self.prepare_json())
    url = '/api/trust_boundaries/name/Shibboleth?session_id=test'
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    tb = jsonpickle.decode(responseData)
    self.assertIsNotNone(tb, 'No results after deserialization')
    self.assertEqual(tb['theName'],'Shibboleth')
    self.assertEqual(tb['theDescription'],'Identity Provider')
    self.assertEqual(tb['theTags'],['tag1'])
    self.assertEqual(tb['theEnvironmentProperties'][0]['theComponents'][0]['theName'],'Authenticate Researcher')
    self.assertEqual(tb['theEnvironmentProperties'][0]['theComponents'][0]['theType'],'process')
    rv = self.app.delete('/api/trust_boundaries/name/Shibboleth?session_id=test')


  def test_put(self):
    method = 'test_put'
    rv = self.app.post('/api/trust_boundaries?session_id=test', content_type='application/json', data=self.prepare_json())
    url = '/api/trust_boundaries/name/Shibboleth'
    self.logger.info('[%s] URL: %s', method, url)

    upd_body = self.prepare_json(trust_boundary=self.prepare_updated_trust_boundary())
    rv = self.app.put('/api/trust_boundaries/name/Shibboleth?session_id=test', data=upd_body, content_type='application/json')
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp)
    self.assertEqual(json_resp['message'],'Shibboleth updated')

    rv = self.app.get('/api/trust_boundaries/name/Shibboleth?session_id=test')
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    upd_tb = jsonpickle.decode(responseData)
    self.assertIsNotNone(upd_tb, 'No results after deserialization')
    self.assertEqual(upd_tb['theName'],'Shibboleth')
    self.assertEqual(upd_tb['theDescription'],'Identity provider')
    self.assertEqual(upd_tb['theTags'],['tag1'])
    self.assertEqual(upd_tb['theEnvironmentProperties'][0]['theComponents'][0]['theName'],'Authenticate Researcher')
    self.assertEqual(upd_tb['theEnvironmentProperties'][0]['theComponents'][0]['theType'],'process')
    rv = self.app.delete('/api/trust_boundaries/name/Shibboleth?session_id=test')

  def test_delete(self):
    rv = self.app.post('/api/trust_boundaries?session_id=test', content_type='application/json', data=self.prepare_json())
    url = '/api/trust_boundaries/name/Shibboleth?session_id=test'
    rv = self.app.delete(url)
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp)
    self.assertEqual(json_resp['message'],'Shibboleth deleted')
    rv = self.app.delete('/api/trust_boundaries/name/Shibboleth?session_id=test')

  def tearDown(self):
    pass


  def prepare_new_trust_boundary(self):
    return self.iTrustBoundaries[0]

  def prepare_updated_trust_boundary(self):
    upd_tb = self.iTrustBoundaries[0]
    upd_tb['theDescription'] = 'Identity provider'
    return upd_tb

  def prepare_dict(self, trust_boundary=None):
    if trust_boundary is None:
      trust_boundary = self.prepare_new_trust_boundary()
    return {
      'session_id': 'test',
      'object': trust_boundary,
    }

  def prepare_json(self, data_dict=None, trust_boundary=None):
    if data_dict is None:
      data_dict = self.prepare_dict(trust_boundary=trust_boundary)
    else:
      assert isinstance(data_dict, dict)
    new_trust_boundary_body = jsonpickle.encode(data_dict, unpicklable=False)
    self.logger.info('JSON data: %s', new_trust_boundary_body)
    return new_trust_boundary_body
