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
from cairis.core.Environment import Environment
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
from cairis.tools.PseudoClasses import EnvironmentTensionModel
from cairis.mio.ModelImport import importModelFile
import os

__author__ = 'Robin Quetin, Shamal Faily'


class EnvironmentAPITests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/NeuroGrid/NeuroGrid.xml',1,'test')


  def setUp(self):
    self.logger = logging.getLogger(__name__)
    self.existing_environment_name = 'Stroke'
    self.environment_class = Environment.__module__+'.'+Environment.__name__
    
  def test_get_environment_names_by_threat_vulnerability(self):
    method = 'test_get_environment_names_by_threat_vulnerability'
    rv = self.app.get('/api/environments/threat/Trojan%20Horse/vulnerability/Workflow%20channel/names?session_id=test')
    responseData = rv.data.decode('utf-8')
    names = jsonpickle.decode(responseData)
    self.assertIsNotNone(names, 'No results after deserialization')
    self.assertIsInstance(names, list, 'The result is not a list as expected')
    self.assertGreater(len(names), 0, 'No environments in the list')
    self.assertEqual(len(names),3)

  def test_get_environment_names_by_vulnerability_threat(self):
    method = 'test_get_environment_names_by_threat_vulnerability'
    rv = self.app.get('/api/environments/vulnerability/Workflow%20channel/threat/Trojan%20Horse/names?session_id=test')
    responseData = rv.data.decode('utf-8')
    names = jsonpickle.decode(responseData)
    self.assertIsNotNone(names, 'No results after deserialization')
    self.assertIsInstance(names, list, 'The result is not a list as expected')
    self.assertGreater(len(names), 0, 'No environments in the list')
    self.assertEqual(len(names),3)

  def test_get_all(self):
    method = 'test_get_all'
    rv = self.app.get('/api/environments?session_id=test')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    environments = jsonpickle.decode(responseData)
    self.assertIsNotNone(environments, 'No results after deserialization')
    self.assertIsInstance(environments, list, 'The result is not a list as expected')
    self.assertGreater(len(environments), 0, 'No environments in the dictionary')
    self.logger.info('[%s] Environments found: %d', method, len(environments))
    environment = environments[0]
    self.logger.info('[%s] First environment: %s\n', method, environment['theName'])

  def test_get_all_names(self):
    method = 'test_get_all_names'
    rv = self.app.get('/api/environments/all/names?session_id=test')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    environments = jsonpickle.decode(responseData)
    self.assertIsNotNone(environments, 'No results after deserialization')
    self.assertIsInstance(environments, list, 'The result is not a list as expected')
    self.assertGreater(len(environments), 0, 'No environments in the list')
    self.logger.info('[%s] Environments found: %d', method, len(environments))
    list_str = ' - '.join(environments)
    self.logger.info('[%s] Environment names: %s\n', method, list_str)

  def test_get_names_by_risk(self):
    method = 'test_get_names_by_risk'
    riskName = 'User Certificate Theft'
    url = '/api/environments/risk/%s/names?session_id=test' % quote(riskName)
    rv = self.app.get(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    environments = jsonpickle.decode(responseData)
    self.assertIsNotNone(environments, 'No results after deserialization')
    self.assertIsInstance(environments, list, 'The result is not a list as expected')
    self.assertGreater(len(environments), 0, 'No environments in the list')
    self.logger.info('[%s] Environments found: %d', method, len(environments))
    list_str = ' - '.join(environments)
    self.logger.info('[%s] Environment names: %s\n', method, list_str)

  def test_get_by_name(self):
    method = 'test_get_by_name'
    url = '/api/environments/name/%s?session_id=test' % quote(self.existing_environment_name)
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    environment = jsonpickle.decode(responseData)
    self.assertIsNotNone(environment, 'No results after deserialization')
    self.logger.info('[%s] Environment: %s\n', method, environment['theName'])

  def test_delete(self):
    method = 'test_delete'
    url = '/api/environments/name/%s?session_id=test' % quote(self.prepare_new_environment().theName)
    new_environment_body = self.prepare_json()

    self.app.delete(url)
    self.logger.info('[%s] Object to delete: %s', method, new_environment_body)
    self.app.post('/api/environments', content_type='application/json', data=new_environment_body)
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.delete(url)
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    json_resp = jsonpickle.decode(responseData)
    self.assertIsInstance(json_resp, dict, 'The response cannot be converted to a dictionary')
    message = json_resp.get('message', None)
    self.assertIsNotNone(message, 'No message in response')
    self.logger.info('[%s] Message: %s\n', method, message)

  def test_post(self):
    method = 'test_post'
    url = '/api/environments'
    self.logger.info('[%s] URL: %s', method, url)
    new_environment_body = self.prepare_json()

    self.app.delete('/api/environments/name/%s?session_id=test' % quote(self.prepare_new_environment().theName))
    rv = self.app.post(url, content_type='application/json', data=new_environment_body)
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
    rv = self.app.delete('/api/environments/name/%s?session_id=test' % quote(self.prepare_new_environment().theName))

  def test_put(self):
    method = 'test_put'
    url = '/api/environments'
    self.logger.info('[%s] URL: %s', method, url)
    new_environment_body = self.prepare_json()

    rv = self.app.delete('/api/environments/name/%s?session_id=test' % quote(self.prepare_new_environment().theName))
    rv = self.app.post(url, content_type='application/json', data=new_environment_body)
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

    environment_to_update = self.prepare_new_environment()
    environment_to_update.theName = 'Edited test environment'
    upd_env_body = self.prepare_json(environment=environment_to_update)
    rv = self.app.put('/api/environments/name/%s?session_id=test' % quote(self.prepare_new_environment().theName), data=upd_env_body, content_type='application/json')
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
    self.assertGreater(message.find('updated'), -1, 'The environment was not successfully updated')

    rv = self.app.get('/api/environments/name/%s?session_id=test' % quote(environment_to_update.theName))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    upd_environment = jsonpickle.decode(responseData)
    self.assertIsNotNone(upd_environment, 'Unable to decode JSON data')
    self.logger.debug('[%s] Response data: %s', method, responseData)
    self.logger.info('[%s] Environment: %s\n', method, upd_environment['theName'])
    rv = self.app.delete('/api/environments/name/%s?session_id=test' % quote(environment_to_update.theName))


  def test_put_composite(self):
    method = 'test_put_composite'
    url = '/api/environments?session_id=test'
    new_environment_body = self.prepare_json(comp_env=True)
    rv = self.app.post(url, content_type='application/json', data=new_environment_body)
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

    environment_to_update = self.prepare_comp_environment()
    environment_to_update.theName = 'Edited test environment'
    upd_env_body = self.prepare_json(environment=environment_to_update)
    rv = self.app.put('/api/environments/name/%s?session_id=test' % quote(self.prepare_comp_environment().theName), data=upd_env_body, content_type='application/json')
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
    self.assertGreater(message.find('updated'), -1, 'The environment was not successfully updated')

    rv = self.app.get('/api/environments/name/%s?session_id=test' % quote(environment_to_update.theName))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    upd_environment = jsonpickle.decode(responseData)
    self.assertIsNotNone(upd_environment, 'Unable to decode JSON data')
    self.logger.debug('[%s] Response data: %s', method, responseData)
    self.logger.info('[%s] Environment: %s\n', method, upd_environment['theName'])
    rv = self.app.delete('/api/environments/name/%s?session_id=test' % quote(environment_to_update.theName))


  def prepare_comp_environment(self):
    new_environment = Environment(
      id=-1,
      name='Complete',
      sc='ALL',
      description='This is a test description',
      environments=['Psychosis','Stroke','Core Technology'],
      duplProperty='Maximise',
      overridingEnvironment='',
      envTensions=[]
    )
    return new_environment

  def prepare_new_environment(self):
    new_environment = Environment(
      id=-1,
      name='Test environment',
      sc='TEST',
      description='This is a test description',
      environments=[],
      duplProperty='',
      overridingEnvironment='',
      envTensions=[]
    )

    for idx1 in range(0, 4):
      for idx2 in range(4, 8):
        tension = EnvironmentTensionModel(
                    base_attr_id=idx1,
                    attr_id=idx2,
                    value=0,
                    rationale='None'
                  )
        new_environment.theTensions.append(tension)

    return new_environment

  def prepare_dict(self, environment=None,comp_env=False):
    if environment is None:
      if comp_env == False:
        environment = self.prepare_new_environment()
      else:
        environment = self.prepare_comp_environment()
    else:
      assert isinstance(environment, Environment)

    return {
      'session_id': 'test',
      'object': environment,
    }

  def prepare_json(self, data_dict=None, environment=None,comp_env=False):
    if data_dict is None:
      data_dict = self.prepare_dict(environment=environment,comp_env=comp_env)
    else:
      assert isinstance(data_dict, dict)
    new_environment_body = jsonpickle.encode(data_dict)
    self.logger.info('JSON data: %s', new_environment_body)
    return new_environment_body
