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


class ModelTests(unittest.TestCase):

  def setUp(self):
    cairis.core.BorgFactory.initialise()
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/NeuroGrid/NeuroGrid.xml',1,'test')

  def testModelCreation(self):
    b = Borg()  
    b.get_dbproxy().classModel('Psychosis')
    b.get_dbproxy().classModel('Psychosis','',True)
    b.get_dbproxy().classModel('Psychosis','Clinical data',True)
    b.get_dbproxy().goalModel('Psychosis')
    b.get_dbproxy().goalModel('Psychosis','Process clinical data on NeuroGrid')
    b.get_dbproxy().responsibilityModel('Psychosis')
    b.get_dbproxy().responsibilityModel('Psychosis','Data Consumer')
    b.get_dbproxy().obstacleModel('Psychosis')
    b.get_dbproxy().obstacleModel('Psychosis','Unauthorised portal access')
    b.get_dbproxy().taskModel('Psychosis')
    b.get_dbproxy().taskModel('Psychosis','Upload data')
    b.get_dbproxy().riskAnalysisModel('Psychosis')
    b.get_dbproxy().riskAnalysisModel('Psychosis','risk','Unauthorised Certificate Access')
    b.get_dbproxy().riskObstacleModel('Unauthorised Certificate Access','Psychosis')
    b.get_dbproxy().assumptionPersonaModel('Claire')
    b.get_dbproxy().textualArgumentationModel('Claire','Activities')
    
    
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/ACME_Water/ACME_Water.xml',1,'test')
    importLocationsFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/ACME_Water/PooleWWTW.xml','test')
    b.get_dbproxy().locationsRiskModel('PooleWWTW','Day')


