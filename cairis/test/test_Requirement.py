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
from cairis.core.EnvironmentParameters import EnvironmentParameters
from cairis.core.AssetParameters import AssetParameters
from cairis.core.AssetEnvironmentProperties import AssetEnvironmentProperties
import cairis.core.RequirementFactory
from cairis.core.ARM import DatabaseProxyException

__author__ = 'Shamal Faily'


class RequirementTest(unittest.TestCase):

  def setUp(self):
    call([os.environ['CAIRIS_CFG_DIR'] + "/initdb.sh"])
    cairis.core.BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/requirements.json')
    d = json.load(f)
    f.close()
    ienvs = d['environments']
    iep1 = EnvironmentParameters(ienvs[0]["theName"],ienvs[0]["theShortCode"],ienvs[0]["theDescription"])
    iep2 = EnvironmentParameters(ienvs[1]["theName"],ienvs[1]["theShortCode"],ienvs[1]["theDescription"])
    iep3 = EnvironmentParameters(ienvs[2]["theName"],ienvs[2]["theShortCode"],ienvs[2]["theDescription"])
    b = Borg()
    b.dbProxy.addEnvironment(iep1)
    b.dbProxy.addEnvironment(iep2)
    b.dbProxy.addEnvironment(iep3)
    self.iassets = d['assets']
    iaeps = [AssetEnvironmentProperties(self.iassets[0]["theEnvironmentProperties"][0][0],self.iassets[0]["theEnvironmentProperties"][0][1],self.iassets[0]["theEnvironmentProperties"][0][2])]
    iap = AssetParameters(self.iassets[0]["theName"],self.iassets[0]["theShortCode"],self.iassets[0]["theDescription"],self.iassets[0]["theSignificance"],self.iassets[0]["theType"],"0","N/A",[],[],iaeps)
    b.dbProxy.addAsset(iap)
    self.irequirements = d['requirements']

  def testRequirement(self):
    b = Borg()
    reqId = b.dbProxy.newId()
    
    ireq = cairis.core.RequirementFactory.build(reqId,self.irequirements[0]["theLabel"],self.irequirements[0]["theName"],self.irequirements[0]["theDescription"],self.irequirements[0]["thePriority"],self.irequirements[0]["theRationale"],self.irequirements[0]["theFitCriterion"],self.irequirements[0]["theOriginator"],self.irequirements[0]["theType"],self.irequirements[0]["theReference"],self.irequirements[0]["theReferenceType"],1)
    b.dbProxy.addRequirement(ireq,self.irequirements[0]["theReference"],True)


    oreqs = b.dbProxy.getRequirements()
    oreq = oreqs[ireq.name()]

    self.assertEqual(str(ireq.id()),str(oreq.id()))
    self.assertEqual(self.iassets[0]["theShortCode"] + "-" + str(ireq.label()),str(oreq.label()))
    self.assertEqual(str(ireq.name()),str(oreq.name()))
    self.assertEqual(str(ireq.description()),str(oreq.description()))
    self.assertEqual(str(ireq.rationale()),str(oreq.rationale()))
    self.assertEqual(str(ireq.fitCriterion()),str(oreq.fitCriterion()))
    self.assertEqual(str(ireq.version()),str(oreq.version()))
    self.assertEqual(str(ireq.originator()),str(oreq.originator()))
    self.assertEqual(str(ireq.type()),str(oreq.type()))
    self.assertEqual(str(ireq.domain()),str(oreq.domain()))
    self.assertEqual(str(ireq.domainType()),str(oreq.domainType()))

    self.assertEqual(len(b.dbProxy.getRequirementVersions(ireq.id())),1)

    soreq = b.dbProxy.getRequirement(oreq.label())
    self.assertEqual(str(oreq.name()),str(soreq.name()))
    self.assertEqual(str(oreq.description()),str(soreq.description()))
    self.assertEqual(str(oreq.rationale()),str(soreq.rationale()))
    self.assertEqual(str(oreq.fitCriterion()),str(soreq.fitCriterion()))
    self.assertEqual(str(oreq.version()),str(soreq.version()))
    self.assertEqual(str(oreq.originator()),str(soreq.originator()))
    self.assertEqual(str(oreq.type()),str(soreq.type()))
    self.assertEqual(str(oreq.domain()),str(soreq.domain()))
    self.assertEqual(str(oreq.domainType()),str(soreq.domainType()))


    uireq = oreq
    uireq.update('label',oreq.label())
    uireq.update('description','revised description')
    uireq.update('name','revised name')
    uireq.update('priority',oreq.priority())
    uireq.update('rationale',oreq.rationale())
    uireq.update('fitCriterion',oreq.fitCriterion())
    uireq.update('supportingMaterial','None')
    uireq.update('type',oreq.type())
    uireq.update('asset',oreq.domain())
    self.assertEqual(uireq.dirty(),9)
    uireq.incrementVersion()

    uireq.theLabel = int(uireq.theLabel.split('-')[1])
    b.dbProxy.updateRequirement(uireq)
    uoreqs = b.dbProxy.getRequirements()
    uoreq = uoreqs['revised name']

    self.assertEqual(str(uireq.name()),str(uoreq.name()))
    self.assertEqual(str(uireq.description()),str(uoreq.description()))
    self.assertEqual(str(uireq.rationale()),str(uoreq.rationale()))
    self.assertEqual(str(uireq.fitCriterion()),str(uoreq.fitCriterion()))
    self.assertEqual(str(oreq.version()),'2')
    self.assertEqual(str(uireq.originator()),str(uoreq.originator()))
    self.assertEqual(str(uireq.type()),str(uoreq.type()))
    self.assertEqual(str(uireq.domain()),str(uoreq.domain()))
    self.assertEqual(str(uireq.domainType()),str(uoreq.domainType()))

    b.dbProxy.deleteRequirement(ireq.id())

  def tearDown(self):
    pass

if __name__ == '__main__':
  unittest.main()
