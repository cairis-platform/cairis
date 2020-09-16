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
  from io import BytesIO
else:
  from urllib import quote
  from StringIO import StringIO
import os
import jsonpickle
from cairis.core.Environment import Environment
from cairis.tools.PseudoClasses import EnvironmentTensionModel
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase

__author__ = 'Robin Quetin, Shamal Faily'


class CImportTests(CairisDaemonTestCase):

  xmlfile = os.environ['CAIRIS_SRC'] + '/../examples/exemplars/NeuroGrid/NeuroGrid.xml'
  dnFile1 = os.environ['CAIRIS_SRC'] + '/test/KnowledgeWork.xml'
  dnFile2 = os.environ['CAIRIS_SRC'] + '/test/classExample.xml'
  logger = logging.getLogger(__name__)

  def test_cimport_package_post(self):
    method = 'test_cimport_package_post'
    url = '/api/import/package'
    package = BytesIO(open(os.environ['CAIRIS_SRC'] + '/test/test.cairis','rb').read())
    rv = self.app.post('/api/import/package?session_id=test', data={
      'file': (package, 'test.cairis'),
    })
    responseData = rv.data.decode('utf-8')
    self.assertIsNotNone(responseData, 'No response')
    json_dict = jsonpickle.decode(responseData)
    self.assertIsInstance(json_dict, dict, 'The response is not a valid JSON dictionary')
    assert isinstance(json_dict, dict)
    message = json_dict.get('message')
    self.assertIsNotNone(message, 'Response does not contain a message')
    self.logger.info('[%s] Message: %s', method, message)

  def test_cimport_ugwb_post(self):
    method = 'test_cimport_ugwb_post'
    url = '/api/import/file/user_goals'
    wb = BytesIO(open(os.environ['CAIRIS_SRC'] + '/test/ngug.xlsx','rb').read())
    rv = self.app.post('/api/import/file/user_goals?session_id=test', data={
      'file': (wb, 'ngug.xlsx'),
    })
    responseData = rv.data.decode('utf-8')
    self.assertIsNotNone(responseData, 'No response')
    json_dict = jsonpickle.decode(responseData)
    self.assertIsInstance(json_dict, dict, 'The response is not a valid JSON dictionary')
    assert isinstance(json_dict, dict)
    message = json_dict.get('message')
    self.assertIsNotNone(message, 'Response does not contain a message')
    self.assertEqual(message, 'Imported 5 characteristic synopses, 7 reference synopses, and 4 reference contributions.')

  def test_cimport_pcwb_post(self):
    method = 'test_cimport_pcwb_post'
    url = '/api/import/file/persona_characteristics'
    wb = BytesIO(open(os.environ['CAIRIS_SRC'] + '/test/ngpc.xlsx','rb').read())
    rv = self.app.post('/api/import/file/persona_characteristics?session_id=test', data={
      'file': (wb, 'ngpc.xlsx'),
    })
    responseData = rv.data.decode('utf-8')
    self.assertIsNotNone(responseData, 'No response')
    json_dict = jsonpickle.decode(responseData)
    self.assertIsInstance(json_dict, dict, 'The response is not a valid JSON dictionary')
    assert isinstance(json_dict, dict)
    message = json_dict.get('message')
    self.assertIsNotNone(message, 'Response does not contain a message')
    self.assertEqual(message, 'Imported 2 external documents, 5 document references, and 2 persona characteristics.')


  def test_cimport_model_post(self):
    method = 'test_cimport_model_post'
    url = '/api/import/text'
    fs_xmlfile = open(self.xmlfile, 'rb')
    file_contents = fs_xmlfile.read()
    self.logger.info('[%s] URL: %s', method, url)
    self.logger.debug('[%s] XML file:\n%s', method, file_contents)

    urlenc_file_contents = quote(file_contents)
    json_dict = {
      'session_id': 'test',
      'object': {
        'urlenc_file_contents': urlenc_file_contents,
        'overwrite' : 1,
        'type': 'all'
      }
    }
    json_body = jsonpickle.encode(json_dict)
    rv = self.app.post(url, data=json_body, content_type='application/json')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.assertIsNotNone(responseData, 'No response')
    json_dict = jsonpickle.decode(responseData)
    self.assertIsInstance(json_dict, dict, 'The response is not a valid JSON dictionary')
    assert isinstance(json_dict, dict)
    message = json_dict.get('message')
    self.assertIsNotNone(message, 'Response does not contain a message')
    self.logger.info('[%s] Message: %s', method, message)

  def test_cimport_diagramsnet_dfd_post(self):
    method = 'test_cimport_diagramsnet_dfd_post'
    url = '/api/import/text'

    rv = self.app.post('/api/environments', content_type='application/json', data=self.defaultEnvBody())
    respBody = rv.data.decode('utf-8')
    json_resp = jsonpickle.decode(respBody)
    self.assertEqual(json_resp.get('message'),'Default created')

    fs_xmlfile = open(self.dnFile1, 'rb')
    file_contents = fs_xmlfile.read()

    urlenc_file_contents = quote(file_contents)
    json_dict = {
      'session_id': 'test',
      'object': {
        'urlenc_file_contents': urlenc_file_contents,
        'overwrite' : 1,
        'environment' : 'Default',
        'type': 'diagrams.net (Data Flow Diagram)'
      }
    }
    json_body = jsonpickle.encode(json_dict)
    rv = self.app.post(url, data=json_body, content_type='application/json')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.assertIsNotNone(responseData, 'No response')
    json_dict = jsonpickle.decode(responseData)
    self.assertIsInstance(json_dict, dict, 'The response is not a valid JSON dictionary')
    assert isinstance(json_dict, dict)
    message = json_dict.get('message')
    self.assertIsNotNone(message, 'Response does not contain a message')
    self.assertEqual(message,'Imported 4 assets, 1 use case, 2 data flows, and 1 trust boundary.')

    fs_xmlfile = open(self.dnFile2, 'rb')
    file_contents = fs_xmlfile.read()

    urlenc_file_contents = quote(file_contents)
    json_dict = {
      'session_id': 'test',
      'object': {
        'urlenc_file_contents': urlenc_file_contents,
        'overwrite' : 1,
        'environment' : 'Default',
        'type': 'diagrams.net (Asset Model)'
      }
    }
    json_body = jsonpickle.encode(json_dict)
    rv = self.app.post(url, data=json_body, content_type='application/json')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.assertIsNotNone(responseData, 'No response')
    json_dict = jsonpickle.decode(responseData)
    self.assertIsInstance(json_dict, dict, 'The response is not a valid JSON dictionary')
    assert isinstance(json_dict, dict)
    message = json_dict.get('message')
    self.assertIsNotNone(message, 'Response does not contain a message')
    self.assertEqual(message,'Imported 4 assets, and 3 asset associations.')

  def test_cimport_file_post(self):
    method = 'test_cimport_file_post'
    url = '/api/import/file/type/all?session_id=test'
    fs_xmlfile = open(self.xmlfile, 'rb')
    file_contents = fs_xmlfile.read()
    self.logger.info('[%s] URL: %s', method, url)
    self.logger.debug('[%s] XML file:\n%s', method, file_contents)
    if (sys.version_info > (3,)):
      buf = BytesIO(file_contents)
    else:
      buf = StringIO(file_contents)
    data = {
      'file': (buf, 'import.xml'),
      'session_id': 'test'
    }
    rv = self.app.post(url, data=data, content_type='multipart/form-data')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.assertIsNotNone(responseData, 'No response')
    json_dict = jsonpickle.decode(responseData)
    self.assertIsInstance(json_dict, dict, 'The response is not a valid JSON dictionary')
    assert isinstance(json_dict, dict)
    message = json_dict.get('message')
    self.assertIsNotNone(message, 'Response does not contain a message')
    self.logger.info('[%s] Message: %s', method, message)
    self.assertEqual(message,'import.xml imported')

  def defaultEnvBody(self):
    defaultEnv = Environment(-1,'Default','DEFAULT','Default environment',[],'','',[])

    for idx1 in range(0, 4):
      for idx2 in range(4, 8):
        tension = EnvironmentTensionModel(idx1,idx2,0,'None')
        defaultEnv.theTensions.append(tension)

    return jsonpickle.encode({'session_id' : 'test', 'object' : defaultEnv})
