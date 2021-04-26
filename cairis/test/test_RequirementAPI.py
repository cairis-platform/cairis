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
import json
from cairis.core.Requirement import Requirement
from cairis.core.Trace import Trace
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
import os
from cairis.mio.ModelImport import importModelFile

__author__ = 'Robin Quetin, Shamal Faily'



class RequirementAPITests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/NeuroGrid/NeuroGrid.xml',1,'test')

  def setUp(self):
    # region Class fields
    self.logger = logging.getLogger(__name__)
    self.existing_asset_name = 'Analysis data'
    self.existing_environment_name = 'Core Technology'
    self.requirement_class = Requirement.__module__+'.'+Requirement.__name__
    self.new_requirement = {
      'theLabel' : '1',
      'theName' : 'Test requirement',
      'theDescription' : 'This is a test description',
      'thePriority' : '1',
      'theRationale' : 'This is to test the requirements controller',
      'theFitCriterion' : 'None',
      'theOriginator' : 'Student',
      'theType' : 'Functional',
      'theDomain' : 'Analysis data',
      'theDomainType' : 'asset'
    }
    self.new_requirement_dict = {
      'session_id': 'test',
      'object': self.new_requirement,
    }
    self.new_requirement_body = json.dumps(self.new_requirement_dict)
    self.to_delete_ids = []
    # endregion
    self.logger.info('JSON data: %s', self.new_requirement_body)

  def test_get_all(self):
    method = 'test_get_all'
    rv = self.app.get('/api/requirements?session_id=test')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    requirements = jsonpickle.decode(responseData)
    self.assertIsNotNone(requirements, 'No results after deserialization')
    self.assertIsInstance(requirements, list, 'The result is not a dictionary as expected')
    assert isinstance(requirements, list)
    self.assertGreater(len(requirements), 0, 'No requirements in the dictionary')
    self.logger.info('[%s] Requirements found: %d', method, len(requirements))
    self.logger.info('[%s] First requirement: %s [%d]\n', method, requirements[0]['theName'])

  def test_post(self):
    method = 'test_post'
    url = '/api/requirements?asset=%s' % quote(self.existing_asset_name)
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.post(url, content_type='application/json', data=self.new_requirement_body)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')

  def test_get_asset_name(self):
    method = 'test_asset_get_name'
    url = '/api/requirements/asset/%s?session_id=test' % quote(self.existing_asset_name)
    rv = self.app.get(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.assertIsNotNone(responseData, 'No response')
    self.logger.debug('[%s] Response data: %s', method, responseData)
    requirements = jsonpickle.decode(responseData)
    self.assertIsNotNone(requirements, 'No results after deserialization')
    self.assertGreater(len(requirements), 0, 'No requirements found for this environment')
    self.logger.info('[%s] Requirement: %s [%d]\n', method, requirements[0]['theName'])

  def test_get_just_asset_name(self):
    method = 'test_asset_get_name'
    url = '/api/requirements/asset/%s/names?session_id=test' % quote(self.existing_asset_name)
    rv = self.app.get(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.assertIsNotNone(responseData, 'No response')
    self.logger.debug('[%s] Response data: %s', method, responseData)
    requirements = jsonpickle.decode(responseData)
    self.assertIsNotNone(requirements, 'No results after deserialization')
    self.assertGreater(len(requirements), 0, 'No requirements found for this environment')

  def test_get_environment_name(self):
    method = 'test_environment_get_name'
    url = '/api/requirements/environment/%s?session_id=test' % quote(self.existing_environment_name)
    rv = self.app.get(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.assertIsNotNone(responseData, 'No response')
    self.logger.debug('[%s] Response data: %s', method, responseData)
    requirements = jsonpickle.decode(responseData)
    self.assertIsNotNone(requirements, 'No results after deserialization')
    if len(requirements) > 0:
      self.logger.info('[%s] Requirement: %s\n', method, requirements[0]['theName'])

  def test_get_just_environment_name(self):
    method = 'test_asset_get_name'
    url = '/api/requirements/environment/%s/names?session_id=test' % quote(self.existing_environment_name)
    rv = self.app.get(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.assertIsNotNone(responseData, 'No response')
    self.logger.debug('[%s] Response data: %s', method, responseData)
    requirements = jsonpickle.decode(responseData)
    self.assertIsNotNone(requirements, 'No results after deserialization')

  def test_x_put(self):
    method = 'test_x_put'

    url = '/api/requirements?asset=%s' % quote(self.existing_asset_name)
    rv = self.app.post(url, content_type='application/json', data=self.new_requirement_body)

    upd_requirement = self.new_requirement
    upd_requirement['theName'] = 'Test2'
    upd_requirement_dict = self.new_requirement_dict
    upd_requirement_dict['object'] = upd_requirement
    upd_requirement_body = json.dumps(upd_requirement_dict)
    self.logger.info('[%s] JSON data: %s', method, upd_requirement_body)

    rv = self.app.put('/api/requirements/name/Analysis%20data', content_type='application/json', data=upd_requirement_body)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    message = json_resp.get('message', None)
    self.assertIsNotNone(message, 'No message returned')
    self.logger.info('Message: %s', message)

    rv = self.app.get('/api/requirements?session_id=test')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    requirements = jsonpickle.decode(responseData)
    requirement = requirements[0]
    self.assertIsNotNone(requirement, 'Requirement not updated as expected')
    self.logger.info('[%s] Requirement: %s\n', method, requirement['theName'])

  def test_concept_map_model(self):
    url = '/api/requirements?environment=%s' % quote('Psychosis')
    reqBody1 = self.new_requirement_dict
    reqBody1['object']['theLabel']='1'
    reqBody1['object']['theName']='OneRequirement'
    reqBody1['object']['theDescription']='OneRequirement description'
    rv = self.app.post(url, content_type='application/json', data=json.dumps(reqBody1))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')

    reqBody2 = self.new_requirement_dict
    reqBody2['object']['theLabel']='2'
    reqBody2['object']['theName']='AnotherRequirement'
    reqBody2['object']['theDescription']='AnotherRequirement description'
    rv = self.app.post(url, content_type='application/json', data=json.dumps(reqBody2))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')

    aTrace = Trace(fObjt = 'requirement',fName ='OneRequirement',tObjt = 'requirement', tName = 'AnotherRequirement')
    traceDict = {'session_id' : 'test', 'object' : aTrace} 
    rv = self.app.post('/api/traces', content_type='application/json', data=jsonpickle.encode(traceDict))

    url = '/api/requirements/model/environment/Psychosis/requirement/all?session_id=test'
    method = 'test_concept_map_model'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url, content_type='application/json')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    self.assertIsNotNone(responseData, 'No results after deserialization')
    self.assertEqual(responseData.find('svg'),1)
