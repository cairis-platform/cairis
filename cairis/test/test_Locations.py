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
    call([os.environ['CAIRIS_SRC'] + "/test/initdb.sh"])
    cairis.core.BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/locations.json')
    d = json.load(f)
    f.close()
    self.iEnvironments = d['environments']
    iep1 = EnvironmentParameters(self.iEnvironments[0]["theName"],self.iEnvironments[0]["theShortCode"],self.iEnvironments[0]["theDescription"])
    b = Borg()
    b.dbProxy.addEnvironment(iep1)
    self.theEnvironments = b.dbProxy.getEnvironments()

    self.iRoles = d['roles']
    irp = RoleParameters(self.iRoles[0]["theName"], self.iRoles[0]["theType"], self.iRoles[0]["theShortCode"], self.iRoles[0]["theDescription"],[])
    b.dbProxy.addRole(irp)
    self.theRoles = b.dbProxy.getRoles()
    self.iPersonas = d['personas']
    ipp = PersonaParameters(self.iPersonas[0]["theName"],self.iPersonas[0]["theActivities"],self.iPersonas[0]["theAttitudes"],self.iPersonas[0]["theAptitudes"],self.iPersonas[0]["theMotivations"],self.iPersonas[0]["theSkills"],self.iPersonas[0]["theIntrinsic"],self.iPersonas[0]["theContextual"],"","0",self.iPersonas[0]["thePersonaType"],[],[PersonaEnvironmentProperties(self.iPersonas[0]["theEnvironmentProperties"][0]["theName"],(self.iPersonas[0]["theEnvironmentProperties"][0]["theDirectFlag"] == "True"),self.iPersonas[0]["theEnvironmentProperties"][0]["theNarrative"],self.iPersonas[0]["theEnvironmentProperties"][0]["theRole"])],[])
    b.dbProxy.addPersona(ipp) 
    thePersonas = b.dbProxy.getPersonas()
    self.thePersona = thePersonas[self.iPersonas[0]["theName"]]

    self.iassets = d['assets']
    iaeps = [AssetEnvironmentProperties(self.iassets[0]["theEnvironmentProperties"][0][0],self.iassets[0]["theEnvironmentProperties"][0][1],self.iassets[0]["theEnvironmentProperties"][0][2])]
    iap = AssetParameters(self.iassets[0]["theName"],self.iassets[0]["theShortCode"],self.iassets[0]["theDescription"],self.iassets[0]["theSignificance"],self.iassets[0]["theType"],"0","N/A",[],[],iaeps)
    b = Borg()
    b.dbProxy.addAsset(iap)

    oaps = b.dbProxy.getAssets()
    self.theAsset = oaps[self.iassets[0]["theName"]]
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
    b = Borg()
    b.dbProxy.deleteAsset(self.theAsset.id())
    b.dbProxy.deletePersona(self.thePersona.id())
    b.dbProxy.deleteRole(self.theRoles[self.iRoles[0]["theName"]].id())
    b.dbProxy.deleteEnvironment(self.theEnvironments[self.iEnvironments[0]["theName"]].id())
    b.dbProxy.close()
    call([os.environ['CAIRIS_SRC'] + "/test/dropdb.sh"])

if __name__ == '__main__':
  unittest.main()
