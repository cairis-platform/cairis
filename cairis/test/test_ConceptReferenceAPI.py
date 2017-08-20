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
from cairis.core.ConceptReference import ConceptReference
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
from cairis.mio.ModelImport import importModelFile
from cairis.tools.JsonConverter import json_deserialize
import os

__author__ = 'Shamal Faily'

class ConceptReferenceAPITests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    importModelFile(os.environ['CAIRIS_SRC'] + '/test/webinos.xml',1,'test')

  def setUp(self):
    self.logger = logging.getLogger(__name__)
    self.new_cr = ConceptReference(
      refId = '-1',
      refName = 'Personal device authentication',
      dimName = 'requirement',
      objtName = 'PS-30',
      cDesc = 'Personal devices support authentication')
    self.new_cr_dict = {
      'session_id' : 'test',
      'object': self.new_cr
    }
    self.existing_cr_name = 'Autostart programmatically controlled'

  def test_get_all(self):
    method = 'test_get_concept_references'
    url = '/api/concept_references?session_id=test'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    crs = jsonpickle.decode(rv.data)
    self.assertIsNotNone(crs, 'No results after deserialization')
    self.assertIsInstance(crs, dict, 'The result is not a dictionary as expected')
    self.assertGreater(len(crs), 0, 'No concept references in the dictionary')
    self.logger.info('[%s] Concept references found: %d', method, len(crs))
    cr = list(crs.values())[0]
    self.logger.info('[%s] First concept reference: %s [%d]\n', method, cr['theName'], cr['theId'])

  def test_get_by_name(self):
    method = 'test_get_by_name'
    url = '/api/concept_references/name/%s?session_id=test' % quote(self.existing_cr_name)
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    self.logger.debug('[%s] Response data: %s', method, rv.data)
    cr = jsonpickle.decode(rv.data)
    self.assertIsNotNone(cr, 'No results after deserialization')
    self.logger.info('[%s] Concept reference: %s [%d]\n', method, cr['theName'], cr['theId'])

  def test_post(self):
    method = 'test_post_new'
    rv = self.app.post('/api/concept_references', content_type='application/json', data=jsonpickle.encode(self.new_cr_dict))
    self.logger.debug('[%s] Response data: %s', method, rv.data)
    json_resp = json_deserialize(rv.data)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertEqual(ackMsg, 'Concept Reference successfully added')

  def test_put(self):
    method = 'test_put'
    self.new_cr_dict['object'].theDescription = 'Updated text segment'
    url = '/api/concept_references/name/%s?session_id=test' % quote(self.existing_cr_name)
    rv = self.app.put(url, content_type='application/json', data=jsonpickle.encode(self.new_cr_dict))
    self.logger.debug('[%s] Response data: %s', method, rv.data)
    json_resp = json_deserialize(rv.data)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertEqual(ackMsg, 'Concept Reference successfully updated')

  def test_delete(self):
    method = 'test_delete'

    rv = self.app.post('/api/concept_references', content_type='application/json', data=jsonpickle.encode(self.new_cr_dict))
    self.logger.debug('[%s] Response data: %s', method, rv.data)
    json_resp = json_deserialize(rv.data)

    url = '/api/concept_references/name/%s?session_id=test' % quote(self.new_cr.theName)
    rv = self.app.delete(url)

    self.logger.debug('[%s] Response data: %s', method, rv.data)
    json_resp = json_deserialize(rv.data)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertEqual(ackMsg, 'Concept Reference successfully deleted')
