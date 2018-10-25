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

import os
from xml.sax.handler import ContentHandler,EntityResolver
from cairis.core.EnvironmentParameters import EnvironmentParameters
from cairis.core.ValueTypeParameters import ValueTypeParameters
from cairis.core.Location import Location
from cairis.core.LocationsParameters import LocationsParameters
from cairis.core.Borg import Borg

__author__ = 'Shamal Faily'

class LocationsContentHandler(ContentHandler,EntityResolver):
  def __init__(self):
    b = Borg()
    self.configDir = b.configDir
    self.allLocations = []

    self.resetLocationsAttributes()
    self.resetLocationAttributes()

  def resolveEntity(self,publicId,systemId):
    return systemId

  def name(self): return self.theLocationsName
  def diagram(self): return self.theDiagram

  def locations(self):
    return self.allLocations

  def links(self):
    return self.theLinks

  def resetLocationAttributes(self):
    self.theName = ''
    self.theAssetInstances = []
    self.thePersonaInstances = []
    self.theLinks = []

  def resetLocationsAttributes(self):
    self.theLocationsName = ''
    self.theDiagram = ''
    self.theLocations = []


  def startElement(self,name,attrs):
    self.currentElementName = name
    if name == 'locations':
      self.theLocationsName = attrs['name']
      self.theDiagram = attrs['diagram']
    elif name == 'location':
      self.theName = attrs['name']
    elif name == 'asset_instance':
      self.theAssetInstances.append((attrs['name'],attrs['asset']))
    elif name == 'persona_instance':
      self.thePersonaInstances.append((attrs['name'],attrs['persona']))
    elif name == 'link':
      toName = attrs['name']
      self.theLinks.append(toName)

  def endElement(self,name):
    if name == 'location':
      self.theLocations.append(Location(-1,self.theName,self.theAssetInstances,self.thePersonaInstances,self.theLinks))
      self.resetLocationAttributes()
    elif name == 'locations':
      self.allLocations.append(LocationsParameters(self.theLocationsName,self.theDiagram,self.theLocations))
      self.resetLocationsAttributes()
