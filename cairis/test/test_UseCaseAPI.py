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
from cairis.core.UseCase import UseCase
from cairis.core.Trace import Trace
from cairis.tools.JsonConverter import json_deserialize
from cairis.core.UseCaseEnvironmentProperties import UseCaseEnvironmentProperties
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
import os
from cairis.mio.ModelImport import importModelFile, importRequirementsFile
from cairis.tools.JsonConverter import json_deserialize
from cairis.tools.PseudoClasses import StepsAttributes, StepAttributes,ExceptionAttributes
from cairis.tools.ModelDefinitions import UseCaseContributionModel

__author__ = 'Shamal Faily'


class UseCaseAPITests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/NeuroGrid/NeuroGrid.xml',1,'test')
    importRequirementsFile(os.environ['CAIRIS_SRC'] + '/test/testusecase.xml','test')
  
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
    self.existing_steps.append(StepAttributes('Researcher does something','','','',[anException]))
    self.existing_steps.append(StepAttributes('System does something','','','',[]))
    self.existing_postcond = 'Test postconditions'
    usecase_class = UseCase.__module__+'.'+UseCase.__name__
    # endregion

  def test_get_all(self):
    method = 'test_get_all'
    rv = self.app.get('/api/usecases?session_id=test')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    usecases = jsonpickle.decode(responseData)
    self.assertIsNotNone(usecases, 'No results after deserialization')
    self.assertIsInstance(usecases, dict, 'The result is not a dictionary as expected')
    self.assertGreater(len(usecases), 0, 'No usecases in the dictionary')
    self.logger.info('[%s] Use Cases found: %d', method, len(usecases))
    usecase = list(usecases.values())[0]
    self.logger.info('[%s] First usecase: %s\n', method, usecase['theName'])

  def test_get_all_summary(self):
    method = 'test_get_all_summary'
    rv = self.app.get('/api/usecases/summary?session_id=test')
    if (sys.version_info > (3,)):
      ucs = json_deserialize(rv.data.decode('utf-8'))
    else:
      ucs = json_deserialize(rv.data)
    self.assertIsNotNone(ucs, 'No results after deserialization')
    self.assertGreater(len(ucs), 0, 'No goal summaries')
    self.logger.info('[%s] Use Cases found: %d', method, len(ucs))
    self.logger.info('[%s] First use case summary: %s \n', method, ucs[0]['theName'])

  def test_get_by_name(self):
    method = 'test_get_by_name'
    url = '/api/usecases/name/%s?session_id=test' % quote(self.existing_usecase_name)
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    usecase = jsonpickle.decode(responseData)
    self.assertIsNotNone(usecase, 'No results after deserialization')
    self.logger.info('[%s] UseCase: %s\n', method, usecase['theName'])

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
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    reqs = jsonpickle.decode(responseData)
    self.assertIsNotNone(reqs, 'No results after deserialization')
    self.assertEqual(new_tr.theFromName,reqs[0]);

  def test_delete(self):
    method = 'test_delete'

    rv = self.app.get('/api/persona_characteristics/name/Managers%20delegate%20security%20decisions?session_id=test')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    pc = jsonpickle.decode(responseData)
    pc['theCharacteristicSynopsis'] = {"theActor" : "Claire", "theActorType" : "persona", "theSynopsis" : "Security delegated", "theDimension" : "goal"}
    pcDict = {'session_id' : 'test','object' : pc}
    rv = self.app.put('/api/persona_characteristics/name/Managers%20delegate%20security%20decisions?session_id=test', content_type='application/json', data=jsonpickle.encode(pcDict))
    url = '/api/usecases/name/%s?session_id=test' % quote(self.prepare_new_usecase().name())
    new_usecase_body = self.prepare_json()

    self.app.delete(url)
    self.logger.info('[%s] Object to delete: %s', method, new_usecase_body)
    self.app.post('/api/usecases', content_type='application/json', data=new_usecase_body)
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

  def test_post(self):
    method = 'test_post'

    rv = self.app.get('/api/persona_characteristics/name/Managers%20delegate%20security%20decisions?session_id=test')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    pc = jsonpickle.decode(responseData)
    pc['theCharacteristicSynopsis'] = {"theActor" : "Claire", "theActorType" : "persona", "theSynopsis" : "Security delegated", "theDimension" : "goal"}
    pcDict = {'session_id' : 'test','object' : pc}
    rv = self.app.put('/api/persona_characteristics/name/Managers%20delegate%20security%20decisions?session_id=test', content_type='application/json', data=jsonpickle.encode(pcDict))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertGreater(ackMsg.find('updated'),-1,'PC not updated')



    url = '/api/usecases'
    self.logger.info('[%s] URL: %s', method, url)
    new_usecase_body = self.prepare_json()

    self.app.delete('/api/usecases/name/%s?session_id=test' % quote(self.prepare_new_usecase().name()))
    rv = self.app.post(url, content_type='application/json', data=new_usecase_body)
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
    rv = self.app.delete('/api/usecases/name/%s?session_id=test' % quote(self.prepare_new_usecase().name()))



  def test_put(self):
    method = 'test_put'
    url = '/api/usecases'
    self.logger.info('[%s] URL: %s', method, url)
    new_usecase_body = self.prepare_json()

    rv = self.app.delete('/api/usecases/name/%s?session_id=test' % quote(self.prepare_new_usecase().name()))
    rv = self.app.post(url, content_type='application/json', data=new_usecase_body)
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

    usecase_to_update = self.prepare_new_usecase()
    usecase_to_update.theName = 'Edited test usecase'
    upd_env_body = self.prepare_json(usecase=usecase_to_update)
    rv = self.app.put('/api/usecases/name/%s?session_id=test' % quote(self.prepare_new_usecase().name()), data=upd_env_body, content_type='application/json')
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
    self.assertGreater(message.find('updated'), -1, 'The usecase was not successfully updated')

    rv = self.app.get('/api/usecases/name/%s?session_id=test' % quote(usecase_to_update.name()))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    upd_usecase = jsonpickle.decode(responseData)
    self.assertIsNotNone(upd_usecase, 'Unable to decode JSON data')
    self.logger.debug('[%s] Response data: %s', method, responseData)
    self.logger.info('[%s] UseCase: %s\n', method, upd_usecase['theName'])

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
    new_usecase.theReferenceContributions = [UseCaseContributionModel('Security delegated',{'theMeansEnd':'means','theContribution':'SomePositive'})]
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
