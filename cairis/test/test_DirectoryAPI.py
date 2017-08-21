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
import json
import sys
if (sys.version_info > (3,)):
  from urllib.parse import quote
else:
  from urllib import quote
from io import StringIO
import os
import jsonpickle
import cairis.core.BorgFactory
from cairis.core.Borg import Borg
from cairis.core.Directory import Directory
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
from cairis.mio.ModelImport import importModelFile,importDirectoryFile
from cairis.tools.JsonConverter import json_deserialize

__author__ = 'Shamal Faily'

class DirectoryAPITests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/NeuroGrid/NeuroGrid.xml',1,'test')
    importDirectoryFile(os.environ['CAIRIS_SRC'] + '/../examples/directories/ics_directory.xml',0,'test')

  def setUp(self):
    self.logger = logging.getLogger(__name__)

  def test_get_threat_directory(self):
    method = 'test_get_threat_directory'
    url = '/api/directory/threat/all?session_id=test'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    tds = jsonpickle.decode(responseData)
    self.assertIsNotNone(tds, 'No results after deserialization')
    self.assertEqual(len(tds), 12)

  def test_get_threat_directory_name(self):
    method = 'test_get_threat_directory_by_name'
    url = '/api/directory/threat/Acts%20of%20nature%20causing%20system%20unavailability?session_id=test'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    tds = jsonpickle.decode(responseData)
    self.assertIsNotNone(tds, 'No results after deserialization')
    self.assertEqual(len(tds), 1)

  def test_get_vulnerability_directory(self):
    method = 'test_get_vulnerability_directory'
    url = '/api/directory/vulnerability/all?session_id=test'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    vds = jsonpickle.decode(responseData)
    self.assertIsNotNone(vds, 'No results after deserialization')
    self.assertEqual(len(vds), 10)

  def test_get_vulnerability_directory_name(self):
    method = 'test_get_vulnerability_directory'
    url = '/api/directory/vulnerability/Lack%20of%20risk%20assessment?session_id=test'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    vds = jsonpickle.decode(responseData)
    self.assertIsNotNone(vds, 'No results after deserialization')
    self.assertEqual(len(vds), 1)

  def tearDown(self):
    pass
