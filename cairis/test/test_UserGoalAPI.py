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
from cairis.core.ReferenceSynopsis import ReferenceSynopsis
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
from cairis.bin.cimport import package_import
from cairis.tools.JsonConverter import json_deserialize
import os

__author__ = 'Shamal Faily'

class UserGoalAPITests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    pkgStr = open(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/webinos.cairis','rb').read()
    package_import(pkgStr,'test')

  def setUp(self):
    self.logger = logging.getLogger(__name__)
    self.new_ug = ReferenceSynopsis(
      rsId = '-1',
      refName = 'Schedules life around TV shows',
      synName = 'Schedule activities',
      dimName = 'goal',
      aType = 'persona',
      aName = 'Justin',
      synDim = 'document_reference',
      initialSatisfaction = 'None',
      goals = [])
    self.new_ug_dict = {
      'session_id' : 'test',
      'object': self.new_ug
    }
    self.existing_ug_name = 'Schedule diary with mobile'

  def test_get_all(self):
    method = 'test_get_user_goals'
    url = '/api/user_goals?session_id=test'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    responseData = rv.data.decode('utf-8')
    ugs = jsonpickle.decode(responseData)
    self.assertIsNotNone(ugs, 'No results after deserialization')
    self.assertIsInstance(ugs, list, 'The result is not a list as expected')
    self.assertGreater(len(ugs), 0, 'No user goals in the dictionary')
    self.logger.info('[%s] User goals found: %d', method, len(ugs))
    ug = ugs[0]
    self.logger.info('[%s] First user goal: %s\n', method, ug['theSynopsis'])

  def test_get_role_usergoals(self):
    method = 'test_get_role_usergoals'
    url = '/api/user_goals/role/User?session_id=test'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    responseData = rv.data.decode('utf-8')
    ugs = jsonpickle.decode(responseData)
    self.assertIsNotNone(ugs, 'No results after deserialization')
    self.assertIsInstance(ugs, list, 'The result is not a list as expected')
    self.assertGreater(len(ugs), 0, 'No user goals in the list')
    self.logger.info('[%s] User goals found: %d', method, len(ugs))

  def test_get_user_goal_filters(self):
    method = 'test_user_goal_filters'
    url = '/api/user_goals/model/environment/Complete/persona/Justin/filters?session_id=test'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    responseData = rv.data.decode('utf-8')
    filters = jsonpickle.decode(responseData)
    self.assertIsNotNone(filters, 'No results after deserialization')
    self.assertIsInstance(filters, list, 'The result is not a list as expected')
    self.assertGreater(len(filters), 0, 'No filters in the list')
    self.logger.info('[%s] Filters found: %d', method, len(filters))

  def test_get_by_name(self):
    method = 'test_get_by_name'
    url = '/api/user_goals/name/%s?session_id=test' % quote(self.existing_ug_name)
    rv = self.app.get(url)
    responseData = rv.data.decode('utf-8')
    self.assertIsNotNone(responseData, 'No response')
    self.logger.debug('[%s] Response data: %s', method, responseData)
    ug = jsonpickle.decode(responseData)
    self.assertIsNotNone(ug, 'No results after deserialization')
    self.logger.info('[%s] User goal: %s\n', method, ug['theSynopsis'])

  def test_post(self):
    method = 'test_post_new'
    rv = self.app.post('/api/user_goals', content_type='application/json', data=jsonpickle.encode(self.new_ug_dict))
    responseData = rv.data.decode('utf-8')
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertGreater(ackMsg.find('created'),-1,'User goal not created')


  def test_put(self):
    method = 'test_put'
    self.new_ug_dict['object'].theExcerpt = 'Schedules activities'
    url = '/api/user_goals/name/%s?session_id=test' % quote(self.existing_ug_name)
    rv = self.app.put(url, content_type='application/json', data=jsonpickle.encode(self.new_ug_dict))
    responseData = rv.data.decode('utf-8')
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertGreater(ackMsg.find('updated'),-1,'User goal not updated')

  def test_delete(self):
    method = 'test_delete'

    rv = self.app.post('/api/user_goals', content_type='application/json', data=jsonpickle.encode(self.new_ug_dict))
    responseData = rv.data.decode('utf-8')
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)

    url = '/api/user_goals/name/%s?session_id=test' % quote(self.new_ug.theSynopsis)
    rv = self.app.delete(url)
    responseData = rv.data.decode('utf-8')
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertGreater(ackMsg.find('deleted'),-1,'User goal not deleted')
