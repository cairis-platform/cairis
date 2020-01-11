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
from cairis.core.RoleParameters import RoleParameters
from cairis.core.AssetParameters import AssetParameters
from cairis.core.VulnerabilityParameters import VulnerabilityParameters
from cairis.core.AttackerParameters import AttackerParameters
from cairis.core.ThreatParameters import ThreatParameters
from cairis.core.RiskParameters import RiskParameters
from cairis.core.ResponseParameters import ResponseParameters
from cairis.core.AssetEnvironmentProperties import AssetEnvironmentProperties
from cairis.core.VulnerabilityEnvironmentProperties import VulnerabilityEnvironmentProperties
from cairis.core.AttackerEnvironmentProperties import AttackerEnvironmentProperties
from cairis.core.ThreatEnvironmentProperties import ThreatEnvironmentProperties
from cairis.core.MisuseCaseEnvironmentProperties import MisuseCaseEnvironmentProperties
from cairis.core.AcceptEnvironmentProperties import AcceptEnvironmentProperties
from cairis.core.TransferEnvironmentProperties import TransferEnvironmentProperties
from cairis.core.MitigateEnvironmentProperties import MitigateEnvironmentProperties
from cairis.core.MisuseCase import MisuseCase
from cairis.core.ClassAssociationParameters import ClassAssociationParameters
from cairis.core.Borg import Borg
from xml.sax.saxutils import unescape

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

class RiskAnalysisContentHandler(ContentHandler,EntityResolver):
  def __init__(self):
    self.theRoleParameters = []
    self.theAssetParameters = []
    self.theVulnerabilities = []
    self.theAttackerParameters = []
    self.theThreats = []
    self.theRisks = []
    self.theResponses = []
    self.theEnvironmentProperties = []
    self.theAssociations = []
    b = Borg()
    self.configDir = b.configDir
    self.resetRoleAttributes()
    self.resetAssetAttributes()
    self.resetVulnerabilityAttributes()
    self.resetAttackerAttributes()
    self.resetThreatAttributes()
    self.resetRiskAttributes()
    self.resetResponseAttributes()
    self.resetAssociationAttributes()

  def resolveEntity(self,publicId,systemId):
    return systemId


  def associations(self):
    return self.theAssociations

  def roles(self):
    return self.theRoleParameters

  def assets(self):
    return self.theAssetParameters

  def vulnerabilities(self):
    return self.theVulnerabilities

  def attackers(self):
    return self.theAttackerParameters

  def threats(self):
    return self.theThreats

  def risks(self):
    return self.theRisks

  def responses(self):
    return self.theResponses

  def resetRoleAttributes(self):
    self.inDescription = 0
    self.theName = ''
    self.theType = ''
    self.theShortCode = ''
    self.theDescription = ''

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
    self.theTags = []
    self.theInterfaces = []
    self.theEnvironmentProperties = []

  def resetSecurityPropertyAttributes(self):
    self.theEnvironmentName = ''
    self.thePropertyName = ''
    self.thePropertyValue = 'None'
    self.inRationale = 0
    self.theRationale = ''


  def resetVulnerabilityAttributes(self):
    self.inDescription = 0
    self.theName = ''
    self.theType = ''
    self.theDescription = ''
    self.theTags = []
    self.theEnvironmentProperties = []
    self.resetVulnerabilityEnvironmentAttributes()

  def resetVulnerabilityEnvironmentAttributes(self):
    self.theEnvironmentName = ''
    self.theSeverity = ''
    self.theAssets = []

  def resetAttackerAttributes(self):
    self.inDescription = 0
    self.theName = ''
    self.theImage = ''
    self.theDescription = ''
    self.theTags = []
    self.theEnvironmentProperties = []
    self.resetAttackerEnvironmentAttributes()

  def resetAttackerEnvironmentAttributes(self):
    self.theEnvironmentName = ''
    self.theRoles = []
    self.theMotivations = []
    self.theCapabilities = []

  def resetThreatAttributes(self):
    self.inMethod = 0
    self.theName = ''
    self.theType = ''
    self.theMethod = ''
    self.theTags = []
    self.theEnvironmentProperties = []
    self.resetThreatEnvironmentAttributes()

  def resetThreatEnvironmentAttributes(self):
    self.theEnvironmentName = ''
    self.theLikelihood = ''
    self.theAttackers = []
    self.theAssets = []
    self.theSpDict = {}
    self.theSpDict['confidentiality'] = (0,'None')
    self.theSpDict['integrity'] = (0,'None')
    self.theSpDict['availability'] = (0,'None')
    self.theSpDict['accountability'] = (0,'None')
    self.theSpDict['anonymity'] = (0,'None')
    self.theSpDict['pseudonymity'] = (0,'None')
    self.theSpDict['unlinkability'] = (0,'None')
    self.theSpDict['unobservability'] = (0,'None')
    self.resetThreatenedPropertyAttributes()

  def resetThreatenedPropertyAttributes(self):
    self.thePropertyName = ''
    self.thePropertyValue = 'None'
    self.inRationale = 0
    self.theRationale = ''

  def resetRiskAttributes(self):
    self.theName = ''
    self.theThreat = ''
    self.theVulnerability = ''
    self.theTags = []
    self.theEnvironmentProperties = []
    self.resetRiskEnvironmentAttributes()

  def resetRiskEnvironmentAttributes(self):
    self.theEnvironmentName = ''
    self.theDescription = ''

  def resetResponseAttributes(self):
    self.theRisk = ''
    self.theType = ''
    self.theTags = []
    self.theEnvironmentProperties = []
    self.resetResponseEnvironmentAttributes()

  def resetResponseEnvironmentAttributes(self):
    self.inDescription = 0
    self.theEnvironmentName = ''
    self.theCost = ''
    self.theDescription = ''
    self.theResponseRoles = []
    self.theDetectionPoint = ''
    self.theDetectionMechanisms = []

  def resetAssociationAttributes(self):
    self.theEnvironmentName = ''
    self.theHeadName = ''
    self.theHeadAdornment = ''
    self.theHeadNav = ''
    self.theHeadNry = ''
    self.theHeadRole = ''
    self.theTailRole = ''
    self.theTailNry = ''
    self.theTailNav = ''
    self.theTailAdornment = ''
    self.theTailName = ''
    self.theRationale = ''

  def startElement(self,name,attrs):
    self.currentElementName = name
    if name == 'role':
      self.theName = attrs['name']
      self.theShortCode = attrs['short_code']
      self.theType = attrs['type']
    elif name == 'tag':
      self.theTags.append(attrs['name'])
    elif name == 'asset':
      self.theName = attrs['name']
      self.theShortCode = attrs['short_code']
      self.theAssetType = attrs['type']
      self.isCritical = attrs['is_critical']
      self.theSecurityProperties = []
    elif (name == 'interface'):
      arName = 'None'
      privName = 'None'
      try:
        arName = attrs['access_right'] 
      except KeyError:
        pass

      try:
        privName = attrs['privilege'] 
      except KeyError:
        pass
      self.theInterfaces.append((attrs['name'],it2Id(attrs['type']),arName,privName))
    elif name == 'security_property':
      self.theEnvironmentName = attrs['environment'] 
      self.thePropertyName = attrs['property']
      self.thePropertyValue = attrs['value']
    elif name == 'vulnerability':
      self.theName = attrs['name']
      self.theType = attrs['type']
    elif name == 'vulnerability_environment':
      self.theEnvironmentName = attrs['name']
      self.theSeverity = attrs['severity']
    elif name == 'vulnerable_asset':
      self.theAssets.append(attrs['name'])
    elif name == 'attacker':
      self.theName = attrs['name']
      self.theImage = attrs['image']
    elif name == 'attacker_environment':
      self.theEnvironmentName = attrs['name']
    elif name == 'attacker_role':
      self.theRoles.append(attrs['name'])
    elif name == 'motivation':
      self.theMotivations.append(attrs['name'])
    elif name == 'capability':
      self.theCapabilities.append((attrs['name'],attrs['value']))
    elif name == 'threat':
      self.theName = attrs['name']
      self.theType = attrs['type']
    elif name == 'threat_environment':
      self.theEnvironmentName = attrs['name']
      self.theLikelihood = attrs['likelihood']
    elif name == 'threat_attacker':
      self.theAttackers.append(attrs['name'])
    elif name == 'threatened_asset':
      self.theAssets.append(attrs['name'])
    elif name == 'threatened_property':
      self.thePropertyName = attrs['name']
      self.thePropertyValue = a2i(attrs['value'])
    elif name == 'risk':
      self.theName = attrs['name']
      self.theThreat = attrs['threat']
      self.theVulnerability = attrs['vulnerability']
    elif name == 'misusecase':
      self.theEnvironmentName = attrs['environment']
    elif name == 'response':
      self.theRisk = attrs['risk']
      self.theType = attrs['type']
    elif name == 'accept_environment':
      self.theEnvironmentName = attrs['name']
      self.theCost = attrs['cost']
    elif name == 'transfer_environment':
      self.theEnvironmentName = attrs['name']
    elif name == 'response_role':
      self.theResponseRoles.append((attrs['name'],attrs['cost']))
    elif name == 'deter_environment':
      self.theEnvironmentName = attrs['name']
      self.theType = 'Deter'
    elif name == 'prevent_environment':
      self.theEnvironmentName = attrs['name']
      self.theType = 'Prevent'
    elif name == 'detect_environment':
      self.theEnvironmentName = attrs['name']
      self.theDetectionPoint = attrs['point']
      self.theType = 'Detect'
    elif name == 'react_environment':
      self.theEnvironmentName = attrs['name']
      self.theType = 'React'
    elif name == 'detection_mechanism':
      self.theDetectionMechanisms.append(attrs['name'])
    elif name == 'description':
      self.inDescription = 1
      self.theDescription = ''
    elif name == 'method':
      self.inMethod = 1
      self.theMethod = ''
    elif name == 'narrative':
      self.inDescription = 1
      self.theDescription = ''
    elif name == 'rationale':
      self.inRationale = 1
      self.theRationale = ''
    elif name == 'significance':
      self.inSignificance = 1
      self.theSignificance = ''
    elif name == 'critical':
      self.inCritical = 1
      self.theCritical = ''
    elif name == 'asset_association':
      self.theEnvironmentName = attrs['environment'] 
      self.theHeadName = attrs['head_name'] 
      self.theHeadAdornment = attrs['head_adornment']
      self.theHeadNav = attrs['head_nav']
      self.theTailNav = attrs['tail_nav']

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
      self.theTailName = attrs['tail_name'] 

  def characters(self,data):
    if self.inDescription:
      self.theDescription += data
    elif self.inSignificance:
      self.theSignificance += data
    elif self.inMethod:
      self.theMethod += data
    elif self.inRationale:
      self.theRationale += data
    elif self.inCritical:
      self.isCritical = True
      self.theCriticalRationale += data

  def endElement(self,name):
    if name == 'role':
      p = RoleParameters(self.theName,self.theType,unescape(self.theShortCode),unescape(self.theDescription),[])
      self.theRoleParameters.append(p)
      self.resetRoleAttributes()
    elif name == 'asset':
      envDict = {}
      for sp in self.theSecurityProperties:
        envName = sp[0]
        spName = sp[1]
        spValue = a2i(sp[2])
        spRationale = sp[3]
        if envName in envDict:
          (envDict[envName])[spName] = (spValue,spRationale)
        else:
          spDict = {}
          spDict['confidentiality'] = (0,'None')
          spDict['integrity'] = (0,'None')
          spDict['availability'] = (0,'None')
          spDict['accountability'] = (0,'None')
          spDict['anonymity'] = (0,'None')
          spDict['pseudonymity'] = (0,'None')
          spDict['unlinkability'] = (0,'None')
          spDict['unobservability'] = (0,'None')
          spDict[spName] = (spValue,spRationale)
          envDict[envName] = spDict
      for envName in envDict:
        spDict = envDict[envName]
        cProperty,cRationale = spDict['confidentiality']
        iProperty,iRationale = spDict['integrity']
        avProperty,avRationale = spDict['availability']
        acProperty,acRationale = spDict['accountability']
        anProperty,anRationale = spDict['anonymity']
        panProperty,panRationale = spDict['pseudonymity']
        unlProperty,unlRationale = spDict['unlinkability']
        unoProperty,unoRationale = spDict['unobservability']
        ep = AssetEnvironmentProperties(envName,[cProperty,iProperty,avProperty,acProperty,anProperty,panProperty,unlProperty,unoProperty],[cRationale,iRationale,avRationale,acRationale,anRationale,panRationale,unlRationale,unoRationale])
        self.theEnvironmentProperties.append(ep)
      p = AssetParameters(self.theName,unescape(self.theShortCode),unescape(self.theDescription),unescape(self.theSignificance),self.theAssetType,self.isCritical,self.theCriticalRationale,self.theTags,self.theInterfaces,self.theEnvironmentProperties)
      self.theAssetParameters.append(p)
      self.resetAssetAttributes()
    elif name == 'security_property':
      self.theSecurityProperties.append((self.theEnvironmentName,self.thePropertyName,self.thePropertyValue,unescape(self.theRationale)))
      self.resetSecurityPropertyAttributes() 
    elif name == 'threatened_property':
      self.theSpDict[self.thePropertyName] = (self.thePropertyValue,unescape(self.theRationale))
      self.resetThreatenedPropertyAttributes()
    elif name == 'vulnerability':
      p = VulnerabilityParameters(self.theName,unescape(self.theDescription),self.theType,self.theTags,self.theEnvironmentProperties)
      self.theVulnerabilities.append(p)
      self.resetVulnerabilityAttributes()
    elif name == 'vulnerability_environment':
      p = VulnerabilityEnvironmentProperties(self.theEnvironmentName,self.theSeverity,self.theAssets)
      self.theEnvironmentProperties.append(p)
      self.resetVulnerabilityEnvironmentAttributes()
    elif name == 'attacker':
      p = AttackerParameters(self.theName,unescape(self.theDescription),self.theImage,self.theTags,self.theEnvironmentProperties)
      self.theAttackerParameters.append(p)
      self.resetAttackerAttributes()
    elif name == 'attacker_environment':
      p = AttackerEnvironmentProperties(self.theEnvironmentName,self.theRoles,self.theMotivations,self.theCapabilities)
      self.theEnvironmentProperties.append(p)
      self.resetAttackerEnvironmentAttributes()
    elif name == 'threat':
      p = ThreatParameters(self.theName,self.theType,unescape(self.theMethod),self.theTags,self.theEnvironmentProperties)
      self.theThreats.append(p)
      self.resetThreatAttributes()
    elif name == 'threat_environment':
      cProperty,cRationale = self.theSpDict['confidentiality']
      iProperty,iRationale = self.theSpDict['integrity']
      avProperty,avRationale = self.theSpDict['availability']
      acProperty,acRationale = self.theSpDict['accountability']
      anProperty,anRationale = self.theSpDict['anonymity']
      panProperty,panRationale = self.theSpDict['pseudonymity']
      unlProperty,unlRationale = self.theSpDict['unlinkability']
      unoProperty,unoRationale = self.theSpDict['unobservability']
      p = ThreatEnvironmentProperties(self.theEnvironmentName,self.theLikelihood,self.theAssets,self.theAttackers,[cProperty,iProperty,avProperty,acProperty,anProperty,panProperty,unlProperty,unoProperty],[cRationale,iRationale,avRationale,acRationale,anRationale,panRationale,unlRationale,unoRationale])
      self.theEnvironmentProperties.append(p)
      self.resetThreatEnvironmentAttributes()
    elif name == 'risk':
      mc = MisuseCase(-1,'Exploit ' + self.theName,self.theEnvironmentProperties,self.theName)
      p = RiskParameters(self.theName,self.theThreat,self.theVulnerability,mc,self.theTags)
      self.theRisks.append(p)
      self.resetRiskAttributes()
    elif name == 'misusecase':
      p = MisuseCaseEnvironmentProperties(self.theEnvironmentName,unescape(self.theDescription))
      self.theEnvironmentProperties.append(p)
      self.resetRiskEnvironmentAttributes()
    elif name == 'response':
      p = ResponseParameters(self.theType + ' ' + self.theRisk,self.theRisk,self.theTags,self.theEnvironmentProperties,self.theType)
      self.theResponses.append(p)
      self.resetResponseAttributes()
    elif name == 'accept_environment':
      p = AcceptEnvironmentProperties(self.theEnvironmentName,self.theCost,unescape(self.theDescription))
      self.theEnvironmentProperties.append(p)
      self.resetResponseEnvironmentAttributes()
    elif name == 'transfer_environment':
      p = TransferEnvironmentProperties(self.theEnvironmentName,unescape(self.theDescription),self.theResponseRoles)
      self.theEnvironmentProperties.append(p)
      self.resetResponseEnvironmentAttributes()
    elif name == 'deter_environment':
      p = MitigateEnvironmentProperties(self.theEnvironmentName,'Deter')
      self.theEnvironmentProperties.append(p)
      self.resetResponseEnvironmentAttributes()
    elif name == 'prevent_environment':
      p = MitigateEnvironmentProperties(self.theEnvironmentName,'Prevent')
      self.theEnvironmentProperties.append(p)
      self.resetResponseEnvironmentAttributes()
    elif name == 'detect_environment':
      p = MitigateEnvironmentProperties(self.theEnvironmentName,'Detect',self.theDetectionPoint)
      self.theEnvironmentProperties.append(p)
      self.resetResponseEnvironmentAttributes()
    elif name == 'react_environment':
      p = MitigateEnvironmentProperties(self.theEnvironmentName,'React','',self.theDetectionMechanisms)
      self.theEnvironmentProperties.append(p)
      self.resetResponseEnvironmentAttributes()
    elif name == 'asset_association':
      p = ClassAssociationParameters(self.theEnvironmentName,self.theHeadName,'asset',self.theHeadNav,self.theHeadAdornment,self.theHeadNry,self.theHeadRole,self.theTailRole,self.theTailNry,self.theTailAdornment,self.theTailNav,'asset',self.theTailName,unescape(self.theRationale))
      self.theAssociations.append(p)
      self.resetAssociationAttributes()
    elif name == 'description':
      self.inDescription = 0
    elif name == 'method':
      self.inMethod = 0
    elif name == 'narrative':
      self.inDescription = 0
    elif name == 'rationale':
      self.inRationale = 0
    elif name == 'significance':
      self.inSignificance = 0
    elif name == 'critical':
      self.inCritical = 0
