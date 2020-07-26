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
import json
from subprocess import call
import cairis.core.BorgFactory
from cairis.core.Borg import Borg
import cairis.core.DefaultParametersFactory
from cairis.core.EnvironmentParameters import EnvironmentParameters

__author__ = 'Shamal Faily'


class DefaultParametersFactoryTest(unittest.TestCase):

  def setUp(self):
    call([os.environ['CAIRIS_CFG_DIR'] + "/initdb.sh"])
    cairis.core.BorgFactory.initialise()
    b = Borg()
    b.dbProxy.addEnvironment(EnvironmentParameters('Default','DEFAULT','Default Environment'))

  def testAddDefaultAsset(self):
    assetId = cairis.core.DefaultParametersFactory.build('TestAsset','Default','asset',None,'Information')
    b = Borg()
    objt = (b.dbProxy.getAssets(assetId))['TestAsset']

    self.assertEqual(objt.name(), 'TestAsset')
    self.assertEqual(objt.shortCode(),'TBD')
    self.assertEqual(objt.description(),'To be defined')
    self.assertEqual(objt.significance(),'To be defined')
    self.assertEqual(objt.tags(),[])
    p = (objt.environmentProperties())[0]
    self.assertEqual('Default', p.name())
    self.assertEqual(1, (p.properties()[2]))
    self.assertEqual('To be defined', p.rationale()[2])


  def testAddDefaultUseCase(self):
    ucId = cairis.core.DefaultParametersFactory.build('TestUseCase','Default','usecase',None)
    b = Borg()
    objt = (b.dbProxy.getUseCases(ucId))['TestUseCase']

    self.assertEqual(objt.name(),'TestUseCase')
    self.assertEqual(objt.tags(),[])
    self.assertEqual(objt.author(),'Unknown')
    self.assertEqual(objt.code(),'TBC')
    self.assertEqual(objt.actors(),['Unknown'])
    self.assertEqual(objt.description(),'To be defined')
    self.assertEqual(objt.author(),'Unknown')
    self.assertEqual(objt.environmentProperties()[0].preconditions(),'To be defined')
    self.assertEqual(str(objt.environmentProperties()[0].steps()[0]),'Undefined')
    self.assertEqual(objt.environmentProperties()[0].postconditions(),'To be defined')


  def tearDown(self):
    pass

if __name__ == '__main__':
  unittest.main()
