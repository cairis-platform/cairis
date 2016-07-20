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
from cairis.core.Role import Role
import jsonpickle
from cairis.core.RoleEnvironmentProperties import RoleEnvironmentProperties
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
from cairis.tools.JsonConverter import json_deserialize
from cairis.mio.ModelImport import importModelFile

class RoleAPITests(CairisDaemonTestCase):

  def setUp(self):
    importModelFile('../../examples/exemplars/NeuroGrid/NeuroGrid.xml',1,'test')
    self.logger = logging.getLogger(__name__)
    self.existing_role_id = 122
    self.existing_role_name = 'Certificate Authority'
    self.role_class = Role.__module__+'.'+Role.__name__
    self.new_role = Role(
      roleId=-1,
      roleName='Student',
      rType='Stakeholder',
      sCode='STU',
      roleDesc='This is a test role',
      cProps=[]
    )
    self.new_role_props = [
      RoleEnvironmentProperties(
        environmentName='Core Technology',
        responses=[('Prevent Unauthorised Certificate Access', 'High')],
        countermeasures=['Location-based X.509 extension']
      )
    ]
    self.new_role_dict = {
      'session_id': 'test',
      'object': self.new_role,
      'property_0': self.new_role_props
    }
    self.new_role_body = jsonpickle.encode(self.new_role_dict)
    self.logger.info('JSON data: %s', self.new_role_body)

  def test_get_all(self):
    method = 'test_get_all'
    rv = self.app.get('/api/roles?session_id=test')
    roles = json_deserialize(rv.data)
    self.assertIsNotNone(roles, 'No results after deserialization')
    self.assertIsInstance(roles, dict, 'The result is not a dictionary as expected')
    self.assertGreater(len(roles), 0, 'No roles in the dictionary')
    self.assertIsInstance(roles.values()[0], Role)
    self.logger.info('[%s] Roles found: %d', method, len(roles))
    self.logger.info('[%s] First role: %s [%d]\n', method, roles.values()[0].theName, roles.values()[0].theId)

  def test_post(self):
    method = 'test_post_new'
    rv = self.app.post('/api/roles', content_type='application/json', data=self.new_role_body)
    self.logger.debug('[%s] Response data: %s', method, rv.data)
    json_resp = json_deserialize(rv.data)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    role_id = json_resp.get('role_id', None)
    self.assertIsNotNone(role_id, 'No role ID returned')
    self.logger.info('[%s] Role ID: %d', method, role_id)

    rv = self.app.get('/api/roles/id/%d?session_id=test' % role_id)
    role = jsonpickle.decode(rv.data)
    self.logger.info('[%s] Role: %s [%d]\n', method, role['theName'], role['theId'])

  def test_get_id(self):
    method = 'test_get_id'
    url = '/api/roles/id/%d?session_id=test' % self.existing_role_id
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    self.logger.debug('[%s] Response data: %s', method, rv.data)
    role = jsonpickle.decode(rv.data)
    self.assertIsNotNone(role, 'No results after deserialization')
    self.assertEqual(role['__python_obj__'], self.role_class, 'The result is not an role as expected')
    self.logger.info('[%s] Role: %s [%d]\n', method, role['theName'], role['theId'])

  def test_get_name(self):
    method = 'test_get_name'
    url = '/api/roles/name/%s?session_id=test' % quote(self.existing_role_name)
    rv = self.app.get(url)
    role = json_deserialize(rv.data)
    self.assertIsNotNone(role, 'No results after deserialization')
    self.assertIsInstance(role, Role, 'The result is not an role as expected')
    self.logger.info('[%s] Role: %s [%d]\n', method, role.theName, role.theId)

  def test_put_name(self):
    method = 'test_put_name'
    rv = self.app.post('/api/roles', content_type='application/json', data=self.new_role_body)

    url = '/api/roles/name/%s' % quote(self.new_role.theName)

    upd_role = self.new_role
    upd_role.theName = 'Test3'
    upd_role_dict = self.new_role_dict
    upd_role_dict['object'] = upd_role
    upd_role_body = jsonpickle.encode(upd_role_dict)
    self.logger.info('[%s] JSON data: %s', method, upd_role_body)

    rv = self.app.put(url, content_type='application/json', data=upd_role_body)
    self.logger.debug('[%s] Response data: %s', method, rv.data)
    json_resp = json_deserialize(rv.data)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    message = json_resp.get('message', None)
    self.assertIsNotNone(message, 'No message returned')

    rv = self.app.get('/api/roles/name/Test3?session_id=test')
    role = json_deserialize(rv.data)
    self.logger.info('[%s] Role: %s [%d]\n', method, role.theName, role.theId)

  def test_put_id(self):
    method = 'test_put_id'

    rv = self.app.post('/api/roles', content_type='application/json', data=self.new_role_body)

    rv = self.app.get('/api/roles?session_id=test')
    roles = json_deserialize(rv.data)
    role = roles.get(self.new_role.theName)
    url = '/api/roles/id/%d' % role.theId

    upd_role = self.new_role
    upd_role.theName = 'Test2'
    upd_role_dict = self.new_role_dict
    upd_role_dict['object'] = upd_role
    upd_role_body = jsonpickle.encode(upd_role_dict)
    self.logger.info('[%s] JSON data: %s', method, upd_role_body)

    rv = self.app.put(url, content_type='application/json', data=upd_role_body)
    self.logger.debug('[%s] Response data: %s', method, rv.data)
    json_resp = json_deserialize(rv.data)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    message = json_resp.get('message', None)
    self.assertIsNotNone(message, 'No message returned')

    rv = self.app.get('/api/roles/name/Test2?session_id=test')
    role = json_deserialize(rv.data)
    self.logger.info('[%s] Role: %s [%d]\n', method, role.theName, role.theId)

  def test_x_delete_name(self):
    method = 'test_delete_name'

    rv = self.app.post('/api/roles', content_type='application/json', data=self.new_role_body)

    url = '/api/roles/name/{}?session_id=test'.format(quote(self.new_role.theName))
    rv = self.app.delete(url)
    self.logger.debug('[%s] Response data: %s', method, rv.data)
    json_resp = json_deserialize(rv.data)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    message = json_resp.get('message', None)
    self.assertIsNotNone(message, 'No message returned')
    self.logger.info('[%s] Message: %s\n', method, message)

    rv = self.app.post('/api/roles', content_type='application/json', data=self.new_role_body)
    rv = self.app.get('/api/roles?session_id=test')
    roles = json_deserialize(rv.data)
    role = roles.get(self.new_role.theName)
    url = '/api/roles/id/%d' % role.theId

    upd_role = self.new_role
    upd_role.theName = 'Test2'
    upd_role_dict = self.new_role_dict
    upd_role_dict['object'] = upd_role
    upd_role_body = jsonpickle.encode(upd_role_dict)
    rv = self.app.put(url, content_type='application/json', data=upd_role_body)
    url = '/api/roles/name/Test2?session_id=test'.format(quote(self.new_role.theName))
    rv = self.app.delete(url)

  def test_get_props_name_get(self):
    method = 'test_get_props_name_get'
    url = '/api/roles/name/%s/properties?session_id=test' % quote(self.existing_role_name)
    cls_role_prop = RoleEnvironmentProperties.__module__+'.'+RoleEnvironmentProperties.__name__

    rv = self.app.get(url)
    role_props = jsonpickle.decode(rv.data)
    self.assertIsNotNone(role_props, 'No results after deserialization')
    self.assertGreater(len(role_props), 0, 'List does not contain any elements')
    role_prop = role_props[0]
    self.assertEqual(cls_role_prop, role_prop['__python_obj__'], 'The result is not an role as expected')
    self.logger.info('[%s] Role property: %s\n', method, role_props[0]['theEnvironmentName'])
