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
from cairis.core.ReferenceContribution import ReferenceContribution
from cairis.core.ARM import DatabaseProxyException
from cairis.mio.ModelImport import importModelFile

__author__ = 'Shamal Faily'


class UseCaseContributionTest(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    cairis.core.BorgFactory.initialise()
    importModelFile(os.environ['CAIRIS_SRC'] + '/test/webinos.xml',1)

  def setUp(self):
    f = open(os.environ['CAIRIS_SRC'] + '/test/usecase_contributions.json')
    d = json.load(f)
    f.close()
    self.csData = d['characteristic_synopses'][0]
    self.rcData = d['usecase_contributions'][0]


  def tearDown(self):
    pass

  def testAddContribution(self):
    ics = ReferenceSynopsis(-1,self.csData['theReference'],self.csData['theSynopsis'],self.csData['theDimension'],self.csData['theActorType'],self.csData['theActor'])
    b = Borg()
    b.dbProxy.addCharacteristicSynopsis(ics)

    irc = ReferenceContribution(self.rcData['theSource'],self.rcData['theDestination'],self.rcData['theMeansEnd'],self.rcData['theContribution'])
    b.dbProxy.addUseCaseContribution(irc)

    orcs = b.dbProxy.getUseCaseContributions(self.rcData['theSource'])
    orc,rType = orcs[self.rcData['theDestination']]
    self.assertEqual(orc.source(), irc.source())
    self.assertEqual(orc.destination(), irc.destination())
    self.assertEqual(orc.meansEnd(), irc.meansEnd())
    self.assertEqual(orc.contribution(), irc.contribution())

  def testUpdateContribution(self):
    b = Borg()
    orcs = b.dbProxy.getUseCaseContributions(self.rcData['theSource'])
    orc,rType = orcs[self.rcData['theDestination']]
    orc.theContribution = 'Break'
    b.dbProxy.updateUseCaseContribution(orc)

    urcs = b.dbProxy.getUseCaseContributions(self.rcData['theSource'])
    urc,rType = urcs[self.rcData['theDestination']]
    self.assertEqual(orc.source(), urc.source())
    self.assertEqual(orc.destination(), urc.destination())
    self.assertEqual(orc.meansEnd(), urc.meansEnd())
    self.assertEqual(orc.contribution(), urc.contribution())

if __name__ == '__main__':
  unittest.main()
