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
import cairis.core.MisuseCaseFactory

__author__ = 'Shamal Faily'


class MisuseCaseFactoryTests(unittest.TestCase):

  def setUp(self):
    cairis.core.BorgFactory.initialise()
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/NeuroGrid/NeuroGrid.xml',1,'test')

  def testBuildMisuseCase(self):
    mc = cairis.core.MisuseCaseFactory.build('Social Engineering','Certificate ubiquity')
    mcEnv = mc.theEnvironmentProperties[0]
    self.assertEqual(mcEnv.theEnvironmentName,'Psychosis')
    self.assertEqual(mcEnv.theLikelihood,'Occasional')
    self.assertEqual(mcEnv.theSeverity,'Critical')
    self.assertEqual(mcEnv.theRiskRating.rating,'Undesirable')
    self.assertEqual(mcEnv.theObjective,'Exploit vulnerabilities in User certificate to threaten User certificate,Client workstation.')

