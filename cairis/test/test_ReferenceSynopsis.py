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
from cairis.core.ReferenceSynopsis import ReferenceSynopsis
from cairis.core.ARM import DatabaseProxyException
from cairis.mio.ModelImport import importModelFile

__author__ = 'Shamal Faily'


class ReferenceSynopsisTest(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    cairis.core.BorgFactory.initialise()
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/NeuroGrid/NeuroGrid.xml',1)

  def setUp(self):
    f = open(os.environ['CAIRIS_SRC'] + '/test/reference_synopses.json')
    d = json.load(f)
    f.close()
    self.rsData = d['reference_synopses'][0]

  def tearDown(self):
    pass

  def testAddSynopsis(self):
    irs = ReferenceSynopsis(-1,self.rsData['theReference'],self.rsData['theSynopsis'],self.rsData['theDimension'],self.rsData['theActorType'],self.rsData['theActor'],self.rsData['theInitialSatisfaction'])
    b = Borg()
    b.dbProxy.addReferenceSynopsis(irs)

    ors = b.dbProxy.getReferenceSynopsis(self.rsData['theReference'])
    self.assertEqual(irs.reference(), ors.reference())
    self.assertEqual(irs.synopsis(), ors.synopsis())
    self.assertEqual(irs.dimension(), ors.dimension())
    self.assertEqual(irs.actorType(), ors.actorType())
    self.assertEqual(irs.actor(), ors.actor())
    self.assertEqual(irs.satisfaction(), ors.satisfaction())

  def testUpdateSynopsis(self):
    b = Borg()
    ors = b.dbProxy.getReferenceSynopsis(self.rsData['theReference'])
    ors.theSynopsis = 'Updated synopsis'
    b.dbProxy.updateReferenceSynopsis(ors)
    urs = b.dbProxy.getReferenceSynopsis(self.rsData['theReference'])
    self.assertEqual(ors.reference(), urs.reference())
    self.assertEqual(ors.synopsis(), urs.synopsis())
    self.assertEqual(ors.dimension(), urs.dimension())
    self.assertEqual(ors.actorType(), urs.actorType())
    self.assertEqual(ors.actor(), urs.actor())
    self.assertEqual(ors.satisfaction(), urs.satisfaction())


if __name__ == '__main__':
  unittest.main()
