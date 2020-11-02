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
from cairis.core.DataFlow import DataFlow
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
import os
from cairis.mio.ModelImport import importModelFile
from cairis.tools.ModelDefinitions import DataFlowModel

__author__ = 'Shamal Faily'


class DataFlowAPITests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    importModelFile(os.environ['CAIRIS_SRC'] + '/test/DFDTestModel.xml',1,'test')

  
  def setUp(self):
    # region Class fields
    self.logger = logging.getLogger(__name__)

    self.existing_dataflow_name = 'authenticate'
    self.existing_environment_name = 'Psychosis'
    self.existing_from_name = 'Authorised Researcher'
    self.existing_from_type = 'entity'
    self.existing_to_name = 'Authenticate Researcher'
    self.existing_to_type = 'process'
    self.existing_type = 'Information'
    self.existing_assets = ['Credentials']
    self.existing_tags = []

    dataflow_class = DataFlow.__module__+'.'+DataFlow.__name__
    # endregion

  def test_get_all(self):
    method = 'test_get_all'
    rv = self.app.get('/api/dataflows?session_id=test')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    dataflows = jsonpickle.decode(responseData)
    self.assertIsNotNone(dataflows, 'No results after deserialization')
    self.assertIsInstance(dataflows, list, 'The result is not a dictionary as expected')
    self.assertGreater(len(dataflows), 0, 'No dataflows in the dictionary')
    self.logger.info('[%s] DataFlows found: %d', method, len(dataflows))
    self.assertEqual(len(dataflows),2)

  def test_get_by_name(self):
    method = 'test_get_by_name'
    url = '/api/dataflows/name/' + quote(self.existing_dataflow_name) + '/from_name/' + self.existing_from_name + '/from_type/' + self.existing_from_type + '/to_name/' + self.existing_to_name + '/to_type/' + self.existing_to_type + '/environment/' + quote(self.existing_environment_name) + '?session_id=test'
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    dataflow = jsonpickle.decode(responseData)
    self.assertIsNotNone(dataflow, 'No results after deserialization')
    self.assertEqual(dataflow['theName'],self.existing_dataflow_name)
    self.assertEqual(dataflow['theType'],self.existing_type)
    self.assertEqual(dataflow['theEnvironmentName'],self.existing_environment_name)
    self.assertEqual(dataflow['theFromName'],self.existing_from_name)
    self.assertEqual(dataflow['theFromType'],self.existing_from_type)
    self.assertEqual(dataflow['theToName'],self.existing_to_name)
    self.assertEqual(dataflow['theToType'],self.existing_to_type)
    self.assertEqual(dataflow['theTags'],self.existing_tags)

  def test_post(self):
    method = 'test_post'
    url = '/api/dataflows'
    self.logger.info('[%s] URL: %s', method, url)
    new_dataflow_body = self.prepare_json()

    rv = self.app.post(url, content_type='application/json', data=new_dataflow_body)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    self.assertEqual(json_resp['message'],'acknowledge created')
    rv = self.app.delete('/api/dataflows/name/acknowledge/from_name/Authenticate Researcher/from_type/process/to_name/Authorised Researcher/to_type/entity/environment/Psychosis?session_id=test')

  def test_put(self):
    method = 'test_put'
    url = '/api/dataflows'
    self.logger.info('[%s] URL: %s', method, url)
    new_dataflow_body = self.prepare_json()

    rv = self.app.post(url, content_type='application/json', data=new_dataflow_body)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')

    dataflow_to_update = self.prepare_new_dataflow()
    dataflow_to_update.theName = 'Edited test dataflow'
    upd_env_body = self.prepare_json(dataflow=dataflow_to_update)
    rv = self.app.put('/api/dataflows/name/acknowledge/from_name/Authenticate%20Researcher/from_type/process/to_name/Authorised%20Researcher/to_type/entity/environment/Psychosis?session_id=test', data=upd_env_body, content_type='application/json')
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp)
    self.assertEqual(json_resp['message'],'Edited test dataflow updated')

    rv = self.app.get('/api/dataflows/name/Edited%20test%20dataflow/from_name/' + dataflow_to_update.fromName() + '/from_type/' + dataflow_to_update.fromType() + '/to_name/' + dataflow_to_update.toName() + '/to_type/' + dataflow_to_update.toType() + '/environment/Psychosis?session_id=test')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    upd_dataflow = jsonpickle.decode(responseData)
    self.assertIsNotNone(upd_dataflow, 'Unable to decode JSON data')

    self.assertEqual(upd_dataflow['theName'],dataflow_to_update.name())
    self.assertEqual(upd_dataflow['theType'],dataflow_to_update.type())
    self.assertEqual(upd_dataflow['theEnvironmentName'],dataflow_to_update.environment())
    self.assertEqual(upd_dataflow['theFromName'],dataflow_to_update.fromName())
    self.assertEqual(upd_dataflow['theFromType'],dataflow_to_update.fromType())
    self.assertEqual(upd_dataflow['theToName'],dataflow_to_update.toName())
    self.assertEqual(upd_dataflow['theToType'],dataflow_to_update.toType())
    self.assertEqual(upd_dataflow['theTags'],dataflow_to_update.tags())

    rv = self.app.delete('/api/dataflows/name/Edited%20test%20dataflow/from_name/' + dataflow_to_update.fromName() + '/from_type/' + dataflow_to_update.fromType() + '/to_name/' + dataflow_to_update.toName() + '/to_type/' + dataflow_to_update.toType() + '/environment/Psychosis?session_id=test')
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp)
    self.assertEqual(json_resp['message'],'Edited test dataflow / ' + dataflow_to_update.fromName() + ' / ' + dataflow_to_update.toName() + ' / Psychosis deleted')

  def test_dataflow_diagram(self):
    url = '/api/dataflows/diagram/environment/Psychosis/filter_type/None/filter_name/None?session_id=test'
    method = 'test_dataflow_datagram'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url, content_type='application/json')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    self.assertIsNotNone(responseData, 'No results after deserialization')
    self.assertEqual(responseData.find('svg'),1)

  def test_control_structure(self):
    url = '/api/dataflows/control_structure/environment/Psychosis/filter_name/None?session_id=test'
    method = 'test_control_structure'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url, content_type='application/json')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    self.assertIsNotNone(responseData, 'No results after deserialization')


  def prepare_new_dataflow(self):
    new_dataflow = DataFlow(
      dfName='acknowledge',
      dfType='Information',
      envName='Psychosis',
      fromName='Authenticate Researcher',
      fromType='process',
      toName='Authorised Researcher',
      toType='entity',
      dfAssets=['Session'],
      dfObs=[{'theObstacleName':'XSS Exploit','theKeyword':'not applicable','theContext':'Not applicable'}],
      dfTags=['tag1']
    )
    return new_dataflow

  def prepare_dict(self, dataflow=None):
    if dataflow is None:
      dataflow = self.prepare_new_dataflow()
    else:
      assert isinstance(dataflow, DataFlow)

    return {
      'session_id': 'test',
      'object': dataflow,
    }

  def prepare_json(self, data_dict=None, dataflow=None):
    if data_dict is None:
      data_dict = self.prepare_dict(dataflow=dataflow)
    else:
      assert isinstance(data_dict, dict)
    new_dataflow_body = jsonpickle.encode(data_dict, unpicklable=False)
    self.logger.info('JSON data: %s', new_dataflow_body)
    return new_dataflow_body
