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
from cairis.mio.ModelImport import importModelFile,importProcessesFile
import cairis.core.BorgFactory
from cairis.core.Borg import Borg

__author__ = 'Shamal Faily'


class CodeTests(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    cairis.core.BorgFactory.initialise()
    importModelFile(os.environ['CAIRIS_SRC'] + '/test/webinos.xml',1)

  def setUp(self):
    os.environ['OUTPUT_DIR'] = '/tmp'

  def tearDown(self):
    pass

  def testImportProcesses(self):
    importProcessesFile(os.environ['CAIRIS_SRC'] + '/test/installCodes.xml',0)
    importProcessesFile(os.environ['CAIRIS_SRC'] + '/test/coding.xml',0)
    importProcessesFile(os.environ['CAIRIS_SRC'] + '/test/processes.xml',0)
