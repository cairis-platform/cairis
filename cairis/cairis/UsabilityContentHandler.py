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
from PersonaParameters import PersonaParameters
from PersonaEnvironmentProperties import PersonaEnvironmentProperties
from ExternalDocumentParameters import ExternalDocumentParameters
from DocumentReferenceParameters import DocumentReferenceParameters
from ConceptReferenceParameters import ConceptReferenceParameters
from PersonaCharacteristicParameters import PersonaCharacteristicParameters
from TaskCharacteristicParameters import TaskCharacteristicParameters
from TaskParameters import TaskParameters
from TaskEnvironmentProperties import TaskEnvironmentProperties
from UseCaseParameters import UseCaseParameters
from UseCaseEnvironmentProperties import UseCaseEnvironmentProperties
from Steps import Steps
from Step import Step
from Borg import Borg

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
    self.theConceptReferences = []
    self.thePersonaCharacteristics = []
    self.theTaskCharacteristics = []
    self.theTasks = []
    self.theUseCases = []
    b = Borg()
    self.configDir = b.configDir
    self.resetPersonaAttributes()
    self.resetDocumentReferenceAttributes()
    self.resetConceptReferenceAttributes()
    self.resetPersonaCharacteristicAttributes()
    self.resetTaskCharacteristicAttributes()
    self.resetTaskAttributes()
    self.resetUseCaseAttributes()

  def resolveEntity(self,publicId,systemId):
    return self.configDir + '/usability.dtd'

  def personas(self):
    return self.thePersonas

  def externalDocuments(self):
    return self.theExternalDocuments

  def documentReferences(self):
    return self.theDocumentReferences

  def conceptReferences(self):
    return self.theConceptReferences

  def personaCharacteristics(self):
    return self.thePersonaCharacteristics

  def taskCharacteristics(self):
    return self.theTaskCharacteristics

  def tasks(self):
    return self.theTasks

  def usecases(self):
    return self.theUseCases

  def resetPersonaAttributes(self):
    self.inActivities = 0
    self.inAttitudes = 0
    self.inAptitudes = 0
    self.inMotivations = 0
    self.inSkills = 0
    self.theName = ''
    self.theTags = []
    self.theType = ''
    self.theImage = ''
    self.isAssumptionPersona = False
    self.theActivities = ''
    self.theAptitudes = ''
    self.theMotivations = ''
    self.theSkills = ''
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

  def resetConceptReferenceAttributes(self):
    self.inDescription = 0
    self.theName = ''
    self.theConcept = ''
    self.theObject = ''
    self.theDescription = ''

  def resetPersonaCharacteristicAttributes(self):
    self.thePersona = ''
    self.theBvName = ''
    self.theModalQualifier = ''
    self.inDefinition = 0
    self.theDefinition = ''
    self.theGrounds = []
    self.theWarrants = []
    self.theRebuttals = []

  def resetTaskCharacteristicAttributes(self):
    self.theTask = ''
    self.theModalQualifier = ''
    self.inDefinition = 0
    self.theDefinition = ''
    self.theGrounds = []
    self.theWarrants = []
    self.theRebuttals = []

  def resetTaskAttributes(self):
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

  def resetUseCaseAttributes(self):
    self.theName = ''
    self.theTags = []
    self.theAuthor = ''
    self.theCode = ''
    self.inDescription = 0
    self.theDescription = ''
    self.theActors = []
    self.theEnvironmentProperties = []
    self.resetUseCaseEnvironmentAttributes()

  def resetUseCaseEnvironmentAttributes(self):
    self.theEnvironmentName = ''    
    self.inPreconditions = 0
    self.thePreconditions = ''
    self.inPostconditions = 0
    self.thePostconditions = ''
    self.theSteps = Steps()
    self.theCurrentStep = None
    self.theCurrentStepNo = 0
    self.theExcName = ''
    self.theExcType = ''
    self.theExcValue = ''
    self.theExcCat = ''
    self.inDefinition = 0
    self.theDefinition = ''

  def startElement(self,name,attrs):
    self.currentElementName = name
    if name == 'persona':
      self.theName = attrs['name']
      self.theType = attrs['type']
      self.theImage = attrs['image']
      if (attrs['assumption_persona'] == 'TRUE'):
        self.isAssumptionPersona = True
    elif name == 'persona_environment':
      self.theEnvironmentName = attrs['name']
      if (attrs['is_direct'] == 'FALSE'):
        self.isDirect = False
    elif name == 'persona_role':
      self.theRoles.append(attrs['name'])
    elif name == 'external_document':
      self.theName = attrs['name']
      self.theVersion = attrs['version']
      self.theDate = attrs['date']
      self.theAuthors = attrs['authors']
    elif name == 'document_reference':
      self.theName = attrs['name']
      self.theContributor = attrs['contributor']
      self.theDocument = attrs['document']
    elif name == 'concept_reference':
      self.theName = attrs['name']
      self.theConcept = attrs['concept']
      self.theObject = attrs['object']
    elif name == 'persona_characteristic':
      self.thePersona = attrs['persona']
      self.theBvName = u2s(attrs['behavioural_variable'])
      self.theModalQualifier = attrs['modal_qualifier'] 
    elif name == 'task_characteristic':
      self.theTask = attrs['task']
      self.theModalQualifier = attrs['modal_qualifier'] 
    elif name == 'grounds':
      refName = attrs['reference']
      refType = attrs['type']
      refArtifact = ''
      self.theGrounds.append((refName,'',refType))
    elif name == 'warrant':
      refName = attrs['reference']
      refType = attrs['type']
      refArtifact = ''
      self.theWarrants.append((refName,'',refType))
    elif name == 'rebuttal':
      refName = attrs['reference']
      refType = attrs['type']
      refArtifact = ''
      self.theRebuttals.append((refName,'',refType))
    elif name == 'task':
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
    elif name == 'usecase':
      self.theName = attrs['name']
      self.theAuthor = attrs['author']
      self.theCode = attrs['code']
    elif name == 'actor':
      self.theActors.append(attrs['name'])
    elif name == 'usecase_environment':
      self.theEnvironmentName = attrs['name']
    elif name == 'step':
      self.theCurrentStepNo = attrs['number']
      self.theCurrentStep = Step(attrs['description'])
    elif name == 'exception':
      self.theExcName = attrs['name']
      self.theExcType = attrs['type']
      self.theExcValue = attrs['value']
      self.theExcCat = u2s(attrs['category'])
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
    elif name == 'preconditions':
      self.inPreconditions = 1
      self.thePreconditions = ''
    elif name == 'postconditions':
      self.inPostconditions = 1
      self.thePostconditions = ''
    elif name == 'tag':
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
    elif self.inNarrative:
      self.theNarrative += data
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
    elif self.inPreconditions:
      self.thePreconditions += data
    elif self.inPostconditions:
      self.thePostconditions += data

  def endElement(self,name):
    if name == 'persona':
      p = PersonaParameters(self.theName,self.theActivities,self.theAttitudes,self.theAptitudes,self.theMotivations,self.theSkills,self.theImage,self.isAssumptionPersona,self.theType,self.theTags,self.theEnvironmentProperties,{})
      self.thePersonas.append(p)
      self.resetPersonaAttributes()
    elif name == 'persona_environment':
      p = PersonaEnvironmentProperties(self.theEnvironmentName,self.isDirect,self.theNarrative,self.theRoles,{'narrative':{}})
      self.theEnvironmentProperties.append(p)
      self.resetPersonaEnvironmentAttributes()
    elif name == 'external_document':
      p = ExternalDocumentParameters(self.theName,self.theVersion,self.theDate,self.theAuthors,self.theDescription)
      self.theExternalDocuments.append(p)
      self.resetExternalDocumentAttributes()
    elif name == 'document_reference':
      p = DocumentReferenceParameters(self.theName,self.theDocument,self.theContributor,self.theExcerpt)
      self.theDocumentReferences.append(p)
      self.resetDocumentReferenceAttributes()
    elif name == 'concept_reference':
      p = ConceptReferenceParameters(self.theName,self.theConcept,self.theObject,self.theDescription)
      self.theConceptReferences.append(p)
      self.resetConceptReferenceAttributes()
    elif name == 'persona_characteristic':
      p = PersonaCharacteristicParameters(self.thePersona,self.theModalQualifier,self.theBvName,self.theDefinition,self.theGrounds,self.theWarrants,[],self.theRebuttals)
      self.thePersonaCharacteristics.append(p)
      self.resetPersonaCharacteristicAttributes()
    elif name == 'task_characteristic':
      p = TaskCharacteristicParameters(self.theTask,self.theModalQualifier,self.theDefinition,self.theGrounds,self.theWarrants,[],self.theRebuttals)
      self.theTaskCharacteristics.append(p)
      self.resetTaskCharacteristicAttributes()
    elif name == 'task':
      p = TaskParameters(self.theName,self.theCode,self.theObjective,self.isAssumptionTask,self.theAuthor,self.theTags,self.theEnvironmentProperties)
      self.theTasks.append(p)
      self.resetTaskAttributes()
    elif name == 'task_environment':
      p = TaskEnvironmentProperties(self.theEnvironmentName,self.theDependencies,self.theTaskPersonas,self.theConcerns,self.theConcernAssociations,self.theNarrative,self.theConsequences,self.theBenefits,{'narrative':{},'consequences':{},'benefits':{}})
      self.theEnvironmentProperties.append(p)
      self.resetTaskEnvironmentAttributes()
    elif name == 'exception':
      self.theCurrentStep.addException((self.theExcName,self.theExcType,self.theExcValue,self.theExcCat,self.theDefinition))
    elif name == 'step':
      self.theSteps.append(self.theCurrentStep)
      self.theCurrentStep = None
    elif name == 'usecase_environment':
      p = UseCaseEnvironmentProperties(self.theEnvironmentName,self.thePreconditions,self.theSteps,self.thePostconditions)
      self.theEnvironmentProperties.append(p)
      self.resetUseCaseEnvironmentAttributes()
    elif name == 'usecase':
      p = UseCaseParameters(self.theName,self.theAuthor,self.theCode,self.theActors,self.theDescription,self.theTags,self.theEnvironmentProperties)
      self.theUseCases.append(p)
      self.resetUseCaseAttributes()
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
    elif name == 'preconditions':
      self.inPreconditions = 0
    elif name == 'postconditions':
      self.inPostconditions = 0
    elif name == 'benefits':
      self.inBenefits = 0
    elif name == 'consequences':
      self.inConsequences = 0

