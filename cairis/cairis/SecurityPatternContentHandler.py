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
from TemplateAssetParameters import TemplateAssetParameters
from SecurityPatternParameters import SecurityPatternParameters
from Borg import Borg

class SecurityPatternContentHandler(ContentHandler,EntityResolver):
  def __init__(self):
    self.theAssets = []
    self.theSecurityPatterns = []
    b = Borg()
    self.configDir = b.configDir
    self.resetAssetAttributes()
    self.resetPatternAttributes()

  def resolveEntity(self,publicId,systemId):
    return self.configDir + '/securitypattern.dtd'


  def patterns(self):
    return self.theSecurityPatterns

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
    self.inCritical = 0
    self.theName = ''
    self.theShortCode = ''
    self.theAssetType = ''
    self.isCritical = False
    self.theCriticalRationale = ''
    self.theDescription = ''
    self.theSignificance = ''
    self.theConfidentialityValue = 'None'
    self.theIntegrityValue = 'None'
    self.theAvailabilityValue = 'None'
    self.theAccountabilityValue = 'None'
    self.theAnonymityValue = 'None'
    self.thePseudonymityValue = 'None'
    self.theUnlinkabilityValue = 'None'
    self.theUnobservabilityValue = 'None'


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
    

  def startElement(self,name,attrs):
    self.currentElementName = name
    if name == 'asset':
      self.theName = attrs['name']
      self.theShortCode = attrs['short_code']
      self.theAssetType = attrs['asset_type']
      self.theConfidentialityValue = attrs['confidentiality']
      self.theIntegrityValue = attrs['integrity']
      self.theAvailabilityValue = attrs['availability']
      self.theAccountabilityValue = attrs['accountability']
      self.theAnonymityValue = attrs['anonymity']
      self.thePseudonymityValue = attrs['pseudonymity']
      self.theUnlinkabilityValue = attrs['unlinkability']
      self.theUnobservabilityValue = attrs['unobservability']
    elif name == 'description':
      self.inDescription = 1
    elif name == 'significance':
      self.inSignificance = 1
    elif name == 'critical':
      self.inCritical = 1
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
    elif name == 'problem':
      self.inProblem = 1
    elif name == 'solution':
      self.inSolution = 1
    elif name == 'rationale':
      self.inRationale = 1
    elif name == 'fit_criterion':
      self.inFitCriterion = 1

  def characters(self,data):
    if self.inDescription:
      self.theDescription = data
      self.inDescription = 0
    elif self.inSignificance:
      self.theSignificance = data
      self.inSignificance = 0
    elif self.inCritical:
      self.isCritical = True
      self.theCriticalRationale = data
      self.inCritical = 0
    elif self.inContext:
      self.theContext = data
      self.inContext = 0
    elif self.inProblem:
      self.theProblem = data
      self.inProblem = 0
    elif self.inSolution:
      self.theSolution = data
      self.inSolution = 0
    elif self.inRationale:
      self.theRationale = data
      self.inRationale = 0
    elif self.inFitCriterion:
      self.theFitCriterion = data
      self.inFitCriterion = 0

  def endElement(self,name):
    if name == 'asset':
      p = TemplateAssetParameters(self.theName,self.theShortCode,self.theDescription,self.theSignificance,self.theAssetType,self.isCritical,self.theCriticalRationale,self.theConfidentialityValue,self.theIntegrityValue,self.theAvailabilityValue,self.theAccountabilityValue,self.theAnonymityValue,self.thePseudonymityValue,self.theUnlinkabilityValue,self.theUnobservabilityValue)
      self.theAssets.append(p)
      self.resetAssetAttributes()
    elif name == 'pattern':
      p = SecurityPatternParameters(self.theName,self.theContext,self.theProblem,self.theSolution,self.theRequirements,self.theStructure)
      self.theSecurityPatterns.append(p)
      self.resetPatternAttributes() 
    elif name == 'structure':
      self.theStructure.append((self.theHeadName,self.theHeadAdornment,self.theHeadNry,self.theHeadRole,self.theTailRole,self.theTailNry,self.theTailAdornment,self.theTailName))
      self.resetStructure()
    elif name == 'requirement':
      self.theRequirements.append((self.theReqName,self.theDescription,self.theType,self.theRationale,self.theFitCriterion,self.theAsset))
      self.resetRequirement()
