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
from cairis.core.InternalDocumentParameters import InternalDocumentParameters
from cairis.core.CodeParameters import CodeParameters
from cairis.core.MemoParameters import MemoParameters
import sys

class QuotationTest(unittest.TestCase):

  def setUp(self):
    call([os.environ['CAIRIS_CFG_DIR'] + "/initdb.sh"])
    cairis.core.BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/processes.json')
    d = json.load(f)
    f.close()

    ienvs = d['environments']
    self.iep1 = EnvironmentParameters(ienvs[0]["theName"],ienvs[0]["theShortCode"],ienvs[0]["theDescription"])
    b = Borg()
    b.dbProxy.addEnvironment(self.iep1)

    iIntDocs = d['internaldocuments']
    i = InternalDocumentParameters(iIntDocs[0]["theName"],iIntDocs[0]["theDescription"], iIntDocs[0]["theContent"], [],[])
    b.dbProxy.addInternalDocument(i)

    iCodes = d['codes']
    i = CodeParameters(iCodes[0]["theName"], iCodes[0]["theType"],iCodes[0]["theDescription"], iCodes[0]["theInclusionCriteria"], iCodes[0]["theExample"])
    b.dbProxy.addCode(i)

    iMemos = d['memos']
    i = MemoParameters(iMemos[0]["theName"], iMemos[0]["theDescription"])
    b.dbProxy.addMemo(i)

    self.iQs = d['quotations']
    

  def testAddUpdateQuotation(self):
    i1 = (self.iQs[0]["theType"],self.iQs[0]["theCode"],self.iQs[0]["theArtifactType"],self.iQs[0]["theArtifactName"],self.iQs[0]["theEnvironment"],self.iQs[0]["theSection"],self.iQs[0]["theStartIdx"],self.iQs[0]["theEndIdx"],self.iQs[0]["theLabel"],self.iQs[0]["theSynopsis"])
    i2 = (self.iQs[1]['theType'],self.iQs[1]["theCode"],self.iQs[1]["theArtifactType"],self.iQs[1]["theArtifactName"],self.iQs[1]["theEnvironment"],self.iQs[1]["theSection"],self.iQs[1]["theStartIdx"],self.iQs[1]["theEndIdx"],self.iQs[1]["theLabel"],self.iQs[1]["theSynopsis"])
    b = Borg()
    b.dbProxy.addQuotation(i1)
    b.dbProxy.addQuotation(i2)
    oqs = b.dbProxy.getQuotations()
    o1 = oqs[0]
    self.assertEqual(self.iQs[0]["theCode"],o1[0])
    self.assertEqual(self.iQs[0]["theArtifactType"],o1[1])
    self.assertEqual(self.iQs[0]["theArtifactName"],o1[2])
    self.assertEqual(self.iQs[0]["theSection"],o1[3])
    self.assertEqual(self.iQs[0]["theStartIdx"],o1[4])
    self.assertEqual(self.iQs[0]["theEndIdx"],o1[5])
    self.assertEqual('Lorem ip',o1[6])
    self.assertEqual(self.iQs[0]["theSynopsis"],o1[7])
    self.assertEqual(self.iQs[0]["theLabel"],o1[8])

    b.dbProxy.updateQuotation(self.iQs[0]["theCode"],self.iQs[0]["theArtifactType"],self.iQs[0]["theArtifactName"],self.iQs[0]["theStartIdx"],self.iQs[0]["theEndIdx"],2,self.iQs[0]["theEndIdx"],self.iQs[0]["theSynopsis"],self.iQs[0]["theLabel"])

    oqs = b.dbProxy.getQuotations()
    ou1 = oqs[0]
    self.assertEqual(self.iQs[0]["theCode"],ou1[0])
    self.assertEqual(self.iQs[0]["theArtifactType"],ou1[1])
    self.assertEqual(self.iQs[0]["theArtifactName"],ou1[2])
    self.assertEqual(self.iQs[0]["theSection"],ou1[3])
    self.assertEqual(2,ou1[4])
    self.assertEqual(self.iQs[0]["theEndIdx"],ou1[5])
    self.assertEqual('orem ip',ou1[6])
    self.assertEqual(self.iQs[0]["theSynopsis"],ou1[7])
    self.assertEqual(self.iQs[0]["theLabel"],ou1[8])

    b.dbProxy.deleteQuotation(self.iQs[0]["theCode"],self.iQs[0]["theArtifactType"],self.iQs[0]["theArtifactName"],1,self.iQs[0]["theEndIdx"])
    b.dbProxy.deleteQuotation(self.iQs[1]["theCode"],self.iQs[1]["theArtifactType"],self.iQs[1]["theArtifactName"],self.iQs[1]["theStartIdx"],self.iQs[1]["theEndIdx"])
  
  def tearDown(self):
    b = Borg()
    b.dbProxy.close()
    call([os.environ['CAIRIS_CFG_DIR'] + "/dropdb.sh"])

if __name__ == '__main__':
  unittest.main()
