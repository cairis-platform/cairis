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
import jsonpickle
from cairis.tools.JsonConverter import json_deserialize
from cairis.core.Goal import Goal
from cairis.core.GoalEnvironmentProperties import GoalEnvironmentProperties
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
from cairis.tools.ModelDefinitions import RefinementModel
import os
from cairis.mio.ModelImport import importModelFile

__author__ = 'Robin Quetin, Shamal Faily'

class GoalAPITests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/NeuroGrid/NeuroGrid.xml',1,'test')

  def setUp(self):
    self.logger = logging.getLogger(__name__)
    self.existing_goal_name = 'Multi-Factor Authentication'
    self.existing_category = 'Maintain'
    self.existing_environment_name_1 = 'Stroke'
    self.existing_environment_name_2 = 'Psychosis'
    self.goal_class = Goal.__module__+'.'+Goal.__name__
    self.to_delete_ids = []

  def test_get_all(self):
    method = 'test_get_all'
    rv = self.app.get('/api/goals?session_id=test')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    goals = jsonpickle.decode(responseData)
    self.assertIsNotNone(goals, 'No results after deserialization')
    self.assertIsInstance(goals, list, 'The result is not a list as expected')
    self.assertGreater(len(goals), 0, 'No goals in the dictionary')
    self.logger.info('[%s] Goals found: %d', method, len(goals))
    goal = goals[0]
    self.logger.info('[%s] First goal: %s\n', method, goal['theName'])

  def test_get_all_summary(self):
    method = 'test_get_all_summary'
    rv = self.app.get('/api/goals/summary?session_id=test')
    if (sys.version_info > (3,)):
      goals = json_deserialize(rv.data.decode('utf-8'))
    else:
      goals = json_deserialize(rv.data)
    self.assertIsNotNone(goals, 'No results after deserialization')
    self.assertGreater(len(goals), 0, 'No goal summaries')
    self.logger.info('[%s] Goals found: %d', method, len(goals))
    self.logger.info('[%s] First goal summary: %s \n', method, goals[0]['theName'])

  def test_get_all_coloured(self):
    method = 'test_get_all_coloured'
    rv = self.app.get('/api/goals?session_id=test&coloured=1')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    goals = jsonpickle.decode(responseData)
    self.assertIsNotNone(goals, 'No results after deserialization')
    self.assertIsInstance(goals, list, 'The result is not a list as expected')
    self.assertGreater(len(goals), 0, 'No goals in the list')
    self.logger.info('[%s] Goals found: %d', method, len(goals))
    goal = goals[0]
    self.logger.info('[%s] First goal: %s\n', method, goal['theName'])

  def test_get_by_name(self):
    method = 'test_get_by_name'
    url = '/api/goals/name/%s?session_id=test' % quote(self.existing_goal_name)
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    goal = jsonpickle.decode(responseData)
    self.assertIsNotNone(goal, 'No results after deserialization')
    self.logger.info('[%s] Goal: %s\n', method, goal['theName'])
    
  def test_delete(self):
    method = 'test_delete'
    url = '/api/goals/name/%s?session_id=test' % quote(self.prepare_new_goal().theName)
    new_goal_body = self.prepare_json()
    
    self.app.delete(url)
    self.logger.info('[%s] Object to delete: %s', method, new_goal_body)
    self.app.post('/api/goals', content_type='application/json', data=new_goal_body)
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.delete(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.info('[%s] Response data: %s', method, responseData)
    self.assertIsNotNone(responseData, 'No response')
    json_resp = jsonpickle.decode(responseData)
    self.assertIsInstance(json_resp, dict, 'The response cannot be converted to a dictionary')
    message = json_resp.get('message', None)
    self.assertIsNotNone(message, 'No message in response')
    self.logger.info('[%s] Message: %s\n', method, message)
    
  def test_post(self):
    method = 'test_post'
    url = '/api/goals'
    self.logger.info('[%s] URL: %s', method, url)
    new_goal_body = self.prepare_json()
    
    self.app.delete('/api/goals/name/%s?session_id=test' % quote(self.prepare_new_goal().theName))
    rv = self.app.post(url, content_type='application/json', data=new_goal_body)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    msg = json_resp.get('message', None)
    self.assertIsNotNone(msg, 'No message returned')
    self.logger.info('[%s] Message: %s\n', method, msg)
    
    rv = self.app.delete('/api/goals/name/%s?session_id=test' % quote(self.prepare_new_goal().theName))
    
  def test_put(self):
    method = 'test_put'
    url = '/api/goals'
    self.logger.info('[%s] URL: %s', method, url)
    new_goal_body = self.prepare_json()
    
    rv = self.app.delete('/api/goals/name/%s?session_id=test' % quote(self.prepare_new_goal().theName))
    rv = self.app.post(url, content_type='application/json', data=new_goal_body)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    msg = json_resp.get('message', None)
    self.assertIsNotNone(msg, 'No message returned')
    self.logger.info('[%s] Message: %s', method, msg)
    
    goal_to_update = self.prepare_new_goal()
    goal_to_update.theName = 'Edited test goal'
    upd_env_body = self.prepare_json(goal=goal_to_update)
    rv = self.app.put('/api/goals/name/%s?session_id=test' % quote(self.prepare_new_goal().theName), data=upd_env_body, content_type='application/json')
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp)
    self.assertIsInstance(json_resp, dict)
    message = json_resp.get('message', None)
    self.assertIsNotNone(message, 'No message in response')
    self.logger.info('[%s] Message: %s', method, message)
    self.assertGreater(message.find('updated'), -1, 'The goal was not successfully updated')
    
    rv = self.app.get('/api/goals/name/%s?session_id=test' % quote(goal_to_update.theName))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    upd_goal = jsonpickle.decode(responseData)
    self.assertIsNotNone(upd_goal, 'Unable to decode JSON data')
    self.logger.debug('[%s] Response data: %s', method, responseData)
    self.logger.info('[%s] Goal: %s\n', method, upd_goal['theName'])
  
    rv = self.app.delete('/api/goals/name/%s?session_id=test' % quote(goal_to_update.theName))

  def test_get_goal_concerns(self):
    method = 'test_get_goal_concerns'
    rv = self.app.get('/api/goals/name/Active%20Directory%20Network%20Services/environment/Day/concerns?session_id=test')
    concerns = json_deserialize(rv.data.decode('utf-8'))
    self.assertIsNotNone(concerns, 'No results after deserialization')
    self.assertGreater(len(concerns), 0, 'No concerns')
    self.assertEqual(len(concerns),3)

  def prepare_new_goal(self):
    new_goal_refinements = [
      RefinementModel("PreventUnauthorised Certificate Access",
      "goal",
      "or",
      "No",
      "None")
    ]
    new_subgoal_refinements = [
      RefinementModel("PreventUnauthorised Certificate Access",
      "goal",
      "or",
      "No",
      "None")
    ]
    new_goal_props = [
      GoalEnvironmentProperties(
        environmentName=self.existing_environment_name_1,
        lbl='',
        definition='This is a first test property',
        category=self.existing_category,
        priority='Medium',
        fitCriterion='None',
        issue='None',
        goalRefinements=new_goal_refinements,
        subGoalRefinements=new_subgoal_refinements,
        concs=[],cas=[]
      ),
      GoalEnvironmentProperties(
        environmentName=self.existing_environment_name_2,
        lbl='',
        definition='This is a second test property',
        category=self.existing_category,
        priority='Low',
        fitCriterion='None',
        issue='Test issue',
        goalRefinements=[],
        subGoalRefinements=[],
        concs=[],cas=[]
      )
    ]

    new_goal = Goal(
      goalId=-1,
      goalName='Test goal',
      goalOrig='',
      tags=['test', 'test123'],
      environmentProperties=[]
    )
    new_goal.theEnvironmentProperties = new_goal_props

    new_goal.theEnvironmentDictionary = {}
    new_goal.theGoalPropertyDictionary = {}

    delattr(new_goal, 'theEnvironmentDictionary')
    delattr(new_goal, 'theGoalPropertyDictionary')

    return new_goal

  def prepare_dict(self, goal=None):
    if goal is None:
      goal = self.prepare_new_goal()
    else:
      assert isinstance(goal, Goal)

    return {
      'session_id': 'test',
      'object': goal,
    }

  def prepare_json(self, data_dict=None, goal=None):
    if data_dict is None:
      data_dict = self.prepare_dict(goal=goal)
    else:
      assert isinstance(data_dict, dict)
    new_goal_body = jsonpickle.encode(data_dict, unpicklable=False)
    self.logger.info('JSON data: %s', new_goal_body)
    return new_goal_body
