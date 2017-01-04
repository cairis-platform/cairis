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
from StringIO import StringIO
import os
import jsonpickle
from cairis.core.Trace import Trace
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
from cairis.mio.ModelImport import importModelFile
from cairis.tools.JsonConverter import json_deserialize
import os

__author__ = 'Shamal Faily'

class TraceAPITests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/NeuroGrid/NeuroGrid.xml',1,'test')


  def setUp(self):
    self.logger = logging.getLogger(__name__)
    self.new_tr = Trace(
      fObjt = 'requirement',
      fName = 'AC-1',
      tObjt = 'vulnerability',
      tName = 'Certificate ubiquity')
    self.new_tr_dict = {
      'session_id' : 'test',
      'object': self.new_tr
    }

  def test_get_all(self):
    method = 'test_get_traces'
    url = '/api/traces/environment/Psychosis?session_id=test'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    trs = jsonpickle.decode(rv.data)
    self.assertIsNotNone(trs, 'No results after deserialization')
    self.assertGreater(len(trs), 0, 'No traces in the list')
    self.logger.info('[%s] Traces found: %d', method, len(trs))
    self.assertEquals(len(trs),7)

  def test_post(self):
    method = 'test_post_new'
    rv = self.app.post('/api/traces', content_type='application/json', data=jsonpickle.encode(self.new_tr_dict))
    self.logger.debug('[%s] Response data: %s', method, rv.data)
    json_resp = json_deserialize(rv.data)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertEqual(ackMsg, 'Trace successfully added')

  def test_delete(self):
    method = 'test_delete'
    rv = self.app.delete('/api/traces/from_type/requirement/from_name/AC-1/to_type/vulnerability/to_name/Certificate%20ubiquity?session_id=test', content_type='application/json')

    self.logger.debug('[%s] Response data: %s', method, rv.data)
    json_resp = json_deserialize(rv.data)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertEqual(ackMsg, 'Trace successfully deleted')
