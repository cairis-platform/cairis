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
from cairis.core.Obstacle import Obstacle
from cairis.core.ObstacleEnvironmentProperties import ObstacleEnvironmentProperties
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
import os
from cairis.mio.ModelImport import importModelFile

__author__ = 'Shamal Faily'

class ObstacleAPITests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/NeuroGrid/NeuroGrid.xml',1,'test')


  def setUp(self):
    # region Class fields
    self.logger = logging.getLogger(__name__)
    self.existing_obstacle_name = 'Control web browser'
    self.existing_category = 'Confidentiality Threat'
    self.existing_environment_name_1 = 'Psychosis'
    self.existing_environment_name_2 = 'Stroke'
    self.obstacle_class = Obstacle.__module__+'.'+ Obstacle.__name__
    self.to_delete_ids = []
    # endregion

  def test_get_all(self):
    method = 'test_get_all'
    rv = self.app.get('/api/obstacles?session_id=test')
    obstacles = jsonpickle.decode(rv.data)
    self.assertIsNotNone(obstacles, 'No results after deserialization')
    self.assertIsInstance(obstacles, dict, 'The result is not a dictionary as expected')
    self.assertGreater(len(obstacles), 0, 'No obstacles in the dictionary')
    self.logger.info('[%s] Obstacles found: %d', method, len(obstacles))
    obstacle = obstacles.values()[0]
    self.logger.info('[%s] First obstacle: %s [%d]\n', method, obstacle['theName'], obstacle['theId'])
    
  def test_get_by_name(self):
    method = 'test_get_by_name'
    url = '/api/obstacles/name/%s?session_id=test' % quote(self.existing_obstacle_name)
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    self.logger.debug('[%s] Response data: %s', method, rv.data)
    obstacle = jsonpickle.decode(rv.data)
    self.assertIsNotNone(obstacle, 'No results after deserialization')
    self.logger.info('[%s] Obstacle: %s [%d]\n', method, obstacle['theName'], obstacle['theId'])
    
  def test_delete(self):
    method = 'test_delete'
    url = '/api/obstacles/name/%s?session_id=test' % quote(self.prepare_new_obstacle().theName)
    new_obstacle_body = self.prepare_json()

    
    self.app.delete(url)
    self.logger.info('[%s] Object to delete: %s', method, new_obstacle_body)
    self.app.post('/api/obstacles', content_type='application/json', data=new_obstacle_body)
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
    url = '/api/obstacles'
    self.logger.info('[%s] URL: %s', method, url)
    new_obstacle_body = self.prepare_json()
    
    rv = self.app.post(url, content_type='application/json', data=new_obstacle_body)
    self.logger.debug('[%s] Response data: %s', method, rv.data)
    json_resp = jsonpickle.decode(rv.data)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    env_id = json_resp.get('obstacle_id', None)
    self.assertIsNotNone(env_id, 'No obstacle ID returned')
    self.assertGreater(env_id, 0, 'Invalid obstacle ID returned [%d]' % env_id)
    self.logger.info('[%s] Obstacle ID: %d\n', method, env_id)
    
    rv = self.app.delete('/api/obstacles/name/%s?session_id=test' % quote(self.prepare_new_obstacle().theName))
    
  def test_put(self):
    method = 'test_put'
    url = '/api/obstacles'
    self.logger.info('[%s] URL: %s', method, url)
    new_obstacle_body = self.prepare_json()
    
    rv = self.app.post(url, content_type='application/json', data=new_obstacle_body)
    self.logger.debug('[%s] Response data: %s', method, rv.data)
    json_resp = jsonpickle.decode(rv.data)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    env_id = json_resp.get('obstacle_id', None)
    self.assertIsNotNone(env_id, 'No obstacle ID returned')
    self.assertGreater(env_id, 0, 'Invalid obstacle ID returned [%d]' % env_id)
    self.logger.info('[%s] Obstacle ID: %d', method, env_id)
    
    obstacle_to_update = self.prepare_new_obstacle()
    obstacle_to_update.theName = 'Edited test obstacle'
    obstacle_to_update.theId = env_id
    upd_env_body = self.prepare_json(obstacle=obstacle_to_update)
    rv = self.app.put('/api/obstacles/name/%s?session_id=test' % quote(self.prepare_new_obstacle().theName), data=upd_env_body, content_type='application/json')
    self.assertIsNotNone(rv.data, 'No response')
    json_resp = jsonpickle.decode(rv.data)
    self.assertIsNotNone(json_resp)
    self.assertIsInstance(json_resp, dict)
    message = json_resp.get('message', None)
    self.assertIsNotNone(message, 'No message in response')
    self.logger.info('[%s] Message: %s', method, message)
    self.assertGreater(message.find('successfully updated'), -1, 'The obstacle was not successfully updated')
    
    rv = self.app.get('/api/obstacles/name/%s?session_id=test' % quote(obstacle_to_update.theName))
    upd_obstacle = jsonpickle.decode(rv.data)
    self.assertIsNotNone(upd_obstacle, 'Unable to decode JSON data')
    self.logger.debug('[%s] Response data: %s', method, rv.data)
    self.logger.info('[%s] Obstacle: %s [%d]\n', method, upd_obstacle['theName'], upd_obstacle['theId'])
  
    rv = self.app.delete('/api/obstacles/name/%s?session_id=test' % quote(obstacle_to_update.theName))

  def prepare_new_obstacle(self):
    new_goal_refinements = []
    new_subgoal_refinements = []
    new_obs_props = [
      ObstacleEnvironmentProperties(
        environmentName=self.existing_environment_name_1,
        lbl='New Obstacle',
        definition='This is a test definition for env1',
        category='Integrity Threat',
        gRefs=new_goal_refinements,
        sgRefs=new_subgoal_refinements,
        concs=[]),
      ObstacleEnvironmentProperties(
        environmentName=self.existing_environment_name_2,
        lbl='New Obstacle',
        category='Integrity Threat',
        definition='This is a test definition for env2',
        gRefs=new_goal_refinements,
        sgRefs=new_subgoal_refinements,
        concs=[])
    ]

    new_obstacle = Obstacle(
      obsId=-1,
      obsName='Test obstacle',
      obsOrig='test case',
      tags=['test', 'test123'],
      environmentProperties=new_obs_props)
    return new_obstacle

  def prepare_dict(self, obstacle=None):
    if obstacle is None:
      obstacle = self.prepare_new_obstacle()
    else:
      assert isinstance(obstacle, Obstacle)

    return {
      'session_id': 'test',
      'object': obstacle,
    }

  def prepare_json(self, data_dict=None, obstacle=None):
    if data_dict is None:
      data_dict = self.prepare_dict(obstacle=obstacle)
    else:
      assert isinstance(data_dict, dict)
    new_obstacle_body = jsonpickle.encode(data_dict, unpicklable=False)
    self.logger.info('JSON data: %s', new_obstacle_body)
    return new_obstacle_body
