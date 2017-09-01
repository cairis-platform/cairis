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
from cairis.core.PersonaParameters import PersonaParameters
from cairis.core.PersonaEnvironmentProperties import PersonaEnvironmentProperties
from cairis.core.AssetParameters import AssetParameters
from cairis.core.AssetEnvironmentProperties import AssetEnvironmentProperties
from cairis.core.Location import Location
from cairis.core.LocationsParameters import LocationsParameters

__author__ = 'Shamal Faily'

class LocationsTest(unittest.TestCase):

  def setUp(self):
    call([os.environ['CAIRIS_CFG_DIR'] + "/initdb.sh"])
    cairis.core.BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/locations.json')
    d = json.load(f)
    f.close()
    iEnvironments = d['environments']
    iep1 = EnvironmentParameters(iEnvironments[0]["theName"],iEnvironments[0]["theShortCode"],iEnvironments[0]["theDescription"])
    b = Borg()
    b.dbProxy.addEnvironment(iep1)

    iRoles = d['roles']
    irp = RoleParameters(iRoles[0]["theName"], iRoles[0]["theType"], iRoles[0]["theShortCode"], iRoles[0]["theDescription"],[])
    b.dbProxy.addRole(irp)
    iPersonas = d['personas']
    ipp = PersonaParameters(iPersonas[0]["theName"],iPersonas[0]["theActivities"],iPersonas[0]["theAttitudes"],iPersonas[0]["theAptitudes"],iPersonas[0]["theMotivations"],iPersonas[0]["theSkills"],iPersonas[0]["theIntrinsic"],iPersonas[0]["theContextual"],"","0",iPersonas[0]["thePersonaType"],[],[PersonaEnvironmentProperties(iPersonas[0]["theEnvironmentProperties"][0]["theName"],(iPersonas[0]["theEnvironmentProperties"][0]["theDirectFlag"] == "True"),iPersonas[0]["theEnvironmentProperties"][0]["theNarrative"],iPersonas[0]["theEnvironmentProperties"][0]["theRole"])],[])
    b.dbProxy.addPersona(ipp) 
    iassets = d['assets']
    iaeps = [AssetEnvironmentProperties(iassets[0]["theEnvironmentProperties"][0][0],iassets[0]["theEnvironmentProperties"][0][1],iassets[0]["theEnvironmentProperties"][0][2])]
    iap = AssetParameters(iassets[0]["theName"],iassets[0]["theShortCode"],iassets[0]["theDescription"],iassets[0]["theSignificance"],iassets[0]["theType"],"0","N/A",[],[],iaeps)
    b = Borg()
    b.dbProxy.addAsset(iap)
    self.ilocations = d['locations']

  def testLocations(self):
    iLocsName = self.ilocations[0]['theName']
    iLocsDia = self.ilocations[0]['theDiagram']
    
    iLocations = []

    iLoc1 = self.ilocations[0]['theLocations'][0] 
    iLoc1Name = iLoc1['theName']
    iLoc1AssetInstances = []
    iLoc1PersonaInstances = []
    iLoc1Links = iLoc1['theLinks']
    iLocations.append(Location(-1,iLoc1Name,iLoc1AssetInstances,iLoc1PersonaInstances,iLoc1Links))

    iLoc2 = self.ilocations[0]['theLocations'][1] 
    iLoc2Name = iLoc2['theName']
    iLoc2AssetInstances = [(iLoc2['theAssetInstances'][0]['theName'],iLoc2['theAssetInstances'][0]['theAsset'])]
    iLoc2PersonaInstances = [(iLoc2['thePersonaInstances'][0]['theName'],iLoc2['thePersonaInstances'][0]['thePersona'])]
    iLoc2Links = iLoc2['theLinks']
    iLocations.append(Location(-1,iLoc2Name,iLoc2AssetInstances,iLoc2PersonaInstances,iLoc2Links))

    ilp = LocationsParameters(iLocsName,iLocsDia,iLocations)

    b = Borg()
    b.dbProxy.addLocations(ilp)

    oLocsDict = b.dbProxy.getLocations()
    oLocs = oLocsDict[ilp.name()]
    oLocsId = oLocs.id()
    oLocsDia = oLocs.diagram()
    oLocsLocations = oLocs.locations()

    self.assertEqual(iLocsDia,oLocsDia)

    oLocs1 = oLocsLocations[0]
    self.assertEqual(iLoc1Name,oLocs1.name())
    self.assertEqual(iLoc1AssetInstances,oLocs1.assetInstances())
    self.assertEqual(iLoc1PersonaInstances,oLocs1.personaInstances())

    oLocs2 = oLocsLocations[1]
    self.assertEqual(iLoc2Name,oLocs2.name())
    self.assertEqual(iLoc2AssetInstances,oLocs2.assetInstances())
    self.assertEqual(iLoc2PersonaInstances,oLocs2.personaInstances())

    ilp.setId(oLocsId)
    b.dbProxy.updateLocations(ilp)
    uLocsDict = b.dbProxy.getLocations()
    uLocs = uLocsDict[ilp.name()]
    uLocsId = uLocs.id()
    uLocsDia = uLocs.diagram()
    uLocsLocations = uLocs.locations()
    self.assertEqual(uLocsDia,oLocsDia)

    uLocs1 = uLocsLocations[0]
    self.assertEqual(uLocs1.name(),oLocs1.name())
    self.assertEqual(uLocs1.assetInstances(),oLocs1.assetInstances())
    self.assertEqual(uLocs1.personaInstances(),oLocs1.personaInstances())

    b.dbProxy.deleteLocations(uLocsId)

  def tearDown(self):
    pass

if __name__ == '__main__':
  unittest.main()
