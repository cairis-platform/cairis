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

import unittest
import os
import logging
from cairis.mio.ModelImport import importTVTypeFile,importModelFile,importAttackPattern,importComponentViewFile,importDirectoryFile
from cairis.mio.ModelExport import exportModel,exportRedmineScenarios,exportRedmineRequirements,exportRedmineUseCases,exportArchitecture,exportAttackPatterns
import cairis.core.BorgFactory
from cairis.core.Borg import Borg

__author__ = 'Shamal Faily'


class ModelExportTests(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    cairis.core.BorgFactory.initialise()
    importModelFile(os.environ['CAIRIS_SRC'] + '/test/webinos.xml',1)
    importTVTypeFile(os.environ['CAIRIS_SRC'] + '/test/OWASPTypes.xml',0)
    importTVTypeFile(os.environ['CAIRIS_SRC'] + '/../examples/threat_vulnerability_types/cwecapec_tv_types.xml',0)
    importDirectoryFile(os.environ['CAIRIS_SRC'] + '/../examples/directories/owasp_directory.xml',0)
    importDirectoryFile(os.environ['CAIRIS_SRC'] + '/../examples/directories/cwecapec_directory.xml',0)
    importDirectoryFile(os.environ['CAIRIS_SRC'] + '/test/D28TV.xml',0)
    importComponentViewFile(os.environ['CAIRIS_SRC'] + '/test/ContextPolicyManagement.xml',0)
    importAttackPattern(os.environ['CAIRIS_SRC'] + '/test/XACMLAttackPattern.xml',0)

  def setUp(self):
    os.environ['OUTPUT_DIR'] = '/tmp'

  def tearDown(self):
    pass

  def testExportModel(self):
    outFile = '/tmp/exportedModel.xml'
    self.assertEqual(exportModel(outFile),'Exported model')
    self.assertEqual(os.path.isfile(outFile),True)

  def testExportRedmineScenarios(self):
    outFile = '/tmp/exportedScenarios.txt'
    self.assertEqual(exportRedmineScenarios(outFile),'Exported 32 scenarios.')
    self.assertEqual(os.path.isfile(outFile),True)

  def testExportRedmineRequirements(self):
    outFile = '/tmp/exportedRequirements.txt'
    self.assertEqual(exportRedmineRequirements(outFile),'Exported requirements')
    self.assertEqual(os.path.isfile(outFile),True)

  def testExportRedmineUseCases(self):
    outFile = '/tmp/exportedUseCases.txt'
    self.assertEqual(exportRedmineUseCases(outFile),'Exported 62 use cases.')
    self.assertEqual(os.path.isfile(outFile),True)

  def testExportArchitecture(self):
    outFile = '/tmp/exportedArchitecture.txt'
    self.assertEqual(exportArchitecture(outFile),'Exported 7 architectural patterns.')
    self.assertEqual(os.path.isfile(outFile),True)

  def testExportAttackPatterns(self):
    outFile = '/tmp/exportedAttackPatterns.txt'
    self.assertEqual(exportAttackPatterns(outFile),'Exported 0 attack patterns.')
    self.assertEqual(os.path.isfile(outFile),True)
