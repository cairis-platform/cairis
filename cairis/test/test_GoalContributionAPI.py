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
from cairis.core.GoalContribution import GoalContribution
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
from cairis.bin.cimport import package_import
from cairis.tools.JsonConverter import json_deserialize
import os

__author__ = 'Shamal Faily'

class GoalContributionAPITests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    pkgStr = open(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/webinos.cairis','rb').read()
    package_import(pkgStr,'test')

  def setUp(self):
    self.logger = logging.getLogger(__name__)
    self.new_gc = GoalContribution(
      src = 'Work 9-5',
      srcType = 'document_reference',
      dest = 'Maintain routine schedule',
      destType = 'document_reference',
      me = 'means',
      cont = 'SomePositive')
    self.new_gc_dict = {
      'session_id' : 'test',
      'object': self.new_gc
    }
    self.existing_src_name = 'Work 9-5'
    self.existing_tgt_name = 'Maintain routine schedule'

  def test_get_all(self):
    method = 'test_get_goal_contributions'
    url = '/api/goal_contributions?session_id=test'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    responseData = rv.data.decode('utf-8')
    gcs = jsonpickle.decode(responseData)
    self.assertIsNotNone(gcs, 'No results after deserialization')
    self.assertIsInstance(gcs, list, 'The result is not a list as expected')
    self.assertEqual(len(gcs), 24, 'No goal contributions in the list')
    self.logger.info('[%s] Goal contributions found: %d', method, len(gcs))

  def test_get_by_name(self):
    method = 'test_get_by_name'
    rv = self.app.post('/api/goal_contributions', content_type='application/json', data=jsonpickle.encode(self.new_gc_dict))

    url = '/api/goal_contributions/source/' + quote(self.existing_src_name) + '/target/' + quote(self.existing_tgt_name) + '?session_id=test'
    rv = self.app.get(url)
    responseData = rv.data.decode('utf-8')
    self.assertIsNotNone(responseData, 'No response')
    self.logger.debug('[%s] Response data: %s', method, responseData)
    gc = jsonpickle.decode(responseData)
    self.assertIsNotNone(gc, 'No results after deserialization')
    self.logger.info('[%s] First goal contribution: %s\n', method, gc['theSource'] + " / " + gc['theDestination'])
    rv = self.app.delete(url)

  def test_post(self):
    method = 'test_post_new'
    rv = self.app.post('/api/goal_contributions', content_type='application/json', data=jsonpickle.encode(self.new_gc_dict))
    responseData = rv.data.decode('utf-8')
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertGreater(ackMsg.find('created'),-1,'Goal contribution not created')
    url = '/api/goal_contributions/source/' + quote(self.existing_src_name) + '/target/' + quote(self.existing_tgt_name) + '?session_id=test'
    rv = self.app.delete(url)


  def test_put(self):
    method = 'test_put'
    rv = self.app.post('/api/goal_contributions', content_type='application/json', data=jsonpickle.encode(self.new_gc_dict))
    self.new_gc_dict['object'].theContribution = 'Hurt'
    url = '/api/goal_contributions/source/' + quote(self.existing_src_name) + '/target/' + quote(self.existing_tgt_name) + '?session_id=test'
    rv = self.app.put(url, content_type='application/json', data=jsonpickle.encode(self.new_gc_dict))
    responseData = rv.data.decode('utf-8')
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertGreater(ackMsg.find('updated'),-1,'Goal contribution not updated')
    rv = self.app.delete(url)

  def test_delete(self):
    method = 'test_delete'
    rv = self.app.post('/api/goal_contributions', content_type='application/json', data=jsonpickle.encode(self.new_gc_dict))
    responseData = rv.data.decode('utf-8')
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)

    url = '/api/goal_contributions/source/' + quote(self.existing_src_name) + '/target/' + quote(self.existing_tgt_name) + '?session_id=test'
    rv = self.app.delete(url)
    responseData = rv.data.decode('utf-8')
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertGreater(ackMsg.find('deleted'),-1,'Goal contribution not deleted')
