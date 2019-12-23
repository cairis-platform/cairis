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
from cairis.core.PersonaParameters import PersonaParameters
from cairis.core.PersonaEnvironmentProperties import PersonaEnvironmentProperties
from cairis.core.ExternalDocumentParameters import ExternalDocumentParameters
from cairis.core.DocumentReferenceParameters import DocumentReferenceParameters
from cairis.core.PersonaCharacteristicParameters import PersonaCharacteristicParameters
from cairis.core.TaskParameters import TaskParameters
from cairis.core.TaskEnvironmentProperties import TaskEnvironmentProperties
from cairis.core.Borg import Borg
from xml.sax.saxutils import unescape


__author__ = 'Shamal Faily'

def a2s(aStr):
  if aStr == 'a':
    return '*'
  elif aStr == '1..a':
    return '1..*'
  else:
    return aStr

def u2s(aStr):
  outStr = ''
  for c in aStr:
    if (c == '_'):
      outStr += ' '
    else:
      outStr += c
  return outStr

def durationValue(dLabel):
  if dLabel == 'Seconds':
    return 'Low'
  elif dLabel == 'Minutes':
    return 'Medium'
  else:
    return 'High'
    
def frequencyValue(fLabel):
  if fLabel == 'Hourly_or_more':
    return 'Low'
  elif fLabel == 'Daily_-_Weekly':
    return 'Medium'
  else:
    return 'High'
  
class UsabilityContentHandler(ContentHandler,EntityResolver):
  def __init__(self):
    self.thePersonas = []
    self.theExternalDocuments = []
    self.theDocumentReferences = []
    self.thePersonaCharacteristics = []
    self.theTasks = []
    b = Borg()
    self.configDir = b.configDir
    self.resetPersonaAttributes()
    self.resetDocumentReferenceAttributes()
    self.resetPersonaCharacteristicAttributes()
    self.resetExternalDocumentAttributes()
    self.resetTaskAttributes()

  def resolveEntity(self,publicId,systemId):
    return systemId

  def personas(self):
    return self.thePersonas

  def externalDocuments(self):
    return self.theExternalDocuments

  def documentReferences(self):
    return self.theDocumentReferences

  def personaCharacteristics(self):
    return self.thePersonaCharacteristics

  def tasks(self):
    return self.theTasks

  def resetPersonaAttributes(self):
    self.inPersona = 0
    self.inActivities = 0
    self.inAttitudes = 0
    self.inAptitudes = 0
    self.inMotivations = 0
    self.inSkills = 0
    self.inIntrinsic = 0
    self.inContextual = 0
    self.theName = ''
    self.theTags = []
    self.theType = ''
    self.theImage = ''
    self.isAssumptionPersona = False
    self.theActivities = ''
    self.theAptitudes = ''
    self.theMotivations = ''
    self.theSkills = ''
    self.theIntrinsic = ''
    self.theContextual = ''
    self.theEnvironmentProperties = []
    self.resetPersonaEnvironmentAttributes()

  def resetPersonaEnvironmentAttributes(self):
    self.theEnvironmentName = ''
    self.theRoles = []
    self.isDirect = True
    self.inNarrative = 0
    self.theNarrative = ''

  def resetExternalDocumentAttributes(self):
    self.theName = ''
    self.theVersion = ''
    self.theDate = ''
    self.theAuthors = ''
    self.inDescription = 0
    self.theDescription = ''

  def resetDocumentReferenceAttributes(self):
    self.inExcerpt = 0
    self.theName = ''
    self.theContributor = ''
    self.theDocument = ''
    self.theExcerpt = ''

  def resetPersonaCharacteristicAttributes(self):
    self.thePersona = ''
    self.inPC = 0
    self.theBvName = ''
    self.theModalQualifier = ''
    self.inDefinition = 0
    self.theDefinition = ''
    self.theGrounds = []
    self.theWarrants = []
    self.theRebuttals = []

  def resetTaskAttributes(self):
    self.inTask = 0
    self.theName = ''
    self.theTags = []
    self.theCode = ''
    self.theAuthor = ''
    self.isAssumptionTask = False
    self.inObjective = 0
    self.theObjective = ''
    self.theEnvironmentProperties = []
    self.resetTaskEnvironmentAttributes()

  def resetTaskEnvironmentAttributes(self):
    self.theEnvironmentName = ''
    self.inDependencies = 0
    self.inNarrative = 0
    self.inConsequences = 0
    self.inBenefits = 0
    self.theDependencies = ''
    self.theNarrative = ''
    self.theConsequences = ''
    self.theBenefits = ''
    self.theTaskPersonas = []
    self.theConcerns = []
    self.theConcernAssociations = []

  def startElement(self,name,attrs):
    self.currentElementName = name
    if name == 'persona':
      self.inPersona = 1
      self.theName = attrs['name']
      self.theType = attrs['type']
      self.theImage = attrs['image']
      if self.theImage != "" and os.path.isfile(self.theImage) == False:
        self.theImage = self.theImage
      if (attrs['assumption_persona'] == 'TRUE'):
        self.isAssumptionPersona = True
    elif name == 'persona_environment':
      self.theEnvironmentName = attrs['name']
      if (attrs['is_direct'] == 'FALSE'):
        self.isDirect = False
    elif name == 'persona_role':
      self.theRoles.append(attrs['name'])
    elif name == 'external_document':
      self.theName = attrs['name'].encode('utf-8')
      self.theVersion = attrs['version']
      self.theDate = attrs['date']
      self.theAuthors = attrs['authors']
    elif name == 'document_reference':
      self.theName = attrs['name'].encode('utf-8')
      self.theContributor = attrs['contributor']
      self.theDocument = attrs['document']
    elif name == 'persona_characteristic':
      self.thePersona = attrs['persona']
      self.inPC = 1
      self.theBvName = u2s(attrs['behavioural_variable'])
      self.theModalQualifier = attrs['modal_qualifier'] 
    elif (name == 'grounds' and self.inPC == 1):
      refName = attrs['reference']
      refType = attrs['type']
      refArtifact = ''
      self.theGrounds.append((refName,'',refType))
    elif (name == 'warrant' and self.inPC == 1):
      refName = attrs['reference']
      refType = attrs['type']
      refArtifact = ''
      self.theWarrants.append((refName,'',refType))
    elif (name == 'rebuttal' and self.inPC == 1):
      refName = attrs['reference']
      refType = attrs['type']
      refArtifact = ''
      self.theRebuttals.append((refName,'',refType))
    elif name == 'task':
      self.inTask = 1
      self.theName = attrs['name']
      try:
        self.theCode = attrs['code']
      except KeyError:
        self.theCode = ''
      self.theAuthor = attrs['author']
      if (attrs['assumption_task'] == 'TRUE'):
        self.isAssumptionTask = True
    elif name == 'task_environment':
      self.theEnvironmentName = attrs['name']
    elif name == 'task_persona':
      self.theTaskPersonas.append((attrs['persona'],durationValue(attrs['duration']),frequencyValue(attrs['frequency']),attrs['demands'],attrs['goal_conflict']))
    elif name == 'task_concern':
      self.theConcerns.append(attrs['asset'])
    elif name == 'task_concern_association':
      self.theConcernAssociations.append((attrs['source_name'],a2s(attrs['source_nry']),attrs['link_name'],attrs['target_name'],a2s(attrs['target_nry'])))
    elif name == 'activities':
      self.inActivities = 1
      self.theActivities = ''
    elif name == 'attitudes':
      self.inAttitudes = 1
      self.theAttitudes = ''
    elif name == 'aptitudes':
      self.inAptitudes = 1
      self.theAptitudes = ''
    elif name == 'motivations':
      self.inMotivations = 1
      self.theMotivations = ''
    elif name == 'skills':
      self.inSkills = 1
      self.theSkills = ''
    elif name == 'intrinsic':
      self.inIntrinsic = 1
      self.theIntrinsic = ''
    elif name == 'contextual':
      self.inContextual = 1
      self.theContextual = ''
    elif name == 'narrative':
      self.inNarrative = 1
      self.theNarrative = ''
    elif name == 'consequences':
      self.inConsequences = 1
      self.theConsequences = ''
    elif name == 'benefits':
      self.inBenefits = 1
      self.theBenefits = ''
    elif name == 'excerpt':
      self.inExcerpt = 1
      self.theExcerpt = ''
    elif name == 'description':
      self.inDescription = 1
      self.theDescription = ''
    elif name == 'definition':
      self.inDefinition = 1
      self.theDefinition = ''
    elif name == 'dependencies':
      self.inDependencies = 1
      self.theDependencies = ''
    elif name == 'objective':
      self.inObjective = 1
      self.theObjective = ''
    elif name == 'tag':
      if ((self.inPersona == 1) or (self.inTask == 1)):
        self.theTags.append(attrs['name'])

  def characters(self,data):
    if self.inActivities:
      self.theActivities += data
    elif self.inAttitudes:
      self.theAttitudes += data
    elif self.inAptitudes:
      self.theAptitudes += data
    elif self.inMotivations:
      self.theMotivations += data
    elif self.inSkills:
      self.theSkills += data
    elif self.inIntrinsic:
      self.theIntrinsic += data
    elif self.inContextual:
      self.theContextual += data
    elif self.inConsequences:
      self.theConsequences += data
    elif self.inBenefits:
      self.theBenefits += data
    elif self.inExcerpt:
      self.theExcerpt += data
    elif self.inDescription:
      self.theDescription += data
    elif self.inDefinition:
      self.theDefinition += data
    elif self.inDependencies:
      self.theDependencies += data
    elif self.inObjective:
      self.theObjective += data
    elif self.inNarrative:
      self.theNarrative += data

  def endElement(self,name):
    if name == 'persona':
      p = PersonaParameters(self.theName,unescape(self.theActivities),unescape(self.theAttitudes),unescape(self.theAptitudes),unescape(self.theMotivations),unescape(self.theSkills),unescape(self.theIntrinsic),unescape(self.theContextual),self.theImage,self.isAssumptionPersona,self.theType,self.theTags,self.theEnvironmentProperties,{})
      self.thePersonas.append(p)
      self.resetPersonaAttributes()
    elif name == 'persona_environment':
      p = PersonaEnvironmentProperties(self.theEnvironmentName,self.isDirect,unescape(self.theNarrative),self.theRoles,{'narrative':{}})
      self.theEnvironmentProperties.append(p)
      self.resetPersonaEnvironmentAttributes()
    elif name == 'external_document':
      p = ExternalDocumentParameters(self.theName,self.theVersion,self.theDate,self.theAuthors,unescape(self.theDescription))
      self.theExternalDocuments.append(p)
      self.resetExternalDocumentAttributes()
    elif name == 'document_reference':
      p = DocumentReferenceParameters(self.theName,self.theDocument,self.theContributor,unescape(self.theExcerpt))
      self.theDocumentReferences.append(p)
      self.resetDocumentReferenceAttributes()
    elif name == 'persona_characteristic':
      p = PersonaCharacteristicParameters(self.thePersona,self.theModalQualifier,self.theBvName,unescape(self.theDefinition),self.theGrounds,self.theWarrants,[],self.theRebuttals)
      self.thePersonaCharacteristics.append(p)
      self.resetPersonaCharacteristicAttributes()
    elif name == 'task':
      p = TaskParameters(unescape(self.theName),unescape(self.theCode),unescape(self.theObjective),self.isAssumptionTask,self.theAuthor,self.theTags,self.theEnvironmentProperties)
      self.theTasks.append(p)
      self.resetTaskAttributes()
    elif name == 'task_environment':
      p = TaskEnvironmentProperties(unescape(self.theEnvironmentName),unescape(self.theDependencies),self.theTaskPersonas,self.theConcerns,self.theConcernAssociations,unescape(self.theNarrative),unescape(self.theConsequences),unescape(self.theBenefits),[],{'narrative':{},'consequences':{},'benefits':{}})
      self.theEnvironmentProperties.append(p)
      self.resetTaskEnvironmentAttributes()
    elif name == 'activities':
      self.inActivities = 0
    elif name == 'attitudes':
      self.inAttitudes = 0
    elif name == 'aptitudes':
      self.inAptitudes = 0
    elif name == 'motivations':
      self.inMotivations = 0
    elif name == 'skills':
      self.inSkills = 0
    elif name == 'intrinsic':
      self.inIntrinsic = 0
    elif name == 'contextual':
      self.inContextual = 0
    elif name == 'narrative':
      self.inNarrative = 0
    elif name == 'excerpt':
      self.inExcerpt = 0
    elif name == 'description':
      self.inDescription = 0
    elif name == 'definition':
      self.inDefinition = 0
    elif name == 'dependencies':
      self.inDependencies = 0
    elif name == 'objective':
      self.inObjective = 0
    elif name == 'benefits':
      self.inBenefits = 0
    elif name == 'consequences':
      self.inConsequences = 0
