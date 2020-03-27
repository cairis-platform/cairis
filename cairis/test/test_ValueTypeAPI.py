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
from io import StringIO
import os
import json
import jsonpickle
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
from cairis.mio.ModelImport import importModelFile
from cairis.tools.JsonConverter import json_deserialize
import os

__author__ = 'Shamal Faily'

class ValueTypeAPITests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/NeuroGrid/NeuroGrid.xml',1,'test')


  def setUp(self):
    self.logger = logging.getLogger(__name__)
    f = open(os.environ['CAIRIS_SRC'] + '/test/valuetypes.json')
    d = json.load(f)
    f.close()
    self.new_vt = d['threat_type'][0]
    self.new_vt['theEnvironmentName'] = 'all'
    self.new_vt['theScore'] = 0
    self.new_vt['theRationale'] = 'None'

    self.new_vt_dict = {
      'session_id' : 'test',
      'object': self.new_vt
    }
    self.existing_vt_dict = {
      'session_id' : 'test',
      'object': {}
    }
    self.existing_vt_name = 'Physical'

  def test_get_all(self):
    method = 'test_get_value_types'
    url = '/api/value_types/type/threat_type/environment/all?session_id=test'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    vts = jsonpickle.decode(responseData)
    self.assertIsNotNone(vts, 'No results after deserialization')
    self.assertIsInstance(vts, list, 'The result is not a dictionary as expected')
    self.assertGreater(len(vts), 0, 'No value types in the dictionary')
    self.logger.info('[%s] Value types found: %d', method, len(vts))
    vt = vts[0]
    self.logger.info('[%s] First threat type: %s [%]\n', method, vt['theName'], vt['theType'])

  def test_get_by_name(self):
    method = 'test_get_by_name'
    url = '/api/value_types/type/threat_type/environment/all/name/' + self.existing_vt_name + '?session_id=test'
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    vt = jsonpickle.decode(responseData)
    self.assertIsNotNone(vt, 'No results after deserialization')
    self.logger.info('[%s] Threat Type : %s [%s]\n', method, vt['theName'], vt['theType'])

  def test_post(self):
    method = 'test_post_new'
    rv = self.app.post('/api/value_types/', content_type='application/json', data=jsonpickle.encode(self.new_vt_dict))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertEqual(ackMsg, 'Path Traversal Attack created')

  def test_put(self):
    method = 'test_put'
    url = '/api/value_types/type/threat_type/environment/all/name/' + self.existing_vt_name + '?session_id=test'
    rv = self.app.get(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.existing_vt_dict['object'] = jsonpickle.decode(responseData)
    self.existing_vt_dict['object']['theDescription'] = 'Updated description'
    self.existing_vt_dict['object']['theScore'] = 0
    self.existing_vt_dict['object']['theEnvironmentName'] = 'all'
    rv = self.app.put(url, content_type='application/json', data=jsonpickle.encode(self.existing_vt_dict))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertEqual(ackMsg, 'Physical updated')

  def test_delete(self):
    method = 'test_delete'
    rv = self.app.post('/api/value_types/', content_type='application/json', data=jsonpickle.encode(self.new_vt_dict))
    url = '/api/value_types/type/threat_type/environment/all/name/' + self.new_vt['theName'] + '?session_id=test'
    rv = self.app.delete(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertEqual(ackMsg, self.new_vt['theName'] + ' deleted')
