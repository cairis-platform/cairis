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
from EnvironmentParameters import EnvironmentParameters
from ValueTypeParameters import ValueTypeParameters
from Borg import Borg

class LocationsContentHandler(ContentHandler,EntityResolver):
  def __init__(self):
    b = Borg()
    self.configDir = b.configDir
    self.theLocationsName = ''
    self.theDiagram = ''
    self.theLocations = []
    self.theLinks = set([])

    self.resetLocationAttributes()

  def resolveEntity(self,publicId,systemId):
    return self.configDir + '/locations.dtd'

  def name(self): return self.theLocationsName
  def diagram(self): return self.theDiagram

  def locations(self):
    return self.theLocations

  def links(self):
    return self.theLinks

  def resetLocationAttributes(self):
    self.theName = ''
    self.theAssetInstances = []
    self.thePersonaInstances = []

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
      if ((self.theName,toName) not in self.theLinks) and ((toName,self.theName) not in self.theLinks):
        self.theLinks.add((self.theName,toName))

  def endElement(self,name):
    if name == 'location':
      self.theLocations.append((self.theName,self.theAssetInstances,self.thePersonaInstances))
      self.theAssetInstances = []
      self.thePersonaInstances = []
