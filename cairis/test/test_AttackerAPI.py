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
from cairis.core.Attacker import Attacker
from cairis.tools.JsonConverter import json_deserialize
from cairis.core.AttackerEnvironmentProperties import AttackerEnvironmentProperties
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
import os
from cairis.mio.ModelImport import importModelFile

__author__ = 'Robin Quetin, Shamal Faily'


class AttackerAPITests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/NeuroGrid/NeuroGrid.xml',1,'test')

  
  def setUp(self):
    # region Class fields
    self.logger = logging.getLogger(__name__)
    self.existing_attacker_name = 'Mallory'
    self.existing_environment_name_1 = 'Stroke'
    self.existing_environment_name_2 = 'Psychosis'
    self.existing_motive_names = ['Hactivism', 'Money']
    self.existing_role_names = ['Hacker', 'Developer']
    self.existing_capabilities = [
      {
        'name':'Resources/Equipment',
        'value': 'Low'
      },
      {
        'name': 'Knowledge/Methods',
        'value': 'High'
      }
    ]
    attacker_class = Attacker.__module__+'.'+Attacker.__name__
    # endregion

  def test_get_all(self):
    method = 'test_get_all'
    rv = self.app.get('/api/attackers?session_id=test')
    if (sys.version_info > (3,)):
      attackers = jsonpickle.decode(rv.data.decode('utf-8'))
    else:
      attackers = jsonpickle.decode(rv.data)
    self.assertIsNotNone(attackers, 'No results after deserialization')
    self.assertIsInstance(attackers, dict, 'The result is not a dictionary as expected')
    self.assertGreater(len(attackers), 0, 'No attackers in the dictionary')
    self.logger.info('[%s] Attackers found: %d', method, len(attackers))
    attacker = list(attackers.values())[0]
    self.logger.info('[%s] First attacker: %s\n', method, attacker['theName'])

  def test_get_all_summary(self):
    method = 'test_get_all_summary'
    rv = self.app.get('/api/attackers/summary?session_id=test')
    if (sys.version_info > (3,)):
      ats = json_deserialize(rv.data.decode('utf-8'))
    else:
      ats = json_deserialize(rv.data)
    self.assertIsNotNone(ats, 'No results after deserialization')
    self.assertGreater(len(ats), 0, 'No attacker summaries')
    self.assertIsInstance(ats[0], dict)
    self.logger.info('[%s] Attackers found: %d', method, len(ats))
    self.logger.info('[%s] First attacker summary: %s [%s]\n', method, ats[0]['theName'])

  def test_get_by_name(self):
    method = 'test_get_by_name'
    url = '/api/attackers/name/%s?session_id=test' % quote(self.existing_attacker_name)
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    self.logger.debug('[%s] Response data: %s', method, rv.data)
    if (sys.version_info > (3,)):
      attacker = jsonpickle.decode(rv.data.decode('utf-8'))
    else:
      attacker = jsonpickle.decode(rv.data)
    self.assertIsNotNone(attacker, 'No results after deserialization')
    self.logger.info('[%s] Attacker: %s\n', method, attacker['theName'])

  def test_delete(self):
    method = 'test_delete'
    url = '/api/attackers/name/%s?session_id=test' % quote(self.prepare_new_attacker().theName)
    new_attacker_body = self.prepare_json()

    self.app.delete(url)

    self.logger.info('[%s] Object to delete: %s', method, new_attacker_body)
    self.app.post('/api/attackers', content_type='application/json', data=new_attacker_body)
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
    url = '/api/attackers'
    self.logger.info('[%s] URL: %s', method, url)
    new_attacker_body = self.prepare_json()

    self.app.delete('/api/attackers/name/%s?session_id=test' % quote(self.prepare_new_attacker().theName))
    rv = self.app.post(url, content_type='application/json', data=new_attacker_body)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')

    rv = self.app.delete('/api/attackers/name/%s?session_id=test' % quote(self.prepare_new_attacker().theName))

  def test_put(self):
    method = 'test_put'
    url = '/api/attackers'
    self.logger.info('[%s] URL: %s', method, url)
    new_attacker_body = self.prepare_json()

    rv = self.app.delete('/api/attackers/name/%s?session_id=test' % quote(self.prepare_new_attacker().theName))
    rv = self.app.post(url, content_type='application/json', data=new_attacker_body)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')

    attacker_to_update = self.prepare_new_attacker()
    attacker_to_update.theName = 'Edited test attacker'
    attacker_to_update.theId = -1
    upd_env_body = self.prepare_json(attacker=attacker_to_update)
    rv = self.app.put('/api/attackers/name/%s?session_id=test' % quote(self.prepare_new_attacker().theName), data=upd_env_body, content_type='application/json')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.assertIsNotNone(responseData, 'No response')
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp)
    self.assertIsInstance(json_resp, dict)
    message = json_resp.get('message', None)
    self.assertIsNotNone(message, 'No message in response')
    self.logger.info('[%s] Message: %s', method, message)
    self.assertGreater(message.find('updated'), -1, 'The attacker was not successfully updated')

    rv = self.app.get('/api/attackers/name/%s?session_id=test' % quote(attacker_to_update.theName))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    upd_attacker = jsonpickle.decode(responseData)
    self.assertIsNotNone(upd_attacker, 'Unable to decode JSON data')
    self.logger.debug('[%s] Response data: %s', method, responseData)
    self.logger.info('[%s] Attacker: %s\n', method, upd_attacker['theName'])

    rv = self.app.delete('/api/attackers/name/%s?session_id=test' % quote(attacker_to_update.theName))

  def prepare_new_attacker(self):
    new_attacker_props = [
      AttackerEnvironmentProperties(
        environmentName=self.existing_environment_name_1,
        roles=self.existing_role_names,
        motives=self.existing_motive_names,
        capabilities=self.existing_capabilities
      ),
      AttackerEnvironmentProperties(
        environmentName=self.existing_environment_name_2,
        roles=self.existing_role_names,
        motives=self.existing_motive_names,
        capabilities=self.existing_capabilities
      )
    ]

    new_attacker = Attacker(
      attackerId=-1,
      attackerName='Test attacker',
      attackerDescription='This is a test attacker',
      attackerImage='',
      tags=['test', 'test123'],
      environmentProperties=[]
    )
    new_attacker.theEnvironmentProperties = new_attacker_props

    new_attacker.theEnvironmentDictionary = {}
    new_attacker.theAttackerPropertyDictionary = {}

    delattr(new_attacker, 'theEnvironmentDictionary')
    delattr(new_attacker, 'theAttackerPropertyDictionary')

    return new_attacker

  def prepare_dict(self, attacker=None):
    if attacker is None:
      attacker = self.prepare_new_attacker()
    else:
      assert isinstance(attacker, Attacker)

    return {
      'session_id': 'test',
      'object': attacker,
    }

  def prepare_json(self, data_dict=None, attacker=None):
    if data_dict is None:
      data_dict = self.prepare_dict(attacker=attacker)
    else:
      assert isinstance(data_dict, dict)
    new_attacker_body = jsonpickle.encode(data_dict, unpicklable=False)
    self.logger.info('JSON data: %s', new_attacker_body)
    return new_attacker_body
