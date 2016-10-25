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
from StringIO import StringIO
import jsonpickle
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
import os
from cairis.mio.ModelImport import importModelFile, importComponentViewFile

__author__ = 'Shamal Faily'


class ArchitecturalPatternAPITests(CairisDaemonTestCase):

  def setUp(self):
    # region Class fields
    self.logger = logging.getLogger(__name__)
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/NeuroGrid/NeuroGrid.xml',1,'test')
    importComponentViewFile(os.environ['CAIRIS_SRC'] + '/test/ContextPolicyManagement.xml','test')
    # endregion

  def test_architectural_patterns_get(self):
    url = '/api/architectural_patterns?session_id=test'
    method = 'test_architectural_patterns_get'
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    self.logger.debug('[%s] Response data: %s', method, rv.data)
    aps = jsonpickle.decode(rv.data)
    ap = aps[0]
    self.assertIsInstance(ap, dict, 'Response is not a valid JSON object')
    self.assertEqual(ap['theName'],'Context Policy Management')

  def test_architectural_pattern_get(self):
    url = '/api/architectural_patterns/name/Context%20Policy%20Management?session_id=test'
    method = 'test_architectural_pattern_get'
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    self.logger.debug('[%s] Response data: %s', method, rv.data)
    ap = jsonpickle.decode(rv.data)
    self.assertIsInstance(ap, dict, 'Response is not a valid JSON object')
    self.assertEqual(ap['theName'],'Context Policy Management')
