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
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
from cairis.tools.ModelDefinitions import DependencyModel
import os
import sys
from cairis.mio.ModelImport import importModelFile

__author__ = 'Robin Quetin, Shamal Faily'


class DependencyAPITests(CairisDaemonTestCase):
  
  @classmethod
  def setUpClass(cls):
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/NeuroGrid/NeuroGrid.xml',1,'test')

  def setUp(self):
    self.logger = logging.getLogger(__name__)
    self.working_name = ('Stroke', 'Data%20Consumer', 'Certificate%20Authority', 'Personal%20certificate')
    self.existing_environment_1 = 'Stroke'
    self.existing_environment_2 = 'Psychosis'
    self.existing_role_1 = 'Data Consumer'
    self.existing_role_2 = 'Certificate Authority'
    self.existing_type = 'goal'
    self.existing_dependency = 'Upload authorisation'

  def test_all_get(self):
    method = 'test_all_get'
    url = '/api/dependencies?session_id=test'

    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    deps = jsonpickle.decode(responseData)
    self.assertIsInstance(deps, list, 'The response is not a valid JSON list')
    self.assertGreater(len(deps), 0, 'No dependencies found')
    item = deps[0]
    self.logger.info('[%s] First dependency: %s\n', method, item['theDependency'])

  def test_dependency_name_get(self):
    method = 'test_dependency_name_get'
    url = '/api/dependencies/environment/%s/depender/%s/dependee/%s/dependency/%s?session_id=test' % self.working_name

    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    item = jsonpickle.decode(responseData)
    self.assertIsInstance(item, dict, 'The response is not a valid JSON dictionary')
    self.assertEqual(item['theEnvironmentName'],'Stroke')
    self.assertEqual(item['theDepender'],'Data Consumer')
    self.assertEqual(item['theDependee'], 'Certificate Authority')
    self.assertEqual(item['theDependency'],'Personal certificate')

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
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    json_dict = jsonpickle.decode(responseData)
    self.assertIsInstance(json_dict, dict, 'Response is not a valid JSON dictionary')
    message = json_dict.get('message', None)
    self.assertIsNotNone(message, 'No message in response')
    self.assertNotIsInstance(message, dict, 'Message is an object')
    self.logger.info('[%s] Message: %s', method, message)

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
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    json_dict = jsonpickle.decode(responseData)
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
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    json_dict = jsonpickle.decode(responseData)
    self.assertIsInstance(json_dict, dict, 'Response is not a valid JSON dictionary')
    message = json_dict.get('message', None)
    self.assertIsNotNone(message, 'No message in response')
    self.assertNotIsInstance(message, dict, 'Message is an object')
    self.logger.info('[%s] Message: %s\n', method, message)

    delete_name = (upd_dep.theEnvironmentName, upd_dep.theDepender, upd_dep.theDependee, upd_dep.theDependency)
    del_get_url = '/api/dependencies/environment/%s/depender/%s/dependee/%s/dependency/%s?session_id=test' % delete_name
    rv = self.app.get(del_get_url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Updated dependency:\n%s\n', method, responseData)
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
