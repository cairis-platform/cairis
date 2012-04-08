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

def a2i(spLabel):
  if spLabel == 'Low':
    return 1
  elif spLabel == 'Medium':
    return 2
  elif spLabel == 'High':
    return 3
  else:
    return 0

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
    self.resetAssetAttributes()
    self.resetSecurityPropertyAttributes()
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

  def resetAssetAttributes(self):
    self.inDescription = 0
    self.inSignificance = 0
    self.theName = ''
    self.theShortCode = ''
    self.theAssetType = ''
    self.theDescription = ''
    self.theSignificance = ''
    self.theInterfaces = []
    self.theSecurityProperties = []

  def resetSecurityPropertyAttributes(self):
    self.thePropertyName = ''
    self.thePropertyValue = 'None'
    self.inRationale = 0
    self.theRationale = ''


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
    elif name == 'significance':
      self.inSignificance = 1
      self.theSignificance = ''
    elif name == 'interface':
      self.theInterfaces.append((attrs['name'],it2Id(attrs['type'])))
    elif name == 'asset':
      self.theName = attrs['name']
      self.theShortCode = attrs['short_code']
      self.theAssetType = attrs['type']
      self.theSecurityProperties = []
    elif name == 'security_property':
      self.thePropertyName = attrs['property']
      self.thePropertyValue = attrs['value']
    elif (name == 'component_association'):
      self.theFromName = attrs['from_component']
      self.theFromInterface = attrs['from_interface']
      self.theToName = attrs['to_component']
      self.theToInterface = attrs['to_interface']

  def characters(self,data):
    if self.inDescription:
      self.theDescription += data
    elif self.inSignificance:
      self.theSignificance += data
    elif self.inRationale:
      self.theRationale += data


  def endElement(self,name):
    if (name == 'component'):
      p = ComponentParameters(self.theName,self.theDescription,self.theInterfaces)
      self.theComponents.append(p)
      self.resetComponentAttributes() 
    elif name == 'asset':
      spDict = {}
      spDict['confidentiality'] = (0,'None')
      spDict['integrity'] = (0,'None')
      spDict['availability'] = (0,'None')
      spDict['accountability'] = (0,'None')
      spDict['anonymity'] = (0,'None')
      spDict['pseudonymity'] = (0,'None')
      spDict['unlinkability'] = (0,'None')
      spDict['unobservability'] = (0,'None')
      for sp in self.theSecurityProperties:
        spName = sp[0]
        spValue = a2i(sp[1])
        spRationale = sp[2]
        if spName in spDict:
          spDict[spName] = (spValue,spRationale)
      spValues = [] 
      spValues.append(spDict['confidentiality'])
      spValues.append(spDict['integrity'])
      spValues.append(spDict['availability'])
      spValues.append(spDict['accountability'])
      spValues.append(spDict['anonymity'])
      spValues.append(spDict['pseudonymity'])
      spValues.append(spDict['unlinkability'])
      spValues.append(spDict['unobservability'])
      p = TemplateAssetParameters(self.theName,self.theShortCode,self.theDescription,self.theSignificance,self.theAssetType,self.theInterfaces,spValues)
      self.theAssetParameters.append(p)
      self.resetAssetAttributes()
    elif name == 'security_property':
      self.theSecurityProperties.append((self.thePropertyName,self.thePropertyValue,self.theRationale))
      self.resetSecurityPropertyAttributes()
    if name == 'component_association':
      p = ComponentAssociationParameters(self.theFromName,self.theFromInterface,self.theToName,self.theToInterface)
      self.theAssociations.append(p)
      self.resetComponentAssociationAttributes() 
    elif name == 'description':
      self.inDescription = 0
    elif name == 'rationale':
      self.inRationale = 0
    elif name == 'significance':
      self.inSignificance = 0
