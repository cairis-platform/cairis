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
from cairis.mio.ModelExport import exportModel,exportJSON,exportRedmineScenarios,exportRedmineUseCases,exportGRL,exportUserGoalWorkbook
import cairis.core.BorgFactory
from cairis.core.Borg import Borg

__author__ = 'Shamal Faily'


class ModelExportTests(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    cairis.core.BorgFactory.initialise()
# Uncommenting the below and commenting the other setup lines might be useful if you want to test exporting using different models
#    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/NeuroGrid/NeuroGrid.xml',1)
#    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/ACME_Water/ACME_Water.xml',1)
    importModelFile(os.environ['CAIRIS_SRC'] + '/test/webinos_incomplete.xml',1)
    importTVTypeFile(os.environ['CAIRIS_SRC'] + '/test/OWASPTypes.xml',0)
    importTVTypeFile(os.environ['CAIRIS_SRC'] + '/../examples/threat_vulnerability_types/cwecapec_tv_types.xml',0)
    importDirectoryFile(os.environ['CAIRIS_SRC'] + '/../examples/directories/owasp_directory.xml',0)
    importDirectoryFile(os.environ['CAIRIS_SRC'] + '/../examples/directories/cwecapec_directory.xml',0)
    importDirectoryFile(os.environ['CAIRIS_SRC'] + '/test/D28TV.xml',0)
    importComponentViewFile(os.environ['CAIRIS_SRC'] + '/test/ContextPolicyManagement.xml',0)
    importAttackPattern(os.environ['CAIRIS_SRC'] + '/test/XACMLAttackPattern.xml',0)
    importModelFile(os.environ['CAIRIS_SRC'] + '/test/misusability.xml',0)

  def setUp(self):
    os.environ['OUTPUT_DIR'] = '/tmp'

  def tearDown(self):
    pass

  def testExportModel(self):
    outFile = '/tmp/exportedModel.xml'
    self.assertEqual(exportModel(outFile),'Exported model')
    self.assertEqual(os.path.isfile(outFile),True)

  def testExportJSON(self):
    outFile = '/tmp/export.json'
    self.assertEqual(exportJSON(outFile),'Exported JSON')
    self.assertEqual(os.path.isfile(outFile),True)

  def testExportRedmineScenarios(self):
    outFile = '/tmp/exportedScenarios.txt'
    self.assertEqual(exportRedmineScenarios(outFile),'Exported 32 scenarios.')
    self.assertEqual(os.path.isfile(outFile),True)

  def testExportRedmineGoals(self):
    b = Borg()
    b.dbProxy.relabelGoals('Complete')
    b.dbProxy.redmineGoals('Complete')

  def testExportRedmineRequirements(self):
    b = Borg()
    b.dbProxy.getRedmineRequirements()

  def testExportRedmineUseCases(self):
    outFile = '/tmp/exportedUseCases.txt'
    self.assertEqual(exportRedmineUseCases(outFile),'Exported 62 use cases.')
    self.assertEqual(os.path.isfile(outFile),True)

  def testExportArchitecture(self):
    b = Borg()
    b.dbProxy.redmineArchitecture()
    b.dbProxy.redmineArchitectureSummary('Complete')
    b.dbProxy.architecturalPatternToXml('Context Policy Management')

  def testExportAttackPatterns(self):
    b = Borg()
    b.dbProxy.redmineAttackPatterns()
    b.dbProxy.redmineAttackPatternsSummary('Complete')

  def testExportPersona(self):
    b = Borg()
    b.dbProxy.personaToXml('Helen')

  def testExportGRL(self):
    outFile = '/tmp/exportedGRL.grl'
    self.assertEqual(exportGRL(outFile,'all','Unsafe application install','Complete'),'Exported GRL for all in tasks Unsafe application install situated in environment Complete')
    self.assertEqual(os.path.isfile(outFile),True)

  def testExportUserGoalWorkbook(self):
    outFile = '/tmp/ugwb.xlsx'
    exportUserGoalWorkbook(outFile)
    self.assertEqual(os.path.isfile(outFile),True)
