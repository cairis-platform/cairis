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
import os
import json
import jsonpickle
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
from cairis.mio.ModelImport import importModelFile
from cairis.tools.JsonConverter import json_deserialize
import os

__author__ = 'Shamal Faily'

class RiskLevelAPITests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/ACME_Water/ACME_Water.xml',1,'test')

  def setUp(self):
    self.logger = logging.getLogger(__name__)
    self.existing_asset_name = 'ICT PC'
    self.existing_threat_name = 'Password enumeration'

  def test_get_risk_level(self):
    method = 'test_get_risk_level'
    url = '/api/risk_level/asset/%s?session_id=test' % quote(self.existing_asset_name)
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    level = jsonpickle.decode(responseData)
    self.assertIsNotNone(level, 'No results after deserialization')
    self.assertIsInstance(level, int, 'The result is not an integer as expected')
    self.assertEqual(level, 9)

  def test_get_risk_level_by_environment(self):
    method = 'test_get_risk_level_by_environment'
    url = '/api/risk_level/asset/ICT%20Application/environment/Day?session_id=test'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    level = jsonpickle.decode(responseData)
    self.assertIsNotNone(level, 'No results after deserialization')
    self.assertIsInstance(level, int, 'The result is not an integer as expected')
    self.assertEqual(level, 9)

    url = '/api/risk_level/asset/ICT%20Application/environment/Night?session_id=test'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    level = jsonpickle.decode(responseData)
    self.assertIsNotNone(level, 'No results after deserialization')
    self.assertIsInstance(level, int, 'The result is not an integer as expected')
    self.assertEqual(level, 9)

  def test_get_risk_threat_level(self):
    method = 'test_get_risk_level'
    url = '/api/risk_level/asset/threat_type/' + quote(self.existing_asset_name) + '/' + quote(self.existing_threat_name) + '?session_id=test'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    level = jsonpickle.decode(responseData)
    self.assertIsNotNone(level, 'No results after deserialization')
    self.assertIsInstance(level, int, 'The result is not an integer as expected')
    self.assertEqual(level, 9)

  def test_get_risk_threat_level_by_environment(self):
    method = 'test_get_risk_level_by_environment'
    url = '/api/risk_level/asset/threat_type/ICT%20Application/Enumeration/environment/Day?session_id=test'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    level = jsonpickle.decode(responseData)
    self.assertIsNotNone(level, 'No results after deserialization')
    self.assertIsInstance(level, int, 'The result is not an integer as expected')
    self.assertEqual(level, 9)

    url = '/api/risk_level/asset/threat_type/ICT%20Application/Enumeration/environment/Night?session_id=test'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    level = jsonpickle.decode(responseData)
    self.assertIsNotNone(level, 'No results after deserialization')
    self.assertIsInstance(level, int, 'The result is not an integer as expected')
    self.assertEqual(level, 0)


