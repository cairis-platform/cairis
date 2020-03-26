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
from cairis.core.DocumentReference import DocumentReference
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
from cairis.mio.ModelImport import importModelFile
from cairis.tools.JsonConverter import json_deserialize
import os

__author__ = 'Shamal Faily'

class DocumentReferenceAPITests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/ACME_Water/ACME_Water.xml',1,'test')


  def setUp(self):
    self.logger = logging.getLogger(__name__)
    self.new_dr = DocumentReference(
      refId = '-1',
      refName = 'Test document reference name',
      docName = 'Alarm handling GT concept',
      cName = 'SF',
      docExc = 'Test text segment')
    self.new_dr_dict = {
      'session_id' : 'test',
      'object': self.new_dr
    }
    self.existing_dr_name = 'Role restrictions'

  def test_get_all(self):
    method = 'test_get_document_references'
    url = '/api/document_references?session_id=test'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    drs = jsonpickle.decode(responseData)
    self.assertIsNotNone(drs, 'No results after deserialization')
    self.assertIsInstance(drs, list, 'The result is not a list as expected')
    self.assertGreater(len(drs), 0, 'No document references in the dictionary')
    self.logger.info('[%s] Document references found: %d', method, len(drs))
    dr = drs[0]
    self.logger.info('[%s] First document reference: %s\n', method, dr['theName'])

  def test_get_by_name(self):
    method = 'test_get_by_name'
    url = '/api/document_references/name/%s?session_id=test' % quote(self.existing_dr_name)
    rv = self.app.get(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.assertIsNotNone(responseData, 'No response')
    self.logger.debug('[%s] Response data: %s', method, responseData)
    dr = jsonpickle.decode(responseData)
    self.assertIsNotNone(dr, 'No results after deserialization')
    self.logger.info('[%s] Document reference: %s\n', method, dr['theName'])

  def test_post(self):
    method = 'test_post_new'
    rv = self.app.post('/api/document_references', content_type='application/json', data=jsonpickle.encode(self.new_dr_dict))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertGreater(ackMsg.find('created'),-1,'Document reference not created')


  def test_put(self):
    method = 'test_put'
    self.new_dr_dict['object'].theExcerpt = 'Updated text segment'
    updDict = self.new_dr_dict
    updDict['object'].theName = 'Updated DR name'
    url = '/api/document_references/name/%s?session_id=test' % quote(self.existing_dr_name)
    rv = self.app.put(url, content_type='application/json', data=jsonpickle.encode(updDict))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertGreater(ackMsg.find('updated'),-1,'Document reference not updated')

  def test_delete(self):
    method = 'test_delete'

    rv = self.app.post('/api/document_references', content_type='application/json', data=jsonpickle.encode(self.new_dr_dict))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)

    url = '/api/document_references/name/%s?session_id=test' % quote(self.new_dr.theName)
    rv = self.app.delete(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertGreater(ackMsg.find('deleted'),-1,'Document reference not deleted')
