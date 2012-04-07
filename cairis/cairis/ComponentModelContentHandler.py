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


from xml.sax.handler import ContentHandler,EntityResolver
from ComponentParameters import ComponentParameters
from ComponentAssociationParameters import ComponentAssociationParameters
from Borg import Borg

def it2Id(itLabel):
  if itLabel == 'required':
    return 1
  else:
    return 0

class ComponentModelContentHandler(ContentHandler,EntityResolver):
  def __init__(self):
    self.theComponents = []
    self.theAssociations = []
    self.resetComponentAttributes()
    self.resetComponentAssociationAttributes()
    b = Borg()
    self.configDir = b.configDir

  def resolveEntity(self,publicId,systemId):
    return self.configDir + '/component_model.dtd'

  def components(self):
    return self.theComponents

  def associations(self):
    return self.theAssociations

  def resetComponentAttributes(self):
    self.inDescription = 0
    self.theName = ''
    self.theDescription = ''
    self.theInterfaces = []

  def resetComponentAssociationAttributes(self):
    self.theFromName = ''
    self.theFromInterface = ''
    self.theToName = ''
    self.theToInterface = ''


  def startElement(self,name,attrs):
    if (name == 'component'):
      self.theName = attrs['name']
    elif (name == 'description'):
      self.inDescription = 1
    elif (name == 'interface'):
      self.theInterfaces.append((attrs['name'],it2Id(attrs['type'])))
    elif (name == 'component_association'):
      self.theFromName = attrs['from_component']
      self.theFromInterface = attrs['from_interface']
      self.theToName = attrs['to_component']
      self.theToInterface = attrs['to_interface']

  def characters(self,data):
    if self.inDescription:
      self.theDescription = data
      self.inDescription = 0

  def endElement(self,name):
    if (name == 'component'):
      p = ComponentParameters(self.theName,self.theDescription,self.theInterfaces)
      self.theComponents.append(p)
      self.resetComponentAttributes() 
    if name == 'component_association':
      p = ComponentAssociationParameters(self.theFromName,self.theFromInterface,self.theToName,self.theToInterface)
      self.theAssociations.append(p)
      self.resetComponentAssociationAttributes() 
