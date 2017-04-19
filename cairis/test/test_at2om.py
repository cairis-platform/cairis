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
import pydot
import os
import logging
from cairis.mio.ModelImport import importModelFile,importAttackTreeString
from cairis.bin.at2om import dotToObstacleModel
import cairis.core.BorgFactory
from cairis.core.Borg import Borg

__author__ = 'Shamal Faily'


class AttackTreeToObstacleModelTests(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    cairis.core.BorgFactory.initialise()
    importModelFile(os.environ['CAIRIS_SRC'] + '/test/webinos.xml',1)

  def setUp(self):
    pass

  def tearDown(self):
    pass

  def testxImportSpreadsheet(self):
    dotInstance = pydot.graph_from_dot_file(os.environ['CAIRIS_SRC'] + '/test/Exploit_vsftpd_backdoor_graphviz.dot')
    xmlBuf = dotToObstacleModel(dotInstance[0],'Complete','Anon')
    importAttackTreeString(xmlBuf)
