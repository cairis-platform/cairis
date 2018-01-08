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
from cairis.mio.ModelImport import importModelFile, importLocationsFile
import cairis.core.BorgFactory
from cairis.core.Borg import Borg

__author__ = 'Shamal Faily'


class TraceTests(unittest.TestCase):

  def setUp(self):
    cairis.core.BorgFactory.initialise()
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/NeuroGrid/NeuroGrid.xml',1,'test')

  def testTraces(self):
    b = Borg()  

    fromDims = b.dbProxy.getTraceDimensions('requirement',1)
    self.assertEqual(len(fromDims),6)
    toDims = b.dbProxy.getTraceDimensions('requirement',0)
    self.assertEqual(len(toDims),2)

    reqId = b.dbProxy.getDimensionId('Dataset policy','requirement')
    vulId = b.dbProxy.getDimensionId('Certificate ubiquity','vulnerability')
    b.dbProxy.addTrace('requirement_vulnerability',reqId,vulId)

    traces = b.dbProxy.removableTraces('Psychosis')
    self.assertEqual(len(traces),3)
    self.assertEqual(traces[0][0],'requirement')
    self.assertEqual(traces[0][1],'Dataset policy')
    self.assertEqual(traces[0][2],'vulnerability')
    self.assertEqual(traces[0][3],'Certificate ubiquity')

    b.dbProxy.deleteTrace('requirement','Dataset policy','vulnerability','Certificate ubiquity')
    traces = b.dbProxy.removableTraces('Psychosis')
    self.assertEqual(len(traces),2)
