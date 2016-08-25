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
from cairis.core.MisuseCase import MisuseCase
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
import os
from cairis.mio.ModelImport import importModelFile

__author__ = 'Robin Quetin, Shamal Faily'


class MisuseCaseAPITests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/NeuroGrid/NeuroGrid.xml',1,'test')

  def setUp(self):
    # region Class fields
    self.logger = logging.getLogger(__name__)
    self.existing_risk_name = 'Unauthorised Certificate Access'
    self.misuse_case_class = MisuseCase.__module__+'.'+MisuseCase.__name__
    # endregion

  def test_get_all(self):
    method = 'test_get_all'
    rv = self.app.get('/api/misusecases?session_id=test')
    misuse_cases = jsonpickle.decode(rv.data)
    self.assertIsNotNone(misuse_cases, 'No results after deserialization')
    self.assertIsInstance(misuse_cases, dict, 'The result is not a dictionary as expected')
    self.assertGreater(len(misuse_cases), 0, 'No misuse_cases in the dictionary')
    self.logger.info('[%s] MisuseCases found: %d', method, len(misuse_cases))
    misuse_case = misuse_cases.values()[0]
    self.logger.info('[%s] First misuse_case: %s [%d]\n', method, misuse_case['theName'], misuse_case['theId'])

  def test_get_by_name(self):
    method = 'test_get_by_risk'
    url = '/api/misusecases/risk/%s?session_id=test' % quote(self.existing_risk_name)
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    self.logger.debug('[%s] Response data: %s', method, rv.data)
    misuse_case = jsonpickle.decode(rv.data)
    self.assertIsNotNone(misuse_case, 'No results after deserialization')
    self.logger.info('[%s] MisuseCase: %s [%d]\n', method, misuse_case['theName'], misuse_case['theId'])
