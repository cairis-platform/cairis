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
from cairis.core.GoalAssociation import GoalAssociation
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
from cairis.mio.ModelImport import importModelFile
from cairis.tools.JsonConverter import json_deserialize
import os

__author__ = 'Shamal Faily'

class GoalAssociationAPITests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/NeuroGrid/NeuroGrid.xml',1,'test')


  def setUp(self):
    self.logger = logging.getLogger(__name__)
    self.new_assoc = GoalAssociation(
      associationId = '-1',
      envName = 'Psychosis',
      goalName = 'Download analysis data',
      goalDimName = 'goal',
      aType = 'and',
      subGoalName = 'Data-set access',
      subGoalDimName = 'goal',
      alternativeId = '0',
      rationale = 'None')
    self.new_assoc_dict = {
      'session_id' : 'test',
      'object': self.new_assoc
    }

  def test_get(self):
    method = 'test_goal_association'
    url = '/api/goals/association/environment/Psychosis/goal/Upload%20clinical%20data%20to%20NeuroGrid/subgoal/Secure%20data%20transmission?session_id=test'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    assoc = jsonpickle.decode(responseData)
    self.assertIsNotNone(assoc, 'No results after deserialization')
    self.assertEqual(assoc['theGoal'],'Upload clinical data to NeuroGrid')
    self.assertEqual(assoc['theSubGoal'],'Secure data transmission')

  def test_get_all(self):
    method = 'test_goal_associations'
    url = '/api/goals/association?environment_name=Core%20Technology&session_id=test'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    assocs = jsonpickle.decode(responseData)
    self.assertIsNotNone(assocs, 'No results after deserialization')
    self.assertEqual(len(assocs), 6)

  def test_post_self_refine(self):
    assoc = self.new_assoc_dict
    assoc['object'].theSubGoal = assoc['object'].theGoal
    method = 'test_post_self_refine'
    rv = self.app.post('/api/goals/association', content_type='application/json', data=jsonpickle.encode(assoc))
    msg = json_deserialize(rv.data)
    self.assertEqual(msg['code'],400)

  def test_post(self):
    method = 'test_post_new'
    rv = self.app.post('/api/goals/association', content_type='application/json', data=jsonpickle.encode(self.new_assoc_dict))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertGreater(ackMsg.find('created'),-1,'Goal association not created')

  def test_put_self_refine(self):
    method = 'test_put'
    self.new_assoc_dict['object'].theGoal = self.new_assoc_dict['object'].theSubGoal
    url = '/api/goals/association/environment/Psychosis/goal/Upload%20clinical%20data%20to%20NeuroGrid/subgoal/Secure%20data%20transmission?session_id=test'
    rv = self.app.put(url, content_type='application/json', data=jsonpickle.encode(self.new_assoc_dict))
    msg = json_deserialize(rv.data)
    self.assertEqual(msg['code'],400)

  def test_put(self):
    method = 'test_put'
    self.new_assoc_dict['object'].theAlternativeId = '1'
    url = '/api/goals/association/environment/Psychosis/goal/Upload%20clinical%20data%20to%20NeuroGrid/subgoal/Secure%20data%20transmission?session_id=test'
    rv = self.app.put(url, content_type='application/json', data=jsonpickle.encode(self.new_assoc_dict))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertGreater(ackMsg.find('updated'),-1,'Goal association not updated')

  def test_delete(self):
    method = 'test_delete'

    rv = self.app.post('/api/goals/association', content_type='application/json', data=jsonpickle.encode(self.new_assoc_dict))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)

    url = '/api/goals/association/environment/Psychosis/goal/Upload%20clinical%20data%20to%20NeuroGrid/subgoal/Anonymise%20data?session_id=test'
    rv = self.app.delete(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertGreater(ackMsg.find('deleted'),-1,'Goal association not deleted')
