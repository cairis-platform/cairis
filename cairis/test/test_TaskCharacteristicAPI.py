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
from cairis.core.TaskCharacteristic import TaskCharacteristic
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
from cairis.mio.ModelImport import importModelFile
from cairis.tools.JsonConverter import json_deserialize
from cairis.tools.PseudoClasses import CharacteristicReference
import os

__author__ = 'Shamal Faily'

class TaskCharacteristicAPITests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    importModelFile(os.environ['CAIRIS_SRC'] + '/test/webinos.xml',1,'test')

  def setUp(self):
    self.logger = logging.getLogger(__name__)

    self.new_tc = TaskCharacteristic(
      pcId = -1,
      pName = 'Smart Device Integration',
      modQual = 'Maybe',
      cDesc = 'This is a test characteristic',
      pcGrounds = [{"theReferenceName": "Acknowledge target device", "theDimensionName": "usecase", "theCharacteristicType": "grounds", "theReferenceDescription": "A test grounds description"}],
      pcWarrant = [],
      pcRebuttal = [],
      pcBacking = [])
    self.new_tc_dict = {
      'session_id' : 'test',
      'object': self.new_tc
    }
    self.existing_tc_name = 'Privacy policy betrayed'

  def test_get_all(self):
    method = 'test_get_task_characteristics'
    url = '/api/task_characteristics?session_id=test'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    tcs = jsonpickle.decode(responseData)
    self.assertIsNotNone(tcs, 'No results after deserialization')
    self.assertIsInstance(tcs, list, 'The result is not a dictionary as expected')
    self.assertGreater(len(tcs), 0, 'No task characteristics in the dictionary')
    self.logger.info('[%s] Task characteristics found: %d', method, len(tcs))
    tc = tcs[0]
    self.logger.info('[%s] First task characteristic: %s\n', method, tc['theName'])

  def test_get_by_name(self):
    method = 'test_get_by_name'
    url = '/api/task_characteristics/name/%s?session_id=test' % quote(self.existing_tc_name)
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    tc = jsonpickle.decode(responseData)
    self.assertIsNotNone(tc, 'No results after deserialization')
    self.logger.info('[%s] Task characteristic: %s\n', method, tc['theName'])

  def test_post(self):
    method = 'test_post_new'
    rv = self.app.post('/api/task_characteristics', content_type='application/json', data=jsonpickle.encode(self.new_tc_dict))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertGreater(ackMsg.find('created'),-1,'TC not created')



  def test_put(self):
    method = 'test_put'
    self.new_tc_dict['object'].theExcerpt = 'Updated text segment'
    url = '/api/task_characteristics/name/%s?session_id=test' % quote(self.new_tc.theName)
    rv = self.app.put(url, content_type='application/json', data=jsonpickle.encode(self.new_tc_dict))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertGreater(ackMsg.find('updated'),-1,'TC not updated')


  def test_delete(self):
    method = 'test_delete'
    rv = self.app.post('/api/task_characteristics', content_type='application/json', data=jsonpickle.encode(self.new_tc_dict))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)

    url = '/api/task_characteristics/name/%s?session_id=test' % quote(self.new_tc.theName)
    rv = self.app.delete(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertGreater(ackMsg.find('deleted'),-1,'TC not deleted')

