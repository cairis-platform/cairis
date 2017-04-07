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
from cairis.core.UseCase import UseCase
from cairis.core.Trace import Trace
from cairis.core.UseCaseEnvironmentProperties import UseCaseEnvironmentProperties
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
import os
from cairis.mio.ModelImport import importModelFile, importUsabilityFile
from cairis.tools.PseudoClasses import StepsAttributes, StepAttributes,ExceptionAttributes

__author__ = 'Shamal Faily'


class UseCaseAPITests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/NeuroGrid/NeuroGrid.xml',1,'test')
    importModelFile(os.environ['CAIRIS_SRC'] + '/test/testusecase.xml',0,'test')
  
  def setUp(self):
    # region Class fields
    self.logger = logging.getLogger(__name__)
    self.existing_usecase_name = 'Test use case'
    self.existing_environment_name = 'Psychosis'
    self.existing_author = 'Shamal Faily'
    self.existing_code = 'TUC-1'
    self.existing_description = 'A test description'
    self.existing_actors = ['Researcher']
    self.existing_precond = 'Test preconditions'
    self.existing_steps = []
    anException = ExceptionAttributes('anException','requirement','Anonymisation guidelines','Confidentiality Threat','anException description')
    self.existing_steps.append(StepAttributes('Researcher does something','','','',[],[anException]))
    self.existing_steps.append(StepAttributes('System does something','','','',[],[]))
    self.existing_postcond = 'Test postconditions'
    usecase_class = UseCase.__module__+'.'+UseCase.__name__
    # endregion

  def test_get_all(self):
    method = 'test_get_all'
    rv = self.app.get('/api/usecases?session_id=test')
    usecases = jsonpickle.decode(rv.data)
    self.assertIsNotNone(usecases, 'No results after deserialization')
    self.assertIsInstance(usecases, dict, 'The result is not a dictionary as expected')
    self.assertGreater(len(usecases), 0, 'No usecases in the dictionary')
    self.logger.info('[%s] Use Cases found: %d', method, len(usecases))
    usecase = usecases.values()[0]
    self.logger.info('[%s] First usecase: %s [%d]\n', method, usecase['theName'], usecase['theId'])

  def test_get_by_name(self):
    method = 'test_get_by_name'
    url = '/api/usecases/name/%s?session_id=test' % quote(self.existing_usecase_name)
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    self.logger.debug('[%s] Response data: %s', method, rv.data)
    usecase = jsonpickle.decode(rv.data)
    self.assertIsNotNone(usecase, 'No results after deserialization')
    self.logger.info('[%s] UseCase: %s [%d]\n', method, usecase['theName'], usecase['theId'])

  def test_get_usecase_requirements(self):
    new_tr = Trace(
      fObjt = 'requirement',
      fName = 'Dataset policy',
      tObjt = 'usecase',
      tName = 'Test use case')
    new_tr_dict = {
      'session_id' : 'test',
      'object': new_tr
    }
    rv = self.app.post('/api/traces', content_type='application/json', data=jsonpickle.encode(new_tr_dict))

    method = 'test_get_requirements_by_usecase_name'
    url = '/api/usecases/name/%s/requirements?session_id=test' % quote(self.existing_usecase_name)
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    self.logger.debug('[%s] Response data: %s', method, rv.data)
    reqs = jsonpickle.decode(rv.data)
    self.assertIsNotNone(reqs, 'No results after deserialization')
    self.assertEqual(new_tr.theFromName,reqs[0]);

  def test_delete(self):
    method = 'test_delete'
    url = '/api/usecases/name/%s?session_id=test' % quote(self.prepare_new_usecase().name())
    new_usecase_body = self.prepare_json()

    self.app.delete(url)
    self.logger.info('[%s] Object to delete: %s', method, new_usecase_body)
    self.app.post('/api/usecases', content_type='application/json', data=new_usecase_body)
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.delete(url)
    self.logger.info('[%s] Response data: %s', method, rv.data)
    self.assertIsNotNone(rv.data, 'No response')
    json_resp = jsonpickle.decode(rv.data)
    self.assertIsInstance(json_resp, dict, 'The response cannot be converted to a dictionary')
    message = json_resp.get('message', None)
    self.assertIsNotNone(message, 'No message in response')
    self.logger.info('[%s] Message: %s\n', method, message)


  def test_post(self):
    method = 'test_post'
    url = '/api/usecases'
    self.logger.info('[%s] URL: %s', method, url)
    new_usecase_body = self.prepare_json()

    self.app.delete('/api/usecases/name/%s?session_id=test' % quote(self.prepare_new_usecase().name()))
    rv = self.app.post(url, content_type='application/json', data=new_usecase_body)
    self.logger.debug('[%s] Response data: %s', method, rv.data)
    json_resp = jsonpickle.decode(rv.data)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    env_id = json_resp.get('usecase_id', None)
    self.assertIsNotNone(env_id, 'No usecase ID returned')
    self.assertGreater(env_id, 0, 'Invalid usecase ID returned [%d]' % env_id)
    self.logger.info('[%s] UseCase ID: %d\n', method, env_id)
    rv = self.app.delete('/api/usecases/name/%s?session_id=test' % quote(self.prepare_new_usecase().name()))

  def test_put(self):
    method = 'test_put'
    url = '/api/usecases'
    self.logger.info('[%s] URL: %s', method, url)
    new_usecase_body = self.prepare_json()

    rv = self.app.delete('/api/usecases/name/%s?session_id=test' % quote(self.prepare_new_usecase().name()))
    rv = self.app.post(url, content_type='application/json', data=new_usecase_body)
    self.logger.debug('[%s] Response data: %s', method, rv.data)
    json_resp = jsonpickle.decode(rv.data)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    env_id = json_resp.get('usecase_id', None)
    self.assertIsNotNone(env_id, 'No usecase ID returned')
    self.assertGreater(env_id, 0, 'Invalid usecase ID returned [%d]' % env_id)
    self.logger.info('[%s] UseCase ID: %d', method, env_id)

    usecase_to_update = self.prepare_new_usecase()
    usecase_to_update.theName = 'Edited test usecase'
    usecase_to_update.theId = env_id
    upd_env_body = self.prepare_json(usecase=usecase_to_update)
    rv = self.app.put('/api/usecases/name/%s?session_id=test' % quote(self.prepare_new_usecase().name()), data=upd_env_body, content_type='application/json')
    self.assertIsNotNone(rv.data, 'No response')
    json_resp = jsonpickle.decode(rv.data)
    self.assertIsNotNone(json_resp)
    self.assertIsInstance(json_resp, dict)
    message = json_resp.get('message', None)
    self.assertIsNotNone(message, 'No message in response')
    self.logger.info('[%s] Message: %s', method, message)
    self.assertGreater(message.find('successfully updated'), -1, 'The usecase was not successfully updated')

    rv = self.app.get('/api/usecases/name/%s?session_id=test' % quote(usecase_to_update.name()))
    upd_usecase = jsonpickle.decode(rv.data)
    self.assertIsNotNone(upd_usecase, 'Unable to decode JSON data')
    self.logger.debug('[%s] Response data: %s', method, rv.data)
    self.logger.info('[%s] UseCase: %s [%d]\n', method, upd_usecase['theName'], upd_usecase['theId'])

    rv = self.app.delete('/api/usecases/name/%s?session_id=test' % quote(usecase_to_update.theName))

  def prepare_new_usecase(self):
    new_usecase_props = [
      UseCaseEnvironmentProperties(
        environmentName=self.existing_environment_name,
        preCond=self.existing_precond,
        steps=self.existing_steps,
        postCond=self.existing_postcond
      )
    ]
    new_usecase = UseCase(
      ucId=-1,
      ucName='New usecase',
      ucAuth='NU',
      ucCode='New objective',
      ucActors=['Researcher'],
      ucDesc='New Author',
      tags=[],
      cProps=[]
    )
    new_usecase.theEnvironmentProperties = new_usecase_props
    new_usecase.theEnvironmentDictionary = {}
    delattr(new_usecase, 'theEnvironmentDictionary')
    return new_usecase

  def prepare_dict(self, usecase=None):
    if usecase is None:
      usecase = self.prepare_new_usecase()
    else:
      assert isinstance(usecase, UseCase)

    return {
      'session_id': 'test',
      'object': usecase,
    }

  def prepare_json(self, data_dict=None, usecase=None):
    if data_dict is None:
      data_dict = self.prepare_dict(usecase=usecase)
    else:
      assert isinstance(data_dict, dict)
    new_usecase_body = jsonpickle.encode(data_dict, unpicklable=False)
    self.logger.info('JSON data: %s', new_usecase_body)
    return new_usecase_body
