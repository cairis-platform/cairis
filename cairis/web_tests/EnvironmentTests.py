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
from cairis.core.Environment import Environment
from cairis.web_tests.CairisTests import CairisTests
from cairis.tools.PseudoClasses import EnvironmentTensionModel
from cairis.mio.ModelImport import importModelFile

__author__ = 'Robin Quetin'


class EnvironmentTests(CairisTests):
    # region Class fields
    logger = logging.getLogger(__name__)
    existing_environment_id = 117
    existing_environment_name = 'Stroke'
    environment_class = Environment.__module__+'.'+Environment.__name__
    # endregion

    def setUp(self):
        importModelFile('../../examples/exemplars/NeuroGrid/NeuroGrid.xml',1,'test')
    
    def test_get_all(self):
        method = 'test_get_all'
        rv = self.app.get('/api/environments?session_id=test')
        environments = jsonpickle.decode(rv.data)
        self.assertIsNotNone(environments, 'No results after deserialization')
        self.assertIsInstance(environments, dict, 'The result is not a dictionary as expected')
        self.assertGreater(len(environments), 0, 'No environments in the dictionary')
        self.logger.info('[%s] Environments found: %d', method, len(environments))
        environment = environments.values()[0]
        self.logger.info('[%s] First environment: %s [%d]\n', method, environment['theName'], environment['theId'])

    def test_get_all_names(self):
        method = 'test_get_all_names'
        rv = self.app.get('/api/environments/all/names?session_id=test')
        environments = jsonpickle.decode(rv.data)
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
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        environment = jsonpickle.decode(rv.data)
        self.assertIsNotNone(environment, 'No results after deserialization')
        self.logger.info('[%s] Environment: %s [%d]\n', method, environment['theName'], environment['theId'])

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
        json_resp = jsonpickle.decode(rv.data)
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
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        json_resp = jsonpickle.decode(rv.data)
        self.assertIsNotNone(json_resp, 'No results after deserialization')
        env_id = json_resp.get('environment_id', None)
        self.assertIsNotNone(env_id, 'No environment ID returned')
        self.assertGreater(env_id, 0, 'Invalid environment ID returned [%d]' % env_id)
        self.logger.info('[%s] Environment ID: %d\n', method, env_id)

        rv = self.app.delete('/api/environments/name/%s?session_id=test' % quote(self.prepare_new_environment().theName))

    def test_put(self):
        method = 'test_put'
        url = '/api/environments'
        self.logger.info('[%s] URL: %s', method, url)
        new_environment_body = self.prepare_json()

        rv = self.app.delete('/api/environments/name/%s?session_id=test' % quote(self.prepare_new_environment().theName))
        rv = self.app.post(url, content_type='application/json', data=new_environment_body)
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        json_resp = jsonpickle.decode(rv.data)
        self.assertIsNotNone(json_resp, 'No results after deserialization')
        env_id = json_resp.get('environment_id', None)
        self.assertIsNotNone(env_id, 'No environment ID returned')
        self.assertGreater(env_id, 0, 'Invalid environment ID returned [%d]' % env_id)
        self.logger.info('[%s] Environment ID: %d', method, env_id)

        environment_to_update = self.prepare_new_environment()
        environment_to_update.theName = 'Edited test environment'
        environment_to_update.theId = env_id
        upd_env_body = self.prepare_json(environment=environment_to_update)
        rv = self.app.put('/api/environments/name/%s?session_id=test' % quote(self.prepare_new_environment().theName), data=upd_env_body, content_type='application/json')
        self.assertIsNotNone(rv.data, 'No response')
        json_resp = jsonpickle.decode(rv.data)
        self.assertIsNotNone(json_resp)
        self.assertIsInstance(json_resp, dict)
        message = json_resp.get('message', None)
        self.assertIsNotNone(message, 'No message in response')
        self.logger.info('[%s] Message: %s', method, message)
        self.assertGreater(message.find('successfully updated'), -1, 'The environment was not successfully updated')

        rv = self.app.get('/api/environments/name/%s?session_id=test' % quote(environment_to_update.theName))
        upd_environment = jsonpickle.decode(rv.data)
        self.assertIsNotNone(upd_environment, 'Unable to decode JSON data')
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        self.logger.info('[%s] Environment: %s [%d]\n', method, upd_environment['theName'], upd_environment['theId'])

        rv = self.app.delete('/api/environments/name/%s?session_id=test' % quote(environment_to_update.theName))

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

    def prepare_dict(self, environment=None):
        if environment is None:
            environment = self.prepare_new_environment()
        else:
            assert isinstance(environment, Environment)

        return {
            'session_id': 'test',
            'object': environment,
        }

    def prepare_json(self, data_dict=None, environment=None):
        if data_dict is None:
            data_dict = self.prepare_dict(environment=environment)
        else:
            assert isinstance(data_dict, dict)
        new_environment_body = jsonpickle.encode(data_dict)
        self.logger.info('JSON data: %s', new_environment_body)
        return new_environment_body
