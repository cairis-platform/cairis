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
import jsonpickle
from cairis.core.Goal import Goal
from cairis.core.GoalEnvironmentProperties import GoalEnvironmentProperties
from cairis.web_tests.CairisTests import CairisTests

__author__ = 'Robin Quetin'


class GoalTests(CairisTests):
    # region Class fields
    logger = logging.getLogger(__name__)
    existing_goal_id = 532
    existing_goal_name = 'Multi-Factor Authentication'
    existing_category = 'Maintain'
    existing_environment_name_1 = 'Stroke'
    existing_environment_name_2 = 'Psychosis'
    goal_class = Goal.__module__+'.'+Goal.__name__
    to_delete_ids = []
    # endregion

    def test_get_all(self):
        method = 'test_get_all'
        rv = self.app.get('/api/goals?session_id=test')
        goals = jsonpickle.decode(rv.data)
        self.assertIsNotNone(goals, 'No results after deserialization')
        self.assertIsInstance(goals, dict, 'The result is not a dictionary as expected')
        self.assertGreater(len(goals), 0, 'No goals in the dictionary')
        self.logger.info('[%s] Goals found: %d', method, len(goals))
        goal = goals.values()[0]
        self.logger.info('[%s] First goal: %s [%d]\n', method, goal['theName'], goal['theId'])
    
    def test_get_by_name(self):
        method = 'test_get_by_name'
        url = '/api/goals/name/%s?session_id=test' % quote(self.existing_goal_name)
        rv = self.app.get(url)
        self.assertIsNotNone(rv.data, 'No response')
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        goal = jsonpickle.decode(rv.data)
        self.assertIsNotNone(goal, 'No results after deserialization')
        self.logger.info('[%s] Goal: %s [%d]\n', method, goal['theName'], goal['theId'])
    
    def test_delete(self):
        method = 'test_delete'
        url = '/api/goals/name/%s?session_id=test' % quote(self.prepare_new_goal().theName)
        new_goal_body = self.prepare_json()
    
        self.app.delete(url)
        self.logger.info('[%s] Object to delete: %s', method, new_goal_body)
        self.app.post('/api/goals', content_type='application/json', data=new_goal_body)
        self.logger.info('[%s] URL: %s', method, url)
        rv = self.app.delete(url)
        self.logger.info('[%s] Response data: %s', method, rv.data)
        self.assertIsNotNone(rv.data, 'No response')
        json_resp = jsonpickle.decode(rv.data)
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
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        json_resp = jsonpickle.decode(rv.data)
        self.assertIsNotNone(json_resp, 'No results after deserialization')
        env_id = json_resp.get('goal_id', None)
        self.assertIsNotNone(env_id, 'No goal ID returned')
        self.assertGreater(env_id, 0, 'Invalid goal ID returned [%d]' % env_id)
        self.logger.info('[%s] Goal ID: %d\n', method, env_id)
    
        rv = self.app.delete('/api/goals/name/%s?session_id=test' % quote(self.prepare_new_goal().theName))
    
    def test_put(self):
        method = 'test_put'
        url = '/api/goals'
        self.logger.info('[%s] URL: %s', method, url)
        new_goal_body = self.prepare_json()
    
        rv = self.app.delete('/api/goals/name/%s?session_id=test' % quote(self.prepare_new_goal().theName))
        rv = self.app.post(url, content_type='application/json', data=new_goal_body)
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        json_resp = jsonpickle.decode(rv.data)
        self.assertIsNotNone(json_resp, 'No results after deserialization')
        env_id = json_resp.get('goal_id', None)
        self.assertIsNotNone(env_id, 'No goal ID returned')
        self.assertGreater(env_id, 0, 'Invalid goal ID returned [%d]' % env_id)
        self.logger.info('[%s] Goal ID: %d', method, env_id)
    
        goal_to_update = self.prepare_new_goal()
        goal_to_update.theName = 'Edited test goal'
        goal_to_update.theId = env_id
        upd_env_body = self.prepare_json(goal=goal_to_update)
        rv = self.app.put('/api/goals/name/%s?session_id=test' % quote(self.prepare_new_goal().theName), data=upd_env_body, content_type='application/json')
        self.assertIsNotNone(rv.data, 'No response')
        json_resp = jsonpickle.decode(rv.data)
        self.assertIsNotNone(json_resp)
        self.assertIsInstance(json_resp, dict)
        message = json_resp.get('message', None)
        self.assertIsNotNone(message, 'No message in response')
        self.logger.info('[%s] Message: %s', method, message)
        self.assertGreater(message.find('successfully updated'), -1, 'The goal was not successfully updated')
    
        rv = self.app.get('/api/goals/name/%s?session_id=test' % quote(goal_to_update.theName))
        upd_goal = jsonpickle.decode(rv.data)
        self.assertIsNotNone(upd_goal, 'Unable to decode JSON data')
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        self.logger.info('[%s] Goal: %s [%d]\n', method, upd_goal['theName'], upd_goal['theId'])
    
        rv = self.app.delete('/api/goals/name/%s?session_id=test' % quote(goal_to_update.theName))

    def prepare_new_goal(self):
        new_goal_refinements = [
            [
                "PreventUnauthorised Certificate Access",
                "goal",
                "or",
                "No",
                "None"
            ]
        ]
        new_subgoal_refinements = [
            [
                "PreventUnauthorised Certificate Access",
                "goal",
                "or",
                "No",
                "None"
            ]
        ]
        new_goal_props = [
            GoalEnvironmentProperties(
                environmentName=self.existing_environment_name_1,
                lbl='Test 1',
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
                lbl='Test 2',
                definition='This is a second test property',
                category=self.existing_category,
                priority='Low',
                fitCriterion='None',
                issue='Test issue',
                goalRefinements=new_goal_refinements,
                subGoalRefinements=new_subgoal_refinements,
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
