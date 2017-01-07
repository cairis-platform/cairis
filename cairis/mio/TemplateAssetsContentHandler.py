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
from cairis.core.ValueTypeParameters import ValueTypeParameters
from cairis.core.TemplateAssetParameters import TemplateAssetParameters
from cairis.core.Borg import Borg

__author__ = 'Shamal Faily'

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

class TemplateAssetsContentHandler(ContentHandler,EntityResolver):
  def __init__(self):
    self.theValueTypes = []
    self.theAssets = []
    self.resetAssetAttributes()
    self.resetSecurityPropertyAttributes()
    b = Borg()
    self.configDir = b.configDir

  def assets(self):
    return self.theAssets

  def valueTypes(self):
    return self.theValueTypes

  def resolveEntity(self,publicId,systemId):
    return systemId

  def resetValueTypeAttributes(self):
    self.inDescription = 0
    self.inRationale = 0
    self.theName = ''
    self.theDescription = ''
    self.theRationale = ''
    self.theScore = 0

  def resetAssetAttributes(self):
    self.inDescription = 0
    self.inSignificance = 0
    self.theName = ''
    self.theShortCode = ''
    self.theAssetType = ''
    self.theSurfaceType = ''
    self.theAccessRight = ''
    self.theDescription = ''
    self.theSignificance = ''
    self.theTags = []
    self.theInterfaces = []
    self.theSecurityProperties = []

  def resetSecurityPropertyAttributes(self):
    self.thePropertyName = ''
    self.thePropertyValue = 'None'
    self.inRationale = 0
    self.theRationale = ''

  def startElement(self,name,attrs):
    if (name == 'description'):
      self.inDescription = 1
      self.theDescription = ''
    elif (name == 'fit_criterion'):
      self.inFitCriterion = 1
      self.theFitCriterion = ''
    elif name == 'significance':
      self.inSignificance = 1
      self.theSignificance = ''
    elif name == 'rationale':
      self.inRationale = 1
      self.theRationale = ''
    elif name == 'interface':
      self.theInterfaces.append((attrs['name'],it2Id(attrs['type']),attrs['access_right'],attrs['privilege']))
    elif name == 'asset':
      self.theName = attrs['name']
      self.theShortCode = attrs['short_code']
      self.theAssetType = attrs['type']
      self.theSurfaceType = attrs['surface_type']
      self.theAccessRight = attrs['access_right']
      self.theSecurityProperties = []
    elif name == 'tag':
      self.theTags.append(attrs['name'])
    elif name == 'security_property':
      self.thePropertyName = attrs['property']
      self.thePropertyValue = attrs['value']
    elif name == 'access_right' or name == 'surface_type':
      self.theName = attrs['name']
      self.theScore = int(attrs['value'])

  def characters(self,data):
    if self.inDescription:
      self.theDescription += data
    elif self.inSignificance:
      self.theSignificance += data
    elif self.inRationale:
      self.theRationale += data

  def endElement(self,name):
    if name == 'asset':
      spDict = {}
      spDict['confidentiality'] = 0
      spDict['integrity'] = 0
      spDict['availability'] = 0
      spDict['accountability'] = 0
      spDict['anonymity'] = 0
      spDict['pseudonymity'] = 0
      spDict['unlinkability'] = 0
      spDict['unobservability'] = 0
      srDict = {}
      srDict['confidentiality'] = 'None'
      srDict['integrity'] = 'None'
      srDict['availability'] = 'None'
      srDict['accountability'] = 'None'
      srDict['anonymity'] = 'None'
      srDict['pseudonymity'] = 'None'
      srDict['unlinkability'] = 'None'
      srDict['unobservability'] = 'None'
      for sp in self.theSecurityProperties:
        spName = sp[0]
        spValue = a2i(sp[1])
        spRationale = sp[2]
        if spName in spDict:
          spDict[spName] = spValue
        if spName in srDict:
          srDict[spName] = spRationale
      spValues = [] 
      spValues.append(spDict['confidentiality'])
      spValues.append(spDict['integrity'])
      spValues.append(spDict['availability'])
      spValues.append(spDict['accountability'])
      spValues.append(spDict['anonymity'])
      spValues.append(spDict['pseudonymity'])
      spValues.append(spDict['unlinkability'])
      spValues.append(spDict['unobservability'])
      srValues = [] 
      srValues.append(srDict['confidentiality'])
      srValues.append(srDict['integrity'])
      srValues.append(srDict['availability'])
      srValues.append(srDict['accountability'])
      srValues.append(srDict['anonymity'])
      srValues.append(srDict['pseudonymity'])
      srValues.append(srDict['unlinkability'])
      srValues.append(srDict['unobservability'])
      p = TemplateAssetParameters(self.theName,self.theShortCode,self.theDescription,self.theSignificance,self.theAssetType,self.theSurfaceType,self.theAccessRight,spValues,srValues,self.theTags,self.theInterfaces)
      self.theAssets.append(p)
      self.resetAssetAttributes()
    elif name == 'security_property':
      self.theSecurityProperties.append((self.thePropertyName,self.thePropertyValue,self.theRationale))
      self.resetSecurityPropertyAttributes()
    elif name == 'description':
      self.inDescription = 0
    elif name == 'rationale':
      self.inRationale = 0
    elif name == 'significance':
      self.inSignificance = 0
    elif name == 'access_right' or name == 'surface_type':
      p = ValueTypeParameters(self.theName,self.theDescription,name,'',self.theScore,self.theRationale)
      self.theValueTypes.append(p)
      self.resetValueTypeAttributes()
