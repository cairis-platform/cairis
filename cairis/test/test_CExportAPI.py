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
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
from cairis.mio.ModelImport import importModelFile
from cairis.mio.ModelImport import importComponentViewFile, importSecurityPatternsFile
from cairis.mio.TVTypeContentHandler import TVTypeContentHandler
from cairis.mio.ArchitecturalPatternContentHandler import ArchitecturalPatternContentHandler
from cairis.mio.SecurityPatternContentHandler import SecurityPatternContentHandler
import os
import xml.sax

__author__ = 'Shamal Faily'

class CExportTests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    importModelFile(os.environ['CAIRIS_SRC'] + '/test/webinos.xml',1,'test')
    importComponentViewFile(os.environ['CAIRIS_SRC'] + '/test/ContextPolicyManagement.xml','test')
    importSecurityPatternsFile(os.environ['CAIRIS_SRC'] + '/test/test_security_patterns.xml','test')

  def setUp(self):
    self.logger = logging.getLogger(__name__)

  def test_cexport_data_get(self):
    method = 'test_cexport_file_get?session_id=test'
    url = '/api/export/file?session_id=test&filename=test.xml'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    self.assertIsNone(xml.sax.parseString(rv.data,TVTypeContentHandler()))

  def test_cexport_architecturalpattern_get(self):
    method = 'test_cexport_architecturalpattern_get?session_id=test'
    url = '/api/export/file/architectural_pattern/Context%20Policy%20Management?session_id=test'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    self.assertIsNone(xml.sax.parseString(rv.data,ArchitecturalPatternContentHandler()))

  def test_cexport_securitypatterns_get(self):
    method = 'test_cexport_securitypatterns_get?session_id=test'
    url = '/api/export/file/security_patterns?session_id=test'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    self.assertIsNone(xml.sax.parseString(rv.data,SecurityPatternContentHandler()))

  def test_cexport_grl_get(self):
    method = 'test_cexport_grl_get?session_id=test'
    url = '/api/export/grl/task/Report Disorder/persona/Peter/environment/Complete?session_id=test'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')

  def test_user_goals_get(self):
    method = 'test_cexport_user_goals_get?session_id=test'
    url = '/api/export/file/user_goals?session_id=test&filename=apiwb&fileType=xlsx'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    f = open('/tmp/newwb.xlsx','wb')
    f.write(rv.data)
    f.close()

  def test_persona_characteristics_get(self):
    method = 'test_cexport_persona_characteristics_get?session_id=test'
    url = '/api/export/file/persona_characteristics?session_id=test&filename=pcwb&fileType=xlsx'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    f = open('/tmp/newpcwb.xlsx','wb')
    f.write(rv.data)
    f.close()
