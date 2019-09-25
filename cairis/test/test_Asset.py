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
from cairis.core.ARM import DatabaseProxyException,AttributeTooBig

__author__ = 'Shamal Faily'


class AssetTest(unittest.TestCase):

  def setUp(self):
    call([os.environ['CAIRIS_CFG_DIR'] + "/initdb.sh"])
    cairis.core.BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/assets.json')
    d = json.load(f)
    f.close()
    ienvs = d['environments']
    self.iep1 = EnvironmentParameters(ienvs[0]["theName"],ienvs[0]["theShortCode"],ienvs[0]["theDescription"])
    self.iep2 = EnvironmentParameters(ienvs[1]["theName"],ienvs[1]["theShortCode"],ienvs[1]["theDescription"])
    self.iep3 = EnvironmentParameters(ienvs[2]["theName"],ienvs[2]["theShortCode"],ienvs[2]["theDescription"])
    b = Borg()
    b.dbProxy.addEnvironment(self.iep1)
    b.dbProxy.addEnvironment(self.iep2)
    b.dbProxy.addEnvironment(self.iep3)
    self.oenvs = b.dbProxy.getEnvironments()
    self.iassets = d['assets']

  def testAsset(self):
    iaeps = [AssetEnvironmentProperties(self.iassets[0]["theEnvironmentProperties"][0][0],self.iassets[0]["theEnvironmentProperties"][0][1],self.iassets[0]["theEnvironmentProperties"][0][2])]
    iap = AssetParameters(self.iassets[0]["theName"],self.iassets[0]["theShortCode"],self.iassets[0]["theDescription"],self.iassets[0]["theSignificance"],self.iassets[0]["theType"],"0","N/A",[],[],iaeps)
    b = Borg()

    iap.theShortCode = 'TESTCODE123456789012345678901234567890'
    with self.assertRaises(AttributeTooBig):
      b.dbProxy.addAsset(iap)
    iap.theShortCode = 'TESTCODE'
    b.dbProxy.addAsset(iap)

    oaps = b.dbProxy.getAssets()
    oap = oaps[self.iassets[0]["theName"]]

    self.assertEqual(iap.name(), oap.name())
    self.assertEqual(iap.shortCode(),oap.shortCode())
    self.assertEqual(iap.description(),oap.description())
    self.assertEqual(iap.significance(),oap.significance())
    oaeps = oap.environmentProperties()
    self.assertEqual(iaeps[0].name(), oaeps[0].name())
    self.assertEqual(str(iaeps[0].properties()[0]), str(oaeps[0].properties()[0]))
    self.assertEqual(str(iaeps[0].properties()[1]), str(oaeps[0].properties()[1]))
    self.assertEqual(str(iaeps[0].properties()[2]), str(oaeps[0].properties()[2]))
    self.assertEqual(str(iaeps[0].properties()[3]), str(oaeps[0].properties()[3]))
    self.assertEqual(str(iaeps[0].properties()[4]), str(oaeps[0].properties()[4]))
    self.assertEqual(str(iaeps[0].properties()[5]), str(oaeps[0].properties()[5]))
    self.assertEqual(str(iaeps[0].properties()[6]), str(oaeps[0].properties()[6]))
    self.assertEqual(str(iaeps[0].properties()[7]), str(oaeps[0].properties()[7]))
    self.assertEqual(iaeps[0].rationale()[0], oaeps[0].rationale()[0])
    self.assertEqual(iaeps[0].rationale()[1], oaeps[0].rationale()[1])
    self.assertEqual(iaeps[0].rationale()[2], oaeps[0].rationale()[2])
    self.assertEqual(iaeps[0].rationale()[3], oaeps[0].rationale()[3])
    self.assertEqual(iaeps[0].rationale()[4], oaeps[0].rationale()[4])
    self.assertEqual(iaeps[0].rationale()[5], oaeps[0].rationale()[5])
    self.assertEqual(iaeps[0].rationale()[6], oaeps[0].rationale()[6])
    self.assertEqual(iaeps[0].rationale()[7], oaeps[0].rationale()[7])

    envName = self.iassets[0]["theEnvironmentProperties"][0][0]
    self.assertEqual(str(iaeps[0].properties()[0]), str(oap.securityProperties(envName,'',envName)[0]))
    self.assertEqual(str(iaeps[0].properties()[1]), str(oap.securityProperties(envName,'',envName)[1]))
    self.assertEqual(str(iaeps[0].properties()[2]), str(oap.securityProperties(envName,'',envName)[2]))
    self.assertEqual(str(iaeps[0].properties()[3]), str(oap.securityProperties(envName,'',envName)[3]))
    self.assertEqual(str(iaeps[0].properties()[4]), str(oap.securityProperties(envName,'',envName)[4]))
    self.assertEqual(str(iaeps[0].properties()[5]), str(oap.securityProperties(envName,'',envName)[5]))
    self.assertEqual(str(iaeps[0].properties()[6]), str(oap.securityProperties(envName,'',envName)[6]))
    self.assertEqual(str(iaeps[0].properties()[7]), str(oap.securityProperties(envName,'',envName)[7]))
    self.assertEqual([['Confidentiality','High','Researchers very worried about the disclosure of partially anonymised patient data.'],['Availability','Medium','Availability of NeuroGrid is quite important, but prepared to sacrifice this if doing so safeguards clinical data.']],oap.propertyList('Psychosis','',''))
    self.assertEqual([['Confidentiality','High','None'],['Availability','Medium','None']],oap.propertyList('','Maximise',''))
    self.assertEqual([['Confidentiality','High','None'],['Availability','Medium','None']],oap.propertyList('','Override','Psychosis'))
    oap.theShortCode = 'TESTCODE'
    oap.theAssetPropertyDictionary['Psychosis'].theSecurityProperties[0] = 1;

    b.dbProxy.updateAsset(oap)

    oaps2 = b.dbProxy.getAssets(oap.id())
    oap2 = oaps[self.iassets[0]["theName"]]
    self.assertEqual(oap2.shortCode(),'TESTCODE')

    oaps = b.dbProxy.deleteAsset(oap.id())


  def tearDown(self):
    pass

if __name__ == '__main__':
  unittest.main()
