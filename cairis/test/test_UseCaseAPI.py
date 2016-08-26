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
from cairis.core.UseCase import UseCase
from cairis.core.UseCaseEnvironmentProperties import UseCaseEnvironmentProperties
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
import os
from cairis.mio.ModelImport import importModelFile, importUsabilityFile
from cairis.tools.PseudoClasses import StepsAttributes, StepAttributes

__author__ = 'Shamal Faily'


class UseCaseAPITests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/NeuroGrid/NeuroGrid.xml',1,'test')
    importModelFile(os.environ['CAIRIS_SRC'] + '/test/testusecase.xml',0,'test')
  
  def setUp(self):
    # region Class fields
    self.logger = logging.getLogger(__name__)
    self.existing_usecase_name = 'Test use case'
    usecase_class = UseCase.__module__+'.'+UseCase.__name__
    # endregion

  def test_get_all(self):
    method = 'test_get_all'
    rv = self.app.get('/api/usecases?session_id=test')
    usecases = jsonpickle.decode(rv.data)
    self.assertIsNotNone(usecases, 'No results after deserialization')
    self.assertIsInstance(usecases, dict, 'The result is not a dictionary as expected')
    self.assertGreater(len(usecases), 0, 'No usecases in the dictionary')
    self.logger.info('[%s] Use Cases found: %d', method, len(usecases))
    usecase = usecases.values()[0]
    self.logger.info('[%s] First usecase: %s [%d]\n', method, usecase['theName'], usecase['theId'])

  def test_get_by_name(self):
    method = 'test_get_by_name'
    url = '/api/usecases/name/%s?session_id=test' % quote(self.existing_usecase_name)
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    self.logger.debug('[%s] Response data: %s', method, rv.data)
    usecase = jsonpickle.decode(rv.data)
    self.assertIsNotNone(usecase, 'No results after deserialization')
    self.logger.info('[%s] UseCase: %s [%d]\n', method, usecase['theName'], usecase['theId'])
