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
    self.logger.debug('[%s] Response data: %s', method, rv.data)
    json_resp = jsonpickle.decode(rv.data)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    self.assertEqual(json_resp['message'],'TrustBoundary successfully added')
    rv = self.app.delete('/api/trust_boundaries/name/Shibboleth?session_id=test')


  def test_get_all(self):
    method = 'test_get_all'
    rv = self.app.get('/api/trust_boundaries?session_id=test')
    tbs = jsonpickle.decode(rv.data)
    self.assertIsNotNone(tbs, 'No results after deserialization')
    self.assertIsInstance(tbs, dict, 'The result is not a dictionary as expected')
    self.assertGreater(len(tbs), 0, 'No trust_boundaries in the dictionary')
    self.logger.info('[%s] TrustBoundaries found: %d', method, len(tbs))
    tb = tbs.values()[0]
    self.assertEqual(tb['theName'],'local')
    self.assertEqual(tb['theDescription'],'Local IT support')
    self.assertEqual(tb['theEnvironmentProperties'][0]['theComponents'][0]['theName'],'Credentials Store')
    self.assertEqual(tb['theEnvironmentProperties'][0]['theComponents'][0]['theType'],'datastore')

  def test_get_by_name(self):
    method = 'test_get_by_name'
    rv = self.app.post('/api/trust_boundaries?session_id=test', content_type='application/json', data=self.prepare_json())
    url = '/api/trust_boundaries/name/Shibboleth?session_id=test'
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    self.logger.debug('[%s] Response data: %s', method, rv.data)
    tb = jsonpickle.decode(rv.data)
    self.assertIsNotNone(tb, 'No results after deserialization')
    self.assertEqual(tb['theName'],'Shibboleth')
    self.assertEqual(tb['theDescription'],'Identity Provider')
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
    json_resp = jsonpickle.decode(rv.data)
    self.assertIsNotNone(json_resp)
    self.assertEqual(json_resp['message'],'TrustBoundary successfully updated')

    rv = self.app.get('/api/trust_boundaries/name/Shibboleth?session_id=test')
    self.assertIsNotNone(rv.data, 'No response')
    self.logger.debug('[%s] Response data: %s', method, rv.data)
    upd_tb = jsonpickle.decode(rv.data)
    self.assertIsNotNone(upd_tb, 'No results after deserialization')
    self.assertEqual(upd_tb['theName'],'Shibboleth')
    self.assertEqual(upd_tb['theDescription'],'Identity provider')
    self.assertEqual(upd_tb['theEnvironmentProperties'][0]['theComponents'][0]['theName'],'Authenticate Researcher')
    self.assertEqual(upd_tb['theEnvironmentProperties'][0]['theComponents'][0]['theType'],'process')
    rv = self.app.delete('/api/trust_boundaries/name/Shibboleth?session_id=test')

  def test_delete(self):
    rv = self.app.post('/api/trust_boundaries?session_id=test', content_type='application/json', data=self.prepare_json())
    url = '/api/trust_boundaries/name/Shibboleth?session_id=test'
    rv = self.app.delete(url)
    self.assertIsNotNone(rv.data, 'No response')
    json_resp = jsonpickle.decode(rv.data)
    self.assertIsNotNone(json_resp)
    self.assertEqual(json_resp['message'],'TrustBoundary successfully deleted')
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
