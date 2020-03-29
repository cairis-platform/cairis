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
from cairis.core.Countermeasure import Countermeasure
from cairis.core.Target import Target
from cairis.core.CountermeasureEnvironmentProperties import CountermeasureEnvironmentProperties
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
from cairis.tools.PseudoClasses import SecurityAttribute, CountermeasureTarget, CountermeasureTaskCharacteristics
import os
from cairis.mio.ModelImport import importModelFile, importSecurityPatternsFile

__author__ = 'Shamal Faily'


class CountermeasureAPITests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/NeuroGrid/NeuroGrid.xml',1,'test')
    importSecurityPatternsFile(os.environ['CAIRIS_SRC'] + '/../examples/architecture/schumacher_patterns.xml','test')
  
  def setUp(self):
    # region Class fields
    self.logger = logging.getLogger(__name__)

    self.existing_countermeasure_name = 'Location-based X.509 extension'
    self.existing_countermeasure_type = 'Information'
    self.existing_countermeasure_description = 'X.509 certificates extended to tie client workstations so NeuroGrid tasks can only be carried out on these.'
    self.existing_environment_name = 'Psychosis'
    self.existing_requirements = ['User certificate addressability']
    self.existing_targets = [CountermeasureTarget('Certificate Ubiquity','High','Discourages certificate sharing')]
    self.existing_properties = []
    self.existing_rationale =  ['None','None','None','None','None','None','None','None']
    self.existing_cost='Medium'
    self.existing_roles=['Data Consumer','Certificate Authority']
    self.existing_personas=[CountermeasureTaskCharacteristics('Upload data','Claire','None','None','None','Low Hindrance'),CountermeasureTaskCharacteristics('Download data','Claire','None','None','None','Low Hindrance')]

    countermeasure_class = Countermeasure.__module__+'.'+Countermeasure.__name__
    # endregion

  def test_get_all(self):
    method = 'test_get_all'
    rv = self.app.get('/api/countermeasures?session_id=test')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    countermeasures = jsonpickle.decode(responseData)
    self.assertIsNotNone(countermeasures, 'No results after deserialization')
    self.assertIsInstance(countermeasures, list, 'The result is not a list as expected')
    self.assertGreater(len(countermeasures), 0, 'No countermeasures in the dictionary')
    self.logger.info('[%s] Countermeasures found: %d', method, len(countermeasures))
    countermeasure = countermeasures[0]
    self.logger.info('[%s] First countermeasure: %s\n', method, countermeasure['theName'])

  def test_get_by_name(self):
    method = 'test_get_by_name'
    url = '/api/countermeasures/name/%s?session_id=test' % quote(self.existing_countermeasure_name)
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    countermeasure = jsonpickle.decode(responseData)
    self.assertIsNotNone(countermeasure, 'No results after deserialization')
    self.logger.info('[%s] Countermeasure: %s\n', method, countermeasure['theName'])

  def test_delete(self):
    method = 'test_delete'
    url = '/api/countermeasures/name/%s?session_id=test' % quote(self.prepare_new_countermeasure().name())
    new_countermeasure_body = self.prepare_json()

    self.app.delete(url)
    self.logger.info('[%s] Object to delete: %s', method, new_countermeasure_body)
    self.app.post('/api/countermeasures', content_type='application/json', data=new_countermeasure_body)
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.delete(url)
    self.logger.info('[%s] Response data: %s', method, rv.data)
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    json_resp = jsonpickle.decode(responseData)
    self.assertIsInstance(json_resp, dict, 'The response cannot be converted to a dictionary')
    message = json_resp.get('message', None)
    self.assertIsNotNone(message, 'No message in response')
    self.logger.info('[%s] Message: %s\n', method, message)

  def test_post(self):
    method = 'test_post'
    url = '/api/countermeasures'
    self.logger.info('[%s] URL: %s', method, url)
    new_countermeasure_body = self.prepare_json()

    self.app.delete('/api/countermeasures/name/%s?session_id=test' % quote(self.prepare_new_countermeasure().name()))
    rv = self.app.post(url, content_type='application/json', data=new_countermeasure_body)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    msg = json_resp.get('message', None)
    self.assertIsNotNone(msg, 'No message returned')
    self.logger.info('[%s] Message: %d\n', method, msg)
    rv = self.app.delete('/api/countermeasures/name/%s?session_id=test' % quote(self.prepare_new_countermeasure().name()))

  def test_target_names(self):
    method = 'test_countermeasure-targets-by-requirement-get'
    url = '/api/countermeasures/targets/environment/Psychosis?requirement=User%20certificate%20addressability&session_id=test'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    targetList = jsonpickle.decode(responseData)
    self.assertIsNotNone(targetList, 'No results after deserialization')
    self.assertGreater(len(targetList), 0, 'No targets returned')
    self.logger.info('[%s] Targets found: %d', method, len(targetList))
    self.assertEqual(len(targetList),2)

  def test_task_names(self):
    method = 'test_countermeasure-tasks-by-role-get'
    url = '/api/countermeasures/tasks/environment/Psychosis?role=Certificate%20Authority&role=Data%20Consumer&role=Researcher&session_id=test'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    taskList = jsonpickle.decode(responseData)
    self.assertIsNotNone(taskList, 'No results after deserialization')
    self.assertEqual(len(taskList),2)

  def test_put(self):
    method = 'test_put'
    url = '/api/countermeasures'
    self.logger.info('[%s] URL: %s', method, url)
    new_countermeasure_body = self.prepare_json()

    rv = self.app.delete('/api/countermeasures/name/%s?session_id=test' % quote(self.prepare_new_countermeasure().name()))
    rv = self.app.post(url, content_type='application/json', data=new_countermeasure_body)
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

    countermeasure_to_update = self.prepare_new_countermeasure()
    countermeasure_to_update.theName = 'Edited test countermeasure'
    upd_env_body = self.prepare_json(countermeasure=countermeasure_to_update)
    rv = self.app.put('/api/countermeasures/name/%s?session_id=test' % quote(self.prepare_new_countermeasure().name()), data=upd_env_body, content_type='application/json')
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
    self.assertGreater(message.find('updated'), -1, 'The countermeasure was not successfully updated')

    rv = self.app.get('/api/countermeasures/name/%s?session_id=test' % quote(countermeasure_to_update.name()))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    upd_countermeasure = jsonpickle.decode(responseData)
    self.assertIsNotNone(upd_countermeasure, 'Unable to decode JSON data')
    self.logger.debug('[%s] Response data: %s', method, rv.data)
    self.logger.info('[%s] Countermeasure: %s\n', method, upd_countermeasure['theName'])
    rv = self.app.delete('/api/countermeasures/name/%s?session_id=test' % quote(countermeasure_to_update.theName))

  def test_generate_asset(self):
    method = 'test_generate_asset'
    url = '/api/countermeasures/name/' + quote(self.existing_countermeasure_name) + '/generate_asset?session_id=test'
    self.logger.info('[%s] URL: %s', method, url)

    rv = self.app.post(url, content_type='application/json',data=jsonpickle.encode({'session_id':'test'}))
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    self.assertIsInstance(json_resp, dict)
    message = json_resp.get('message', None)
    self.assertIsNotNone(message, 'No message in response')
    self.logger.info('[%s] Message: %s\n', method, message)
    self.assertEqual(message,'Asset ' + self.existing_countermeasure_name + ' CM created')

  def test_generate_asset_from_template(self):
    method = 'test_generate_asset_from_template'
    url = '/api/countermeasures/name/' + quote(self.existing_countermeasure_name) + '/template_asset/PFFirewall/generate_asset?session_id=test'
    self.logger.info('[%s] URL: %s', method, url)

    rv = self.app.post(url, content_type='application/json',data=jsonpickle.encode({'session_id':'test'}))
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    self.assertIsInstance(json_resp, dict)
    message = json_resp.get('message', None)
    self.assertIsNotNone(message, 'No message in response')
    self.logger.info('[%s] Message: %s\n', method, message)
    self.assertEqual(message,'Asset PFFirewall created')

  def test_situate_countermeasure_pattern(self):
    method = 'test_situate_countermeasure_pattern'
    url = '/api/countermeasures/name/' + quote(self.existing_countermeasure_name) + '/security_pattern/Demilitarized%20Zone/situate?session_id=test'
    self.logger.info('[%s] URL: %s', method, url)

    rv = self.app.post(url, content_type='application/json',data=jsonpickle.encode({'session_id':'test'}))
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    self.assertIsInstance(json_resp, dict)
    message = json_resp.get('message', None)
    self.assertIsNotNone(message, 'No message in response')
    self.logger.info('[%s] Message: %s\n', method, message)
    self.assertEqual(message,'Demilitarized Zone situated')

  def test_associate_situated_pattern(self):
    method = 'test_situate_countermeasure_pattern'
    rv = self.app.post('/api/security_patterns/name/Protection%20Reverse%20Proxy/environment/Psychosis/situate', content_type='application/json',data=jsonpickle.encode({'session_id':'test'}))
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    json_resp = jsonpickle.decode(responseData)
    msg = json_resp.get('message', None)
    self.assertEqual(msg, 'Security Pattern successfully situated')

    rv = self.app.get('api/countermeasures/name/Location-based%20X.509%20extension/candidate_patterns?session_id=test')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    cps = jsonpickle.decode(responseData)
    self.assertEqual(cps[0],'Protection Reverse Proxy') 

    url = '/api/countermeasures/name/' + quote(self.existing_countermeasure_name) + '/security_pattern/Protection%20Reverse%20Proxy/associate_situated?session_id=test'
    self.logger.info('[%s] URL: %s', method, url)

    rv = self.app.post(url, content_type='application/json',data=jsonpickle.encode({'session_id':'test'}))
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    self.assertIsInstance(json_resp, dict)
    message = json_resp.get('message', None)
    self.assertIsNotNone(message, 'No message in response')
    self.logger.info('[%s] Message: %s\n', method, message)
    self.assertEqual(message,'Protection Reverse Proxy associated')

    rv = self.app.get('api/countermeasures/name/Location-based%20X.509%20extension/patterns?session_id=test')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    cps = jsonpickle.decode(responseData)
    self.assertEqual(cps[0],'Protection Reverse Proxy') 

    url = '/api/countermeasures/name/' + quote(self.existing_countermeasure_name) + '/security_pattern/Protection%20Reverse%20Proxy/remove_situated'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.delete(url, content_type='application/json',data=jsonpickle.encode({'session_id':'test'}))
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    self.assertIsInstance(json_resp, dict)
    message = json_resp.get('message', None)
    self.assertIsNotNone(message, 'No message in response')
    self.logger.info('[%s] Message: %s\n', method, message)
    self.assertEqual(message,'Situated pattern Protection Reverse Proxy removed')

    rv = self.app.get('api/countermeasures/name/Location-based%20X.509%20extension/patterns?session_id=test')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    cps = jsonpickle.decode(responseData)
    self.assertEqual(len(cps),0)


  def prepare_new_countermeasure(self):
    new_countermeasure_props = [
      CountermeasureEnvironmentProperties(
        environmentName=self.existing_environment_name,
        requirements=self.existing_requirements,
        targets=self.existing_targets,
        properties=self.existing_properties,
        rationale=self.existing_rationale,
        cost=self.existing_cost,
        roles=self.existing_roles,
        personas=self.existing_personas)
    ]

    new_countermeasure = Countermeasure(
      cmId=-1,
      cmName='New countermeasure',
      cmDesc='New CM description',
      cmType='Information',
      tags=[],
      cProps=[]
    )
    new_countermeasure.theEnvironmentProperties = new_countermeasure_props
    return new_countermeasure

  def prepare_dict(self, countermeasure=None):
    if countermeasure is None:
      countermeasure = self.prepare_new_countermeasure()
    else:
      assert isinstance(countermeasure, Countermeasure)

    return {
      'session_id': 'test',
      'object': countermeasure,
    }

  def prepare_json(self, data_dict=None, countermeasure=None):
    if data_dict is None:
      data_dict = self.prepare_dict(countermeasure=countermeasure)
    else:
      assert isinstance(data_dict, dict)
    new_countermeasure_body = jsonpickle.encode(data_dict, unpicklable=False)
    self.logger.info('JSON data: %s', new_countermeasure_body)
    return new_countermeasure_body
