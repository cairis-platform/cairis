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
from cairis.core.RoleParameters import RoleParameters
from cairis.core.EnvironmentParameters import EnvironmentParameters
from cairis.core.AssetParameters import AssetParameters
from cairis.core.AssetEnvironmentProperties import AssetEnvironmentProperties
from cairis.core.Step import Step
from cairis.core.Steps import Steps
from cairis.core.UseCaseEnvironmentProperties import UseCaseEnvironmentProperties
from cairis.core.UseCaseParameters import UseCaseParameters
from cairis.core.ObstacleEnvironmentProperties import ObstacleEnvironmentProperties
from cairis.core.ObstacleParameters import ObstacleParameters
from cairis.core.UseCaseParameters import UseCaseParameters
from cairis.core.DataFlowParameters import DataFlowParameters
from cairis.mio.ModelImport import importDataflowsFile

__author__ = 'Shamal Faily'


class DataFlowTest(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    call([os.environ['CAIRIS_CFG_DIR'] + "/initdb.sh"])
    cairis.core.BorgFactory.initialise()

    f = open(os.environ['CAIRIS_SRC'] + '/test/dataflow.json')
    d = json.load(f)
    f.close()
    iEnvironments = d['environments']
    iep1 = EnvironmentParameters(iEnvironments[0]["theName"],iEnvironments[0]["theShortCode"],iEnvironments[0]["theDescription"])
    b = Borg()
    b.dbProxy.addEnvironment(iep1)

    iRoles = d['roles']
    irp = RoleParameters(iRoles[0]["theName"], iRoles[0]["theType"], iRoles[0]["theShortCode"], iRoles[0]["theDescription"],[])
    b.dbProxy.addRole(irp)

    iUseCases = d['use_cases']
    ucName = iUseCases[0]["theName"]
    ucAuthor = iUseCases[0]["theAuthor"]
    ucCode = iUseCases[0]["theCode"]
    ucDesc = iUseCases[0]["theDescription"]
    ucActor = iUseCases[0]["theActor"]
    ucEnv = iUseCases[0]["theEnvironments"][0]
    ucEnvName = ucEnv["theName"]
    ucPre = ucEnv["thePreconditions"]
    ucPost = ucEnv["thePostconditions"]
    ss = Steps()
    for ucStep in ucEnv["theFlow"]:
      ss.append(Step(ucStep["theDescription"]))  
    ucep = UseCaseEnvironmentProperties(ucEnvName,ucPre,ss,ucPost)
    iuc = UseCaseParameters(ucName,ucAuthor,ucCode,[ucActor],ucDesc,[],[ucep])
    b = Borg()
    b.dbProxy.addUseCase(iuc) 

    for iAsset in d['assets']:
      iaeps = [AssetEnvironmentProperties(iAsset["theEnvironmentProperties"][0][0],iAsset["theEnvironmentProperties"][0][1],iAsset["theEnvironmentProperties"][0][2])]
      iap = AssetParameters(iAsset["theName"],iAsset["theShortCode"],iAsset["theDescription"],iAsset["theSignificance"],iAsset["theType"],"0","N/A",[],[],iaeps)
      b.dbProxy.addAsset(iap)

    for iObstacle in d['obstacles']:
      ioep = ObstacleEnvironmentProperties(iObstacle["theEnvironmentProperties"][0],iObstacle["theEnvironmentProperties"][1],iObstacle["theEnvironmentProperties"][2],iObstacle["theEnvironmentProperties"][3])
      iop = ObstacleParameters(iObstacle["theName"],iObstacle["theOriginator"],[],[ioep])
      b.dbProxy.addObstacle(iop)


  def setUp(self):
    f = open(os.environ['CAIRIS_SRC'] + '/test/dataflow.json')
    d = json.load(f)
    f.close()
    self.dfJson = d['dataflows'][0]

  def testAddDataFlow(self):
    dfObs = []
    for dfo in self.dfJson['theObstacles']:
      dfObs.append((dfo['theName'],dfo['theKeyword'],dfo['theContext']))
    idfp = DataFlowParameters(self.dfJson['theName'],self.dfJson['theType'],self.dfJson['theEnvironmentName'],self.dfJson['theFromName'],self.dfJson['theFromType'],self.dfJson['theToName'],self.dfJson['theToType'],self.dfJson['theAssets'],dfObs,self.dfJson['theTags'])
    b = Borg()
    b.dbProxy.addDataFlow(idfp)
    odfs = b.dbProxy.getDataFlows()
    odf = odfs[0]
    self.assertEqual(idfp.name(),odf.name())
    self.assertEqual(idfp.type(),odf.type())
    self.assertEqual(idfp.environment(),odf.environment())
    self.assertEqual(idfp.fromName(),odf.fromName())
    self.assertEqual(idfp.fromType(),odf.fromType())
    self.assertEqual(idfp.toName(),odf.toName())
    self.assertEqual(idfp.toType(),odf.toType())
    self.assertEqual(idfp.assets(),odf.assets())
    self.assertEqual(idfp.obstacles(),odf.obstacles())
    self.assertEqual(idfp.tags(),odf.tags())

  def testUpdateDataFlow(self):
    dfObs = []
    for dfo in self.dfJson['theObstacles']:
      dfObs.append((dfo['theName'],dfo['theKeyword'],dfo['theContext']))
    idfp = DataFlowParameters(self.dfJson['theName'],self.dfJson['theType'],self.dfJson['theEnvironmentName'],self.dfJson['theFromName'],self.dfJson['theFromType'],self.dfJson['theToName'],self.dfJson['theToType'],self.dfJson['theAssets'],dfObs,self.dfJson['theTags'])
    b = Borg()
    b.dbProxy.addDataFlow(idfp)
    idfp.theName = 'Authenticate'
    b.dbProxy.updateDataFlow('authenticate','Authorised Researcher','entity','Authenticate Researcher','process','Psychosis',idfp)
    odfs = b.dbProxy.getDataFlows()
    odf = odfs[0]
    self.assertEqual(idfp.name(),odf.name())
    self.assertEqual(idfp.type(),odf.type())
    self.assertEqual(idfp.environment(),odf.environment())
    self.assertEqual(idfp.fromName(),odf.fromName())
    self.assertEqual(idfp.fromType(),odf.fromType())
    self.assertEqual(idfp.toName(),odf.toName())
    self.assertEqual(idfp.toType(),odf.toType())
    self.assertEqual(idfp.assets(),odf.assets())
    self.assertEqual(idfp.obstacles(),odf.obstacles())
    self.assertEqual(idfp.tags(),odf.tags())

  def testImportDataflows(self):
    self.assertEqual(importDataflowsFile(os.environ['CAIRIS_SRC'] + '/test/testdataflow.xml'),'Imported 1 dataflow. Imported 0 trust boundaries.')

  def testImportDataflowsWithoutTypee(self):
    self.assertEqual(importDataflowsFile(os.environ['CAIRIS_SRC'] + '/test/testdataflow_withouttype.xml'),'Imported 1 dataflow. Imported 0 trust boundaries.')
    b = Borg()
    odfs = b.dbProxy.getDataFlows()
    odf = odfs[0]
    self.assertEqual(odf.type(),'Information')

  def testExportDataflows(self):
    importDataflowsFile(os.environ['CAIRIS_SRC'] + '/test/testdataflow.xml')
    b = Borg()
    self.assertEqual(b.dbProxy.dataflowsToXml()[1],1)

  def testDataFlowDiagram(self):
    importDataflowsFile(os.environ['CAIRIS_SRC'] + '/test/testdataflow.xml')
    b = Borg()
    dfs = b.dbProxy.dataFlowDiagram('Psychosis','None','')
    self.assertEqual(len(dfs),1)

  def tearDown(self):
    b = Borg()
    b.dbProxy.deleteDataFlow(self.dfJson['theName'],self.dfJson['theFromName'],self.dfJson['theFromType'],self.dfJson['theToName'],self.dfJson['theToType'],self.dfJson['theEnvironmentName'])
    odfs = b.dbProxy.getDataFlows()
    self.assertEqual(len(odfs),0)

if __name__ == '__main__':
  unittest.main()
