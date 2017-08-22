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
from io import StringIO
import jsonpickle
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
from cairis.tools.ModelDefinitions import ObjectDependencyModel
import os
from cairis.mio.ModelImport import importModelFile

__author__ = 'Shamal Faily'


class ObjectDependencyAPITests(CairisDaemonTestCase):

  def setUp(self):
    # region Class fields
    self.logger = logging.getLogger(__name__)
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/NeuroGrid/NeuroGrid.xml',1,'test')
    # endregion

  def test_object_dependency_get(self):
    url = '/api/object_dependency/dimension/asset/object/Portal?session_id=test'
    method = 'test_object_dependency_get'
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else: 
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    deps = jsonpickle.decode(responseData)
    self.assertIsInstance(deps, dict, 'Response is not a valid JSON object')
    self.assertEqual(len(deps['theDependencies']),5)
    objtDep = deps['theDependencies'][0]
    self.assertEqual(objtDep['theDimensionName'],'obstacle')
    self.assertEqual(objtDep['theObjectName'],'Insecure internal data transmission')

  def test_object_dependency_delete(self):
    url = '/api/object_dependency/dimension/asset/object/Portal?session_id=test'
    method = 'test_object_dependency_delete'
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

