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
from cairis.core.AcceptEnvironmentProperties import AcceptEnvironmentProperties
from cairis.core.MitigateEnvironmentProperties import MitigateEnvironmentProperties
from cairis.core.TransferEnvironmentProperties import TransferEnvironmentProperties
from cairis.core.Response import Response
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
from cairis.tools.PseudoClasses import ValuedRole
from cairis.mio.ModelImport import importModelFile
import os

__author__ = 'Robin Quetin, Shamal Faily'


class ResponseAPITests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/NeuroGrid/NeuroGrid.xml',1,'test')


  def setUp(self):
    # region Class fields
    self.logger = logging.getLogger(__name__)
    self.existing_response_name = 'Prevent Unauthorised Certificate Access'
    self.existing_environment_name = 'Stroke'
    self.existing_risk_name = 'Unauthorised Certificate Access'
    self.existing_role_name = 'Developer'
    self.response_class = Response.__module__+'.'+Response.__name__
    # endregion


  def test_get_all(self):
    method = 'test_get_all'
    rv = self.app.get('/api/responses?session_id=test')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    responses = jsonpickle.decode(responseData)
    self.assertIsNotNone(responses, 'No results after deserialization')
    self.assertIsInstance(responses, list, 'The result is not a dictionary as expected')
    self.assertGreater(len(responses), 0, 'No responses in the dictionary')
    self.logger.info('[%s] Responses found: %d', method, len(responses))
    response = responses[0]
    self.logger.info('[%s] First response: %s\n', method, response['theName'])

  def test_get_by_name(self):
    method = 'test_get_by_name'
    url = '/api/responses/name/%s?session_id=test' % quote(self.existing_response_name)
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    response = jsonpickle.decode(responseData)
    self.assertIsNotNone(response, 'No results after deserialization')
    self.logger.info('[%s] Response: %s\n', method, response['theName'])

  def test_delete(self):
    method = 'test_delete'
    url = '/api/responses/name/%s?session_id=test' % quote(self.prepare_new_response().theName)
    new_response_body = self.prepare_json()

    self.app.delete(url)
    self.logger.info('[%s] Object to delete: %s', method, new_response_body)
    self.app.post('/api/responses', content_type='application/json', data=new_response_body)
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

  def test_new_accept_post(self):
    method = 'test_new_accept_post'
    url = '/api/responses'
    self.logger.info('[%s] URL: %s', method, url)
    new_response_body = self.prepare_json(response_type='Accept')

    self.app.delete('/api/responses/name/%s?session_id=test' % quote(self.prepare_new_response().theName))
    rv = self.app.post(url, content_type='application/json', data=new_response_body)
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

    rv = self.app.delete('/api/responses/name/%s?session_id=test' % quote(self.prepare_new_response().theName))

  def test_new_mitigate_post(self):
    method = 'test_new_mitigate_post'
    url = '/api/responses'
    self.logger.info('[%s] URL: %s', method, url)
    new_response_body = self.prepare_json()

    self.app.delete('/api/responses/name/%s?session_id=test' % quote(self.prepare_new_response().theName))
    rv = self.app.post(url, content_type='application/json', data=new_response_body)
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

    rv = self.app.post('/api/responses/name/%s/generate_goal?session_id=test' % quote(self.prepare_new_response().theName))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertEqual(ackMsg, 'Goal successfully generated')
    rv = self.app.delete('/api/responses/name/%s?session_id=test' % quote(self.prepare_new_response().theName))


  def test_new_transfer_post(self):
    method = 'test_new_transfer_post'
    url = '/api/responses'
    self.logger.info('[%s] URL: %s', method, url)
    new_response_body = self.prepare_json(response_type='Transfer')

    self.app.delete('/api/responses/name/%s?session_id=test' % quote(self.prepare_new_response().theName))
    rv = self.app.post(url, content_type='application/json', data=new_response_body)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data

    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertEqual(ackMsg, 'Test response created')
    rv = self.app.delete('/api/responses/name/%s?session_id=test' % quote(self.prepare_new_response().theName))


  def test_put(self):
    method = 'test_put'
    url = '/api/responses'
    self.logger.info('[%s] URL: %s', method, url)
    new_response_body = self.prepare_json()

    rv = self.app.delete('/api/responses/name/%s?session_id=test' % quote(self.prepare_new_response().theName))
    rv = self.app.post(url, content_type='application/json', data=new_response_body)
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

    response_to_update = self.prepare_new_response()
    response_to_update.theName = 'Edited test response'
    upd_env_body = self.prepare_json(response=response_to_update)
    rv = self.app.put('/api/responses/name/%s?session_id=test' % quote(self.prepare_new_response().theName), data=upd_env_body, content_type='application/json')
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
    self.assertGreater(message.find('updated'), -1, 'The response was not successfully updated')

    rv = self.app.get('/api/responses/name/%s?session_id=test' % quote(response_to_update.theName))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    upd_response = jsonpickle.decode(responseData)
    self.assertIsNotNone(upd_response, 'Unable to decode JSON data')
    self.logger.debug('[%s] Response data: %s', method, responseData)
    self.logger.info('[%s] Response: %s\n', method, upd_response['theName'])

    rv = self.app.delete('/api/responses/name/%s?session_id=test' % quote(response_to_update.theName))

  def prepare_new_response(self, response_type='Mitigate'):
    new_response = Response(
      respId=-1,
      respName='Test response',
      respRisk=self.existing_risk_name,
      tags=['test'],
      cProps=[],
      respType=response_type
    )
    if response_type == 'Mitigate':
      new_response_props ={"mitigate" : [
        MitigateEnvironmentProperties(
          environmentName=self.existing_environment_name,
          type='Detect',
          detPoint='At',
          detMechs=[]
        )
      ],
      "transfer" : [],
      "accept" : []}
    elif response_type == 'Accept':
      new_response_props = {"accept" : [
        AcceptEnvironmentProperties(
          environmentName=self.existing_environment_name,
          cost='Low',
          rationale='Test'
        )
      ],
      "transfer" : [],
      "mitigate" : []}
    elif response_type == 'Transfer':
      new_response_props = {"transfer" : [
        TransferEnvironmentProperties(
          environmentName=self.existing_environment_name,
          rationale='Test',
          roles=[
            (self.existing_role_name, 'Low')
          ]
        )
      ],
      "accept" : [],
      "mitigate" : []}
    else:
      new_response_props = {"accept" : [],"transfer" : [], "mitigate" : []}
    new_response.theEnvironmentProperties = new_response_props
    return new_response

  def prepare_dict(self, response=None, response_type='Mitigate'):
    if response is None:
      response = self.prepare_new_response(response_type=response_type)
    else:
      assert isinstance(response, Response)

    if response.theResponseType == 'Transfer': 
      transfer_props = response.theEnvironmentProperties["transfer"]
      for idx in range(0, len(transfer_props)):
        the_roles = transfer_props[idx].theRoles
        for idx in range(0, len(the_roles)):
          the_roles[idx] = ValuedRole(
                             role_name=the_roles[idx][0],
                             cost=the_roles[idx][1]
                           )
        transfer_props[idx].theRoles = the_roles
      response.theEnvironmentProperties = { "transfer" : transfer_props, "accept" : [], "mitigate" : []}

    return {
      'session_id': 'test',
      'object': response,
    }

  def prepare_json(self, data_dict=None, response=None, response_type='Mitigate'):
    if data_dict is None:
      data_dict = self.prepare_dict(response=response, response_type=response_type)
    else:
      assert isinstance(data_dict, dict)
    new_response_body = jsonpickle.encode(data_dict, unpicklable=False)
    self.logger.info('JSON data: %s', new_response_body)
    return new_response_body
