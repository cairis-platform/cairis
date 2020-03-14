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
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    obstacles = jsonpickle.decode(responseData)
    self.assertIsNotNone(obstacles, 'No results after deserialization')
    self.assertIsInstance(obstacles, dict, 'The result is not a dictionary as expected')
    self.assertGreater(len(obstacles), 0, 'No obstacles in the dictionary')
    self.logger.info('[%s] Obstacles found: %d', method, len(obstacles))
    obstacle = list(obstacles.values())[0]
    self.logger.info('[%s] First obstacle: %s \n', method, obstacle['theName'])

  def test_get_all_summary(self):
    method = 'test_get_all_summary'
    rv = self.app.get('/api/obstacles/summary?session_id=test')
    if (sys.version_info > (3,)):
      obs = json_deserialize(rv.data.decode('utf-8'))
    else:
      obs = json_deserialize(rv.data)
    self.assertIsNotNone(obs, 'No results after deserialization')
    self.assertGreater(len(obs), 0, 'No goal summaries')
    self.logger.info('[%s] Obstacles found: %d', method, len(obs))
    self.logger.info('[%s] First obstacle summary: %s\n', method, obs[0]['theName'])
    
  def test_get_by_name(self):
    method = 'test_get_by_name'
    url = '/api/obstacles/name/%s?session_id=test' % quote(self.existing_obstacle_name)
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    obstacle = jsonpickle.decode(responseData)
    self.assertIsNotNone(obstacle, 'No results after deserialization')
    self.logger.info('[%s] Obstacle: %s \n', method, obstacle['theName'])
    
  def test_delete(self):
    method = 'test_delete'
    url = '/api/obstacles/name/%s?session_id=test' % quote(self.prepare_new_obstacle().theName)
    new_obstacle_body = self.prepare_json()

    
    self.app.delete(url)
    self.logger.info('[%s] Object to delete: %s', method, new_obstacle_body)
    self.app.post('/api/obstacles', content_type='application/json', data=new_obstacle_body)
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
    url = '/api/obstacles'
    self.logger.info('[%s] URL: %s', method, url)
    new_obstacle_body = self.prepare_json()
    
    rv = self.app.post(url, content_type='application/json', data=new_obstacle_body)
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
    
    rv = self.app.delete('/api/obstacles/name/%s?session_id=test' % quote(self.prepare_new_obstacle().theName))
    
  def test_put(self):
    method = 'test_put'
    url = '/api/obstacles'
    self.logger.info('[%s] URL: %s', method, url)
    new_obstacle_body = self.prepare_json()
    
    rv = self.app.post(url, content_type='application/json', data=new_obstacle_body)
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
    
    obstacle_to_update = self.prepare_new_obstacle()
    obstacle_to_update.theName = 'Edited test obstacle'
    upd_env_body = self.prepare_json(obstacle=obstacle_to_update)
    rv = self.app.put('/api/obstacles/name/%s?session_id=test' % quote(self.prepare_new_obstacle().theName), data=upd_env_body, content_type='application/json')
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
    self.assertGreater(message.find('updated'), -1, 'The obstacle was not successfully updated')
    
    rv = self.app.get('/api/obstacles/name/%s?session_id=test' % quote(obstacle_to_update.theName))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    upd_obstacle = jsonpickle.decode(responseData)
    self.assertIsNotNone(upd_obstacle, 'Unable to decode JSON data')
    self.logger.debug('[%s] Response data: %s', method, responseData)
    self.logger.info('[%s] Obstacle: %s\n', method, upd_obstacle['theName'])
    rv = self.app.delete('/api/obstacles/name/%s?session_id=test' % quote(obstacle_to_update.theName))

  def test_generate_vulnerability(self):
    method = 'test_generate_vulnerability'
    url = '/api/obstacles/name/' + quote(self.existing_obstacle_name) + '/generate_vulnerability?session_id=test'
    self.logger.info('[%s] URL: %s', method, url)

    rv = self.app.post(url, content_type='application/json',data=jsonpickle.encode({'session_id':'test'}))
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    self.assertIsInstance(json_resp, dict)
    message = json_resp.get('message', None)
    self.assertIsNotNone(message, 'No message in response')
    self.logger.info('[%s] Message: %s\n', method, message)
    self.assertGreater(message.find('successfully generated'), -1, 'Vulnerability not generated')


  def prepare_new_obstacle(self):
    return Obstacle(-1,'Test obstacle','test case',['test','test123'],[ObstacleEnvironmentProperties('Psychosis','New Obstacle','This a test definition for env1','Integrity Threat',[],[],[]),ObstacleEnvironmentProperties('Stroke','New Obstacle','This is a test definition for env2','Integrity Threat',[],[],[])])

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
