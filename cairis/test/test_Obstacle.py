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
from cairis.core.ObstacleParameters import ObstacleParameters
from cairis.core.ObstacleEnvironmentProperties import ObstacleEnvironmentProperties
from cairis.core.ARM import DatabaseProxyException

__author__ = 'Rachel Larcombe, Shamal Faily'

class ObstacleTest(unittest.TestCase):

  def setUp(self):
    call([os.environ['CAIRIS_CFG_DIR'] + "/initdb.sh"])
    cairis.core.BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/obstacles.json')
    d = json.load(f)
    f.close()
    ienvs = d['environments']
    iep1 = EnvironmentParameters(ienvs[0]["theName"],ienvs[0]["theShortCode"],ienvs[0]["theDescription"])
    b = Borg()
    b.dbProxy.addEnvironment(iep1)
    self.iObstacle = d['obstacles']

  def testObstacle(self):
    b = Borg()
    igep1 = ObstacleEnvironmentProperties(self.iObstacle[0]["theEnvironmentProperties"][0],self.iObstacle[0]["theEnvironmentProperties"][1],self.iObstacle[0]["theEnvironmentProperties"][2],self.iObstacle[0]["theEnvironmentProperties"][3])
   

    igp1 = ObstacleParameters(self.iObstacle[0]["theName"],self.iObstacle[0]["theOriginator"],[],[igep1])
   
    b.dbProxy.addObstacle(igp1)
  
    b.dbProxy.relabelObstacles(igep1.name())
    oObstacle = b.dbProxy.getObstacles()
    og1 = oObstacle[self.iObstacle[0]["theName"]]
    self.assertEqual(igp1.name(), og1.name())
    self.assertEqual(igp1.originator(), og1.originator())
    ogep1 = og1.environmentProperty(igep1.name())
    self.assertEqual(igep1.definition(), ogep1.definition())
    self.assertEqual(igep1.category(), ogep1.category())

    igp1.setId(og1.id())
    b.dbProxy.updateObstacle(igp1)


    b.dbProxy.deleteObstacle(og1.id())
 
  def tearDown(self):
    pass

if __name__ == '__main__':
  unittest.main()
