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
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
import os
from cairis.mio.ModelImport import importModelFile

__author__ = 'Shamal Faily'


class DimensionAPITests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/NeuroGrid/NeuroGrid.xml',1,'test')

  
  def setUp(self):
    # region Class fields
    self.logger = logging.getLogger(__name__)  
    # endregion

  def test_get_all_dimensions(self):
    method = 'test_get_all_dimensions'
    rv = self.app.get('/api/dimensions/table/role?session_id=test')
    dims = jsonpickle.decode(rv.data)
    self.assertIsNotNone(dims, 'No results after deserialization')
    self.assertIsInstance(dims, list, 'The result is not a dict as expected')
    self.assertGreater(len(dims), 0, 'No dimensions in the dictionary')
    self.assertEqual(len(dims), 8, 'Incorrect number of role names returned')
    dimValue = dims[0]
    self.logger.info('[%s] First role: %s\n', method, dimValue)

  def test_get_all_dimensions_by_environment(self):
    method = 'test_get_all_dimensions_by_environment'
    url = '/api/dimensions/table/asset/environment/Psychosis?session_id=test'
    rv = self.app.get(url)
    dims = jsonpickle.decode(rv.data)
    self.assertIsNotNone(dims, 'No results are deserialization')
    self.assertGreater(len(dims), 0, 'No dimensions in the dictionary')
    self.assertEqual(len(dims), 12, 'Incorrect number of asset names returned')
    dimValue = dims[0]
    self.logger.info('[%s] First asset: %s\n', method, dimValue)
