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
from cairis.core.TemplateAssetParameters import TemplateAssetParameters
from cairis.core.TemplateRequirementParameters import TemplateRequirementParameters
from cairis.core.SecurityPatternParameters import SecurityPatternParameters
from cairis.core.ValueTypeParameters import ValueTypeParameters
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

class SecurityPatternContentHandler(ContentHandler,EntityResolver):
  def __init__(self):
    self.theAssets = []
    self.theSecurityPatterns = []
    self.theMetricTypes = []
    b = Borg()
    self.configDir = b.configDir
    self.resetAssetAttributes()
    self.resetSecurityPropertyAttributes()
    self.resetPatternAttributes()

  def resolveEntity(self,publicId,systemId):
    return systemId

  def patterns(self):
    return self.theSecurityPatterns

  def metricTypes(self):
    return self.theMetricTypes

  def assets(self):
    return self.theAssets

  def resetPatternAttributes(self):
    self.inContext = 0
    self.inProblem = 0
    self.inSolution = 0
    self.inDescription = 0
    self.inRationale = 0
    self.inFitCriterion = 0
    self.theName = ''
    self.theContext = ''
    self.theProblem = ''
    self.theSolution = ''
    self.theStructure = []
    self.theRequirements = []
    self.resetStructure()
    self.resetRequirement()

  def resetAssetAttributes(self):
    self.inDescription = 0
    self.inSignificance = 0
    self.theName = ''
    self.theShortCode = ''
    self.theAssetType = ''
    self.theDescription = ''
    self.theSignificance = ''
    self.theSurfaceType = ''
    self.theAccessRight = ''
    self.theTags = []
    self.theInterfaces = []
    self.theSecurityProperties = []

  def resetSecurityPropertyAttributes(self):
    self.thePropertyName = ''
    self.thePropertyValue = 'None'
    self.inRationale = 0
    self.theRationale = ''

  def resetStructure(self):
    self.theHeadName = ''
    self.theHeadAdornment = ''
    self.theHeadNry = ''
    self.theHeadRole = ''
    self.theTailRole = ''
    self.theTailNry = ''
    self.theTailAdornment = ''
    self.theTailName = ''

  def resetRequirement(self):
    self.theAsset = ''
    self.theType = ''
    self.theReqName = ''
    self.theDescription = ''
    self.theRationale = ''
    self.theFitCriterion = ''

  def resetValueTypeAttributes(self):
    self.inDescription = 0
    self.inRationale = 0
    self.theName = ''
    self.theDescription = ''
    self.theRationale = ''
    self.theScore = 0

  def startElement(self,name,attrs):
    self.currentElementName = name
    if name == 'asset':
      self.theName = attrs['name']
      self.theShortCode = attrs['short_code']
      self.theAssetType = attrs['type']
      self.theSurfaceType = attrs['surface_type']
      self.theAccessRight = attrs['access_right']
      self.theSecurityProperties = []
    elif name == 'tag':
      self.theTags.append(attrs['name'])
    elif name == 'interface':
      self.theInterfaces.append((attrs['name'],it2Id(attrs['type'])))
    elif name == 'security_property':
      self.thePropertyName = attrs['property']
      self.thePropertyValue = attrs['value']
    elif name == 'description':
      self.inDescription = 1
      self.theDescripton = ''
    elif name == 'significance':
      self.inSignificance = 1
      self.theSignificance = ''
    elif name == 'pattern':
      self.theName = attrs['name']
    elif name == 'structure':
      self.theHeadName = attrs['head_asset'] 
      self.theHeadAdornment = attrs['head_adornment']
      rawHeadNry = attrs['head_nry']
      if (rawHeadNry == 'a'):
        rawHeadNry = '*'
      elif (rawHeadNry == '1..a'):
        rawHeadNry = '1..*'
      self.theHeadNry = rawHeadNry
      self.theHeadRole = attrs['head_role']
      self.theTailRole = attrs['tail_role']
      rawTailNry = attrs['tail_nry']
      if (rawTailNry == 'a'):
        rawTailNry = '*'
      elif (rawTailNry == '1..a'):
        rawTailNry = '1..*'
      self.theTailNry = rawTailNry
      self.theTailAdornment = attrs['tail_adornment']
      self.theTailName = attrs['tail_asset'] 
    elif name == 'requirement':
      self.theReqName = attrs['name']
      self.theAsset = attrs['asset']
      rawType = attrs['type']
      self.theType = rawType.replace('_',' ')
    elif name == 'context':
      self.inContext = 1
      self.theContext = ''
    elif name == 'problem':
      self.inProblem = 1
      self.theProblem = ''
    elif name == 'solution':
      self.inSolution = 1
      self.theSolution = ''
    elif name == 'rationale':
      self.inRationale = 1
      self.theRationale = ''
    elif name == 'fit_criterion':
      self.inFitCriterion = 1
      self.theFitCriterion = ''
    elif name == 'access_right' or name == 'surface_type':
      self.theName = attrs['name']
      self.theScore = int(attrs['value'])


  def characters(self,data):
    if self.inDescription:
      self.theDescription += data
    elif self.inSignificance:
      self.theSignificance += data
    elif self.inContext:
      self.theContext += data
    elif self.inProblem:
      self.theProblem += data
    elif self.inSolution:
      self.theSolution += data
    elif self.inRationale:
      self.theRationale += data
    elif self.inFitCriterion:
      self.theFitCriterion += data

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
    elif name == 'pattern':
      p = SecurityPatternParameters(self.theName,self.theContext,self.theProblem,self.theSolution,self.theRequirements,self.theStructure)
      self.theSecurityPatterns.append(p)
      self.resetPatternAttributes() 
    elif name == 'structure':
      self.theStructure.append((self.theHeadName,self.theHeadAdornment,self.theHeadNry,self.theHeadRole,self.theTailRole,self.theTailNry,self.theTailAdornment,self.theTailName))
      self.resetStructure()
    elif name == 'requirement':
      tr = TemplateRequirementParameters(self.theReqName,self.theAsset,self.theType,self.theDescription,self.theRationale,self.theFitCriterion)
      self.theRequirements.append(tr)
      self.resetRequirement()
    elif name == 'description':
      self.inDescription = 0
    elif name == 'rationale':
      self.inRationale = 0
    elif name == 'significance':
      self.inSignificance = 0
    elif name == 'context':
      self.inContext = 0
    elif name == 'problem':
      self.inProblem = 0
    elif name == 'solution':
      self.inSolution = 0
    elif name == 'fit_criterion':
      self.inFitCriterion = 0
    elif name == 'access_right' or name == 'surface_type':
      p = ValueTypeParameters(self.theName,self.theDescription,name,'',self.theScore,self.theRationale)
      self.theMetricTypes.append(p)
      self.resetValueTypeAttributes()

