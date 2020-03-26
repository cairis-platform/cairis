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
import jsonpickle
from cairis.core.ExternalDocument import ExternalDocument
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
from cairis.mio.ModelImport import importModelFile
from cairis.tools.JsonConverter import json_deserialize
import os

__author__ = 'Shamal Faily'

class ExternalDocumentAPITests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/ACME_Water/ACME_Water.xml',1,'test')


  def setUp(self):
    self.logger = logging.getLogger(__name__)
    self.new_edoc = ExternalDocument(
      edId = '-1',
      edName = 'Test external document name',
      edVersion = '1',
      edDate = '2016',
      edAuths = 'SF',
      edDesc = 'Test external document description')
    self.new_edoc_dict = {
      'session_id' : 'test',
      'object': self.new_edoc
    }
    self.existing_edoc_name = 'big security worry GT concept'

  def test_get_all(self):
    method = 'test_get_external_documents'
    url = '/api/external_documents?session_id=test'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    edocs = jsonpickle.decode(responseData)
    self.assertIsNotNone(edocs, 'No results after deserialization')
    self.assertIsInstance(edocs, list, 'The result is not a dictionary as expected')
    self.assertGreater(len(edocs), 0, 'No external documents in the dictionary')
    self.logger.info('[%s] External documents found: %d', method, len(edocs))
    edoc = edocs[0]
    self.logger.info('[%s] First external document: %s\n', method, edoc['theName'])

  def test_get_by_name(self):
    method = 'test_get_by_name'
    url = '/api/external_documents/name/%s?session_id=test' % quote(self.existing_edoc_name)
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    edoc = jsonpickle.decode(responseData)
    self.assertIsNotNone(edoc, 'No results after deserialization')
    self.logger.info('[%s] External document: %s\n', method, edoc['theName'])

  def test_post(self):
    method = 'test_post_new'
    rv = self.app.post('/api/external_documents', content_type='application/json', data=jsonpickle.encode(self.new_edoc_dict))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertGreater(ackMsg.find('created'),-1,'External document not created')

  def test_put(self):
    method = 'test_put'
    self.new_edoc_dict['object'].theVersion = '2'
    upd_dict = self.new_edoc_dict
    upd_dict['object'].theName = 'Unrelated GT concept'
    url = '/api/external_documents/name/%s?session_id=test' % quote(self.existing_edoc_name)
    rv = self.app.put(url, content_type='application/json', data=jsonpickle.encode(upd_dict))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertGreater(ackMsg.find('updated'),-1,'External document not updated')

  def test_delete(self):
    method = 'test_delete'

    rv = self.app.post('/api/external_documents', content_type='application/json', data=jsonpickle.encode(self.new_edoc_dict))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)

    url = '/api/external_documents/name/%s?session_id=test' % quote(self.new_edoc.theName)
    rv = self.app.delete(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data

    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertGreater(ackMsg.find('deleted'),-1,'External document not deleted')
