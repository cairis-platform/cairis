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
from cairis.core.PolicyStatement import PolicyStatement
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
import os
from cairis.mio.ModelImport import importModelFile
from cairis.tools.ModelDefinitions import PolicyStatementModel

__author__ = 'Shamal Faily'


class PolicyStatementAPITests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    importModelFile(os.environ['CAIRIS_SRC'] + '/test/PolicyStatementTest.xml',1,'test')

  
  def setUp(self):
    # region Class fields
    self.logger = logging.getLogger(__name__)

    self.existing_goal_name = 'Identifiable connections'
    self.existing_environment_name = 'Day'
    self.existing_subject = 'SCADA Workstation'
    self.existing_access_type = 'interact'
    self.existing_resource = 'Works Network'
    self.existing_permission = 'allow'

    ps_class = PolicyStatement.__module__+'.'+PolicyStatement.__name__
    # endregion

  def test_get_all(self):
    method = 'test_get_all'
    rv = self.app.get('/api/policy_statements?session_id=test')
    responseData = rv.data.decode('utf-8')
    objts = jsonpickle.decode(responseData)
    self.assertIsNotNone(objts, 'No results after deserialization')
    self.assertIsInstance(objts, list, 'The result is not a list as expected')
    self.assertGreater(len(objts), 0, 'No policy statements in the list')
    self.logger.info('[%s] PolicyStatements found: %d', method, len(objts))
    self.assertEqual(len(objts),2)

  def test_get_by_name(self):
    method = 'test_get_by_name'
    url = '/api/policy_statements/goal/' + self.existing_goal_name + '/environment/' + self.existing_environment_name + '/subject/' + self.existing_subject + '/access_type/' + self.existing_access_type + '/resource/' + self.existing_resource + '?session_id=test'
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    responseData = rv.data.decode('utf-8')
    self.logger.debug('[%s] Response data: %s', method, responseData)
    objt = jsonpickle.decode(responseData)
    self.assertIsNotNone(objt, 'No results after deserialization')
    self.assertEqual(objt['theGoalName'],self.existing_goal_name)
    self.assertEqual(objt['theEnvironmentName'],self.existing_environment_name)
    self.assertEqual(objt['theSubject'],self.existing_subject)
    self.assertEqual(objt['theAccessType'],self.existing_access_type)
    self.assertEqual(objt['theResource'],self.existing_resource)
    self.assertEqual(objt['thePermission'],self.existing_permission)

  def test_post(self):
    method = 'test_post'
    url = '/api/policy_statements'
    self.logger.info('[%s] URL: %s', method, url)
    new_ps_body = self.prepare_json()
    rv = self.app.post(url, content_type='application/json', data=new_ps_body)
    responseData = rv.data.decode('utf-8')
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    self.assertEqual(json_resp['message'],'Active Directory Network Services/Day/Corporate Network/write/Telemetry Network created')
    rv = self.app.delete('/api/policy_statements/goal/Active%20Directory%20Network%20Services/environment/Day/subject/Corporate%20Network/access_type/write/resource/Telemetry%20Network?session_id=test')

  def test_put(self):
    method = 'test_put'
    url = '/api/policy_statements'
    self.logger.info('[%s] URL: %s', method, url)
    new_ps_body = self.prepare_json()

    rv = self.app.post(url, content_type='application/json', data=new_ps_body)
    responseData = rv.data.decode('utf-8')
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')

    ps_to_update = self.prepare_new_policy_statement()
    ps_to_update.thePermission = 'deny'
    upd_ps_body = self.prepare_json(ps=ps_to_update)
    rv = self.app.put('/api/policy_statements/goal/Active%20Directory%20Network%20Services/environment/Day/subject/Corporate%20Network/access_type/write/resource/Telemetry%20Network?session_id=test', data=upd_ps_body, content_type='application/json')
    self.assertIsNotNone(rv.data, 'No response')
    responseData = rv.data.decode('utf-8')
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp)
    self.assertEqual(json_resp['message'],'Active Directory Network Services/Day/Corporate Network/write/Telemetry Network updated')

    rv = self.app.get('/api/policy_statements/goal/Active%20Directory%20Network%20Services/environment/Day/subject/Corporate%20Network/access_type/write/resource/Telemetry%20Network?session_id=test')
    responseData = rv.data.decode('utf-8')
    objt = jsonpickle.decode(responseData)
    self.assertIsNotNone(objt, 'No results after deserialization')
    self.assertEqual(objt['theGoalName'],'Active Directory Network Services')
    self.assertEqual(objt['theEnvironmentName'],'Day')
    self.assertEqual(objt['theSubject'],'Corporate Network')
    self.assertEqual(objt['theAccessType'],'write')
    self.assertEqual(objt['theResource'],'Telemetry Network')
    self.assertEqual(objt['thePermission'],'deny')

    rv = self.app.delete('/api/policy_statements/goal/Active%20Directory%20Network%20Services/environment/Day/subject/Corporate%20Network/access_type/write/resource/Telemetry%20Network?session_id=test')
    self.assertIsNotNone(rv.data, 'No response')
    responseData = rv.data.decode('utf-8')
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp)
    self.assertEqual(json_resp['message'],'Active Directory Network Services/Day/Corporate Network/write/Telemetry Network deleted')

  def prepare_new_policy_statement(self):
    new_ps = PolicyStatement(
      psId = -1,
      goalName='Active Directory Network Services',
      envName='Day',
      subjName='Corporate Network',
      acName='write',
      resName='Telemetry Network',
      pName='allow')
    return new_ps

  def prepare_dict(self, ps=None):
    if ps is None:
      ps = self.prepare_new_policy_statement()
    else:
      assert isinstance(ps, PolicyStatement)

    return {
      'session_id': 'test',
      'object': ps,
    }

  def prepare_json(self, data_dict=None, ps=None):
    if data_dict is None:
      data_dict = self.prepare_dict(ps=ps)
    else:
      assert isinstance(data_dict, dict)
    new_ps_body = jsonpickle.encode(data_dict, unpicklable=False)
    self.logger.info('JSON data: %s', new_ps_body)
    return new_ps_body
