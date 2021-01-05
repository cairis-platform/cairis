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
from cairis.core.UserStory import UserStory
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
from cairis.mio.ModelImport import importModelFile
from cairis.tools.JsonConverter import json_deserialize
import os

__author__ = 'Shamal Faily'

class UserStoryAPITests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    importModelFile(os.environ['CAIRIS_SRC'] + '/test/NeuroGridTest.xml',1,'test')


  def setUp(self):
    self.logger = logging.getLogger(__name__)
    self.new_us = UserStory(
      usId = '-1',
      usName = 'Delegation',
      usAuth = 'SF',
      usRole = 'Researcher',
      usDesc = 'Complete delegation form',
      ugName = 'Security delegated',
      ac = ['TBC'])
    self.new_us_dict = {
      'session_id' : 'test',
      'object': self.new_us
    }
    self.existing_us_name = 'Paperwork'

  def test_get_all(self):
    method = 'test_get_all'
    url = '/api/userstories?session_id=test'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    uss = jsonpickle.decode(responseData)
    self.assertIsNotNone(uss, 'No results after deserialization')
    self.assertIsInstance(uss, list, 'The result is not a list as expected')
    self.assertGreater(len(uss), 0, 'No user stories in the list')
    self.assertEqual(uss[0]['theRole'],'Researcher')


  def test_get_by_name(self):
    method = 'test_get_by_name'
    url = '/api/userstories/name/%s?session_id=test' % quote(self.existing_us_name)
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    us = jsonpickle.decode(responseData)
    self.assertIsNotNone(us, 'No results after deserialization')
    self.assertEqual(us['theDescription'],'Submit ethics approval')

  def test_post(self):
    method = 'test_post_new'
    rv = self.app.post('/api/userstories', content_type='application/json', data=jsonpickle.encode(self.new_us_dict))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertGreater(ackMsg.find('created'),-1,'User story not created')

  def test_put(self):
    method = 'test_put'
    upd_dict = self.new_us_dict
    upd_dict['object'].theName = 'Updated name'
    url = '/api/userstories/name/%s?session_id=test' % quote(self.existing_us_name)
    rv = self.app.put(url, content_type='application/json', data=jsonpickle.encode(upd_dict))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertGreater(ackMsg.find('updated'),-1,'User story not updated')

  def test_delete(self):
    method = 'test_delete'

    rv = self.app.post('/api/userstories', content_type='application/json', data=jsonpickle.encode(self.new_us_dict))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)

    url = '/api/userstories/name/%s?session_id=test' % quote(self.new_us_dict['object'].theName)
    rv = self.app.delete(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data

    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertGreater(ackMsg.find('deleted'),-1,'User story not deleted')
