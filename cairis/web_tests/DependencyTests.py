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
import jsonpickle
from cairis.core.Dependency import Dependency
from cairis.web_tests.CairisTests import CairisTests
from cairis.tools.ModelDefinitions import DependencyModel

__author__ = 'Robin Quetin'


class DependencyTests(CairisTests):
    logger = logging.getLogger(__name__)
    working_name_1 = ('Stroke', 'all', 'all', 'all')
    working_name_2 = ('Stroke', 'Data%20Consumer', 'Certificate%20Authority', 'Personal%20certificate')
    existing_environment_1 = 'Stroke'
    existing_environment_2 = 'Psychosis'
    existing_role_1 = 'Data Consumer'
    existing_role_2 = 'Certificate Authority'
    existing_type = 'goal'
    existing_dependency = 'Upload authorisation'

    def test_all_get(self):
        method = 'test_all_get'
        url = '/api/dependencies?session_id=test'

        rv = self.app.get(url)
        self.assertIsNotNone(rv.data, 'No response')
        json_dict = jsonpickle.decode(rv.data)
        self.assertIsInstance(json_dict, dict, 'The response is not a valid JSON dictionary')
        self.assertGreater(len(json_dict), 0, 'No dependencies found')
        assert isinstance(json_dict, dict)
        item = json_dict.items()[0]
        self.logger.info('[%s] First dependency: %s [%d]\n', method, item[0], item[1]['theId'])

    def test_dependencies_name_get(self):
        method = 'test_dependencies_name_get'
        url = '/api/dependencies/environment/%s/depender/%s/dependee/%s/dependency/%s?session_id=test' % self.working_name_1

        rv = self.app.get(url)
        self.assertIsNotNone(rv.data, 'No response')
        json_dict = jsonpickle.decode(rv.data)
        self.assertIsInstance(json_dict, list, 'The response is not a valid JSON dictionary')
        self.assertGreater(len(json_dict), 0, 'No dependencies found')
        assert isinstance(json_dict, list)
        ids = []
        for dep in json_dict:
            ids.append(str(dep['theId']))
        self.logger.info('[%s] Dependency IDs: %s\n', method, ', '.join(ids))

    def test_dependency_name_get(self):
        method = 'test_dependency_name_get'
        url = '/api/dependencies/environment/%s/depender/%s/dependee/%s/dependency/%s?session_id=test' % self.working_name_2

        rv = self.app.get(url)
        self.assertIsNotNone(rv.data, 'No response')
        json_dict = jsonpickle.decode(rv.data)
        self.assertIsInstance(json_dict, list, 'The response is not a valid JSON dictionary')
        self.assertEqual(len(json_dict), 1, 'Result is not unique')
        assert isinstance(json_dict, list)
        item = json_dict[0]
        has_keys = all (k in item for k in DependencyModel.required)
        self.assertTrue(has_keys, 'Result is not a dependency')
        dep_name = '/'.join([item['theEnvironmentName'], item['theDepender'], item['theDependee'], item['theDependency']])
        self.logger.info('[%s] Dependency: %s [%d]\n', method, dep_name, item['theId'])

    def test_dependency_post(self):
        method = 'test_dependency_post'
        url = '/api/dependencies'
        new_dep = self.prepare_new_dependency()
        json_dict = {
            'session_id': 'test',
            'object': new_dep
        }
        json_body = jsonpickle.encode(json_dict)

        new_name = (new_dep.theEnvironmentName, new_dep.theDepender, new_dep.theDependee, new_dep.theDependency)
        delete_url = '/api/dependencies/environment/%s/depender/%s/dependee/%s/dependency/%s?session_id=test' % new_name
        self.app.delete(delete_url)

        rv = self.app.post(url, data=json_body, content_type='application/json')
        self.assertIsNotNone(rv.data, 'No response')
        json_dict = jsonpickle.decode(rv.data)
        self.assertIsInstance(json_dict, dict, 'Response is not a valid JSON dictionary')
        message = json_dict.get('message', None)
        self.assertIsNotNone(message, 'No message in response')
        self.assertNotIsInstance(message, dict, 'Message is an object')
        self.logger.info('[%s] Message: %s', method, message)
        dep_id = json_dict.get('dependency_id', None)
        self.assertIsNotNone(dep_id, 'No dependency ID returned')
        self.logger.info('[%s] New dependency ID: %d\n', method, dep_id)

        new_name = (new_dep.theEnvironmentName, new_dep.theDepender, new_dep.theDependee, new_dep.theDependency)
        delete_url = '/api/dependencies/environment/%s/depender/%s/dependee/%s/dependency/%s?session_id=test' % new_name
        self.app.delete(delete_url)

    def test_dependency_name_delete(self):
        method = 'test_dependency_name_delete'
        url = '/api/dependencies'
        new_dep = self.prepare_new_dependency()
        json_dict = {
            'session_id': 'test',
            'object': new_dep
        }
        json_body = jsonpickle.encode(json_dict)
        self.app.post(url, data=json_body, content_type='application/json')

        new_name = (new_dep.theEnvironmentName, new_dep.theDepender, new_dep.theDependee, new_dep.theDependency)
        delete_url = '/api/dependencies/environment/%s/depender/%s/dependee/%s/dependency/%s?session_id=test' % new_name
        rv = self.app.delete(delete_url)
        self.assertIsNotNone(rv.data, 'No response')
        json_dict = jsonpickle.decode(rv.data)
        self.assertIsInstance(json_dict, dict, 'Response is not a valid JSON dictionary')
        message = json_dict.get('message', None)
        self.assertIsNotNone(message, 'No message in response')
        self.assertNotIsInstance(message, dict, 'Message is an object')
        self.logger.info('[%s] Message: %s\n', method, message)

    def test_dependency_name_put(self):
        method = 'test_dependency_name_put'
        url = '/api/dependencies'
        new_dep = self.prepare_new_dependency()
        json_dict = {
            'session_id': 'test',
            'object': new_dep
        }
        json_body = jsonpickle.encode(json_dict)
        self.app.post(url, data=json_body, content_type='application/json')
        new_name = (new_dep.theEnvironmentName, new_dep.theDepender, new_dep.theDependee, new_dep.theDependency)

        upd_dep = new_dep
        upd_dep.theEnvironmentName = self.existing_environment_2
        json_dict = {
            'session_id': 'test',
            'object': upd_dep
        }
        json_body = jsonpickle.encode(json_dict)
        upd_url = '/api/dependencies/environment/%s/depender/%s/dependee/%s/dependency/%s?session_id=test' % new_name
        rv = self.app.put(upd_url, data=json_body, content_type='application/json')
        self.assertIsNotNone(rv.data, 'No response')
        json_dict = jsonpickle.decode(rv.data)
        self.assertIsInstance(json_dict, dict, 'Response is not a valid JSON dictionary')
        message = json_dict.get('message', None)
        self.assertIsNotNone(message, 'No message in response')
        self.assertNotIsInstance(message, dict, 'Message is an object')
        self.logger.info('[%s] Message: %s\n', method, message)

        delete_name = (upd_dep.theEnvironmentName, upd_dep.theDepender, upd_dep.theDependee, upd_dep.theDependency)
        del_get_url = '/api/dependencies/environment/%s/depender/%s/dependee/%s/dependency/%s?session_id=test' % delete_name
        rv = self.app.get(del_get_url)
        self.logger.debug('[%s] Updated dependency:\n%s\n', method, rv.data)
        self.app.delete(del_get_url)

    def prepare_new_dependency(self):
        d = Dependency(
            -1,
            self.existing_environment_1,
            self.existing_role_1,
            self.existing_role_2,
            self.existing_type,
            self.existing_dependency,
            'This is a test dependency'
        )
        return d
