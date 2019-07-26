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
from cairis.core.Role import Role
import jsonpickle
import os
from cairis.core.RoleEnvironmentProperties import RoleEnvironmentProperties
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
from cairis.tools.JsonConverter import json_deserialize
from cairis.mio.ModelImport import importModelFile

__author__ = 'Robin Quetin, Shamal Faily'


class RoleAPITests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/NeuroGrid/NeuroGrid.xml',1,'test')


  def setUp(self):
    self.logger = logging.getLogger(__name__)
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
        countermeasures=['Location-based X.509 extension'],
        goals=[],
        requirements=[]
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
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    roles = jsonpickle.decode(responseData)
    self.assertIsNotNone(roles, 'No results after deserialization')
    self.assertIsInstance(roles, list, 'The result is not a list as expected')
    self.assertGreater(len(roles), 0, 'No roles in the list')
    self.logger.info('[%s] Roles found: %d', method, len(roles))
    self.logger.info('[%s] First role: %s\n', method, roles[0]['theName'])

  def test_post(self):
    method = 'test_post_new'
    rv = self.app.post('/api/roles', content_type='application/json', data=self.new_role_body)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    message = json_resp.get('message', None)
    self.assertIsNotNone(message, 'No message returned')
    self.assertEqual(message, 'Student created')

  def test_get_name(self):
    method = 'test_get_name'
    url = '/api/roles/name/%s?session_id=test' % quote(self.existing_role_name)
    rv = self.app.get(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    role = jsonpickle.decode(responseData)
    self.assertIsNotNone(role, 'No results after deserialization')
    self.assertEqual(role['theName'],self.existing_role_name)

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
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    message = json_resp.get('message', None)
    self.assertIsNotNone(message, 'No message returned')
    self.assertEqual(message, upd_role.theName + ' updated')

    rv = self.app.get('/api/roles/name/Test3?session_id=test')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    role = json_deserialize(responseData)
    self.logger.info('[%s] Role: %s\n', method, role['theName'])

  def test_x_delete_name(self):
    method = 'test_delete_name'

    rv = self.app.post('/api/roles', content_type='application/json', data=self.new_role_body)

    url = '/api/roles/name/{}?session_id=test'.format(quote(self.new_role.theName))
    rv = self.app.delete(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    message = json_resp.get('message', None)
    self.assertIsNotNone(message, 'No message returned')
    self.assertEqual(message, 'Student deleted')

    rv = self.app.post('/api/roles', content_type='application/json', data=self.new_role_body)

    url = '/api/roles/name/Test2'

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
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    role_props = jsonpickle.decode(responseData)
    self.assertIsNotNone(role_props, 'No results after deserialization')
    self.assertGreater(len(role_props), 0, 'List does not contain any elements')
    role_prop = role_props[0]
    self.logger.info('[%s] Role property: %s\n', method, role_props[0]['theEnvironmentName'])
