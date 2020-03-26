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
from cairis.core.DomainProperty import DomainProperty
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
import os
from cairis.mio.ModelImport import importModelFile

__author__ = 'Shamal Faily'


class DomainPropertyAPITests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/NeuroGrid/NeuroGrid.xml',1,'test')

  
  def setUp(self):
    # region Class fields
    self.logger = logging.getLogger(__name__)

    self.existing_domainproperty_name = 'Secure data analysis'
    self.existing_domainproperty_type = 'Hypothesis'
    self.existing_domainproperty_originator = 'Shamal Faily'
    self.existing_domainproperty_definition = 'We assume that the process of analysing data once it has been uploaded to NeuroGrid is secure.'

    domainproperty_class = DomainProperty.__module__+'.'+DomainProperty.__name__
    # endregion

  def test_get_all(self):
    method = 'test_get_all'
    rv = self.app.get('/api/domainproperties?session_id=test')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    domainproperties = jsonpickle.decode(responseData)
    self.assertIsNotNone(domainproperties, 'No results after deserialization')
    self.assertIsInstance(domainproperties, list, 'The result is a list as expected')
    self.assertGreater(len(domainproperties), 0, 'No domainproperties in the dictionary')
    self.logger.info('[%s] DomainProperties found: %d', method, len(domainproperties))
    domainproperty = domainproperties[0]
    self.logger.info('[%s] First domainproperty: %s\n', method, domainproperty['theName'])

  def test_get_by_name(self):
    method = 'test_get_by_name'
    url = '/api/domainproperties/name/%s?session_id=test' % quote(self.existing_domainproperty_name)
    rv = self.app.get(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.assertIsNotNone(responseData, 'No response')
    self.logger.debug('[%s] Response data: %s', method, responseData)
    domainproperty = jsonpickle.decode(responseData)
    self.assertIsNotNone(domainproperty, 'No results after deserialization')
    self.logger.info('[%s] Domain Property: %s\n', method, domainproperty['theName'])

  def test_delete(self):
    method = 'test_delete'
    url = '/api/domainproperties/name/%s?session_id=test' % quote(self.prepare_new_domainproperty().name())
    new_domainproperty_body = self.prepare_json()

    self.logger.info('[%s] Object to delete: %s', method, new_domainproperty_body)
    self.app.post('/api/domainproperties', content_type='application/json', data=new_domainproperty_body)
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.delete(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.info('[%s] Response data: %s', method, responseData)
    self.assertIsNotNone(rv.data, 'No response')
    json_resp = jsonpickle.decode(responseData)
    self.assertIsInstance(json_resp, dict, 'The response cannot be converted to a dictionary')
    message = json_resp.get('message', None)
    self.assertIsNotNone(message, 'No message in response')
    self.logger.info('[%s] Message: %s\n', method, message)

  def test_post(self):
    method = 'test_post'
    url = '/api/domainproperties'
    self.logger.info('[%s] URL: %s', method, url)
    new_domainproperty_body = self.prepare_json()

    rv = self.app.post(url, content_type='application/json', data=new_domainproperty_body)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')


    rv = self.app.post(url, content_type='application/json', data=new_domainproperty_body)
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
    self.assertGreater(message.find('already exists'), -1, 'The domainproperty post should have failed')

    rv = self.app.delete('/api/domainproperties/name/%s?session_id=test' % quote(self.prepare_new_domainproperty().name()))

  def test_put(self):
    method = 'test_put'
    url = '/api/domainproperties'
    self.logger.info('[%s] URL: %s', method, url)
    new_domainproperty_body = self.prepare_json()

    rv = self.app.post(url, content_type='application/json', data=new_domainproperty_body)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')

    domainproperty_to_update = self.prepare_new_domainproperty()
    domainproperty_to_update.theName = 'Edited test domainproperty'
    upd_env_body = self.prepare_json(domainproperty=domainproperty_to_update)
    rv = self.app.put('/api/domainproperties/name/%s?session_id=test' % quote(self.prepare_new_domainproperty().name()), data=upd_env_body, content_type='application/json')
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
    self.assertGreater(message.find('updated'), -1, 'The domainproperty was not successfully updated')

    rv = self.app.get('/api/domainproperties/name/%s?session_id=test' % quote(domainproperty_to_update.name()))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    upd_domainproperty = jsonpickle.decode(responseData)
    self.assertIsNotNone(upd_domainproperty, 'Unable to decode JSON data')
    self.logger.debug('[%s] Response data: %s', method, responseData)
    self.logger.info('[%s] Domain Property: %s\n', method, upd_domainproperty['theName'])

    rv = self.app.put('/api/domainproperties/name/%s?session_id=test' % quote(self.prepare_new_domainproperty().name()), data=upd_env_body, content_type='application/json')
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
    self.assertGreater(message.find('already exists'), -1, 'The domainproperty update should have failed')

    rv = self.app.delete('/api/domainproperties/name/%s?session_id=test' % quote(domainproperty_to_update.theName))

  def prepare_new_domainproperty(self):

    new_domainproperty = DomainProperty(
      dpId=-1,
      dpName='New Domain Property',
      dpDesc='New description',
      dpType='Hypothesis',
      dpOrig='Shamal Faily',
      tags=[]
    )
    return new_domainproperty

  def prepare_dict(self, domainproperty=None):
    if domainproperty is None:
      domainproperty = self.prepare_new_domainproperty()
    else:
      assert isinstance(domainproperty, DomainProperty)

    return {
      'session_id': 'test',
      'object': domainproperty,
    }

  def prepare_json(self, data_dict=None, domainproperty=None):
    if data_dict is None:
      data_dict = self.prepare_dict(domainproperty=domainproperty)
    else:
      assert isinstance(data_dict, dict)
    new_domainproperty_body = jsonpickle.encode(data_dict, unpicklable=False)
    self.logger.info('JSON data: %s', new_domainproperty_body)
    return new_domainproperty_body
