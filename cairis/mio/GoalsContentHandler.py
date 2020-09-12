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
from cairis.core.DomainPropertyParameters import DomainPropertyParameters
from cairis.core.GoalParameters import GoalParameters
from cairis.core.ObstacleParameters import ObstacleParameters
from cairis.core.CountermeasureParameters import CountermeasureParameters
from cairis.core.GoalEnvironmentProperties import GoalEnvironmentProperties
from cairis.core.ObstacleEnvironmentProperties import ObstacleEnvironmentProperties
from cairis.core.CountermeasureEnvironmentProperties import CountermeasureEnvironmentProperties
from cairis.core.Target import Target
from cairis.core.UseCaseParameters import UseCaseParameters
from cairis.core.UseCaseEnvironmentProperties import UseCaseEnvironmentProperties
from cairis.core.Steps import Steps
from cairis.core.Step import Step
import cairis.core.RequirementFactory
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

def a2i(spLabel):
  if spLabel == 'Low':
    return 1
  elif spLabel == 'Medium':
    return 2
  elif spLabel == 'High':
    return 3
  else:
    return 0

def u2s(aStr):
  outStr = ''
  for c in aStr:
    if (c == '_'):
      outStr += ' '
    else:
      outStr += c
  return outStr
  
class GoalsContentHandler(ContentHandler,EntityResolver):
  def __init__(self,session_id = None):
    b = Borg()
    self.dbProxy = b.get_dbproxy(session_id)
    self.configDir = b.configDir
    self.theDomainProperties = []
    self.theGoals = []
    self.theObstacles = []
    self.theRequirements = []
    self.theUseCases = []
    self.theCountermeasures = []
    self.theReferenceLabelDictionary = {}

    self.resetDomainPropertyAttributes()
    self.resetGoalAttributes()
    self.resetObstacleAttributes()
    self.resetRequirementAttributes()
    self.resetGoalAttributes()
    self.resetUseCaseAttributes()
    self.resetUseCaseEnvironmentAttributes()
    self.resetCountermeasureAttributes()

  def resolveEntity(self,publicId,systemId):
    return systemId

  def roles(self):
    return self.theRoles

  def domainProperties(self):
    return self.theDomainProperties

  def goals(self):
    return self.theGoals

  def obstacles(self):
    return self.theObstacles

  def requirements(self):
    return self.theRequirements

  def usecases(self):
    return self.theUseCases

  def countermeasures(self):
    return self.theCountermeasures

  def resetDomainPropertyAttributes(self):
    self.inDomainProperty = 0
    self.theName = ''
    self.theTags = []
    self.theType = ''
    self.theDefinition = ''
    self.theOriginator = ''

  def resetGoalAttributes(self):
    self.inGoal = 0
    self.theName = ''
    self.theTags = []
    self.theOriginator = ''
    self.theEnvironmentProperties = []
    self.resetGoalEnvironmentAttributes()

  def resetObstacleAttributes(self):
    self.inObstacle = 0
    self.theName = ''
    self.theTags = []
    self.theOriginator = ''
    self.theEnvironmentProperties = []
    self.resetObstacleEnvironmentAttributes()

  def resetGoalEnvironmentAttributes(self):
    self.inDefinition = 0
    self.inFitCriterion = 0
    self.inIssue = 0
    self.theEnvironmentName = ''
    self.theCategory = ''
    self.thePriority = ''
    self.theDefinition = ''
    self.theConcerns = []
    self.theConcernAssociations = []

  def resetObstacleEnvironmentAttributes(self):
    self.inDefinition = 0
    self.theEnvironmentName = ''
    self.theCategory = ''
    self.theDefinition = ''
    self.theConcerns = []
    self.resetProbabilityElements()

  def resetProbabilityElements(self):
    self.theProbability = 0.0
    self.inRationale = 0
    self.theRationale = ''

  def resetRequirementAttributes(self):
    self.inDescription = 0
    self.inRationale = 0
    self.inFitCriterion = 0
    self.inOriginator = 0
    self.theReference = ''
    self.theReferenceType = ''
    self.theLabel = 0
    self.theName = ''
    self.theType = ''
    self.thePriority = 0
    self.theDescription = 0
    self.theRationale = 0
    self.theFitCriterion = 0
    self.theOriginator = 0

  def resetUseCaseAttributes(self):
    self.inUseCase = 0
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
    self.theCognitiveAttribute = {}
    self.theCognitiveAttribute['vigilance'] = (0,'None')
    self.theCognitiveAttribute['situation awareness'] = (0,'None')
    self.theCognitiveAttribute['stress'] = (0,'None')
    self.theCognitiveAttribute['workload'] = (0,'None')
    self.theCognitiveAttribute['risk awareness'] = (0,'None')
    
  def resetCountermeasureAttributes(self):
    self.theName = ''
    self.theType = ''
    self.inDescription = 0
    self.theDescription = ''
    self.theEnvironmentProperties = []
    self.resetCountermeasureEnvironmentAttributes()

  def resetCountermeasureEnvironmentAttributes(self):
    self.theEnvironmentName = ''
    self.theCost = ''
    self.theCmRequirements = []
    self.theTargets = []
    self.theCmRoles = []
    self.theTaskPersonas = []
    self.theSpDict = {}
    self.theSpDict['confidentiality'] = (0,'None')
    self.theSpDict['integrity'] = (0,'None')
    self.theSpDict['availability'] = (0,'None')
    self.theSpDict['accountability'] = (0,'None')
    self.theSpDict['anonymity'] = (0,'None')
    self.theSpDict['pseudonymity'] = (0,'None')
    self.theSpDict['unlinkability'] = (0,'None')
    self.theSpDict['unobservability'] = (0,'None')
    self.theTargetName = ''
    self.theTargetEffectiveness = ''
    self.theTargetResponses = []
    self.resetMitigatingPropertyAttributes()

  def resetMitigatingPropertyAttributes(self):
    self.thePropertyName = ''
    self.thePropertyValue = 'None'
    self.inRationale = 0
    self.theRationale = ''

  def startElement(self,name,attrs):
    self.currentElementName = name
    if name == 'domainproperty':
      self.inDomainProperty = 1
      self.theName = attrs['name']
      self.theType = attrs['type']
      self.theOriginator = attrs['originator']
    elif name == 'goal':
      self.inGoal = 1
      self.theName = attrs['name']
      self.theOriginator = attrs['originator']
    elif name == 'obstacle':
      self.inObstacle = 1
      self.theName = attrs['name']
      self.theOriginator = attrs['originator']
    elif name == 'goal_environment':
      self.theEnvironmentName = attrs['name']
      self.theCategory = attrs['category']
      self.thePriority = attrs['priority']
    elif name == 'obstacle_environment':
      self.theEnvironmentName = attrs['name']
      self.theCategory = u2s(attrs['category'])
    elif name == 'probability':
      self.theProbability = attrs['value']
    elif name == 'rationale':
      self.inRationale = 1
      self.theRationale = ''
    elif name == 'concern':
      self.theConcerns.append(attrs['name'])
    elif name == 'concern_association':
      self.theConcernAssociations.append((attrs['source_name'],a2s(attrs['source_nry']),attrs['link_name'],attrs['target_name'],a2s(attrs['target_nry'])))
    elif name == 'requirement':
      self.theReference = attrs['reference']
      if (self.theReference in self.theReferenceLabelDictionary):
        self.theReferenceLabelDictionary[self.theReference] += 1
      else:
        self.theReferenceLabelDictionary[self.theReference] = 1
      self.theLabel = self.theReferenceLabelDictionary[self.theReference]

      try:
        self.theName = attrs['name']
      except KeyError:
        self.theName = ''
      self.theReferenceType = attrs['reference_type']
      self.theType = u2s(attrs['type'])
      self.thePriority = attrs['priority']
    elif name == 'usecase':
      self.inUseCase = 1
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
      if (self.theExcType == 'None'):
        self.theExcValue = 'None'
        self.theExcCat = 'None'
      else: 
        try: 
          self.theExcValue = attrs['value']
          self.theExcCat = u2s(attrs['category'])
        except KeyError:
          raise ARMException('Exception ' + self.theExcName + ' has a goal or requirement exception type but no related goal/requirement name or exception category')
    elif name == 'countermeasure':
      self.theName = attrs['name']
      self.theType = attrs['type']
    elif name == 'countermeasure_environment':
      self.theEnvironmentName = attrs['name']
      self.theCost = attrs['cost']
    elif name == 'countermeasure_requirement':
      self.theCmRequirements.append(attrs['name'])
    elif name == 'target':
      self.theTargetName = attrs['name']
      self.theTargetEffectiveness = attrs['effectiveness']
    elif name == 'target_response':
      self.theTargetResponses.append(attrs['name'])
    elif name == 'mitigating_property':
      self.thePropertyName = attrs['name']
      self.thePropertyValue = a2i(attrs['value'])
    elif name == 'responsible_role':
      self.theCmRoles.append(attrs['name'])
    elif name == 'responsible_persona':
      self.theTaskPersonas.append((attrs['task'],attrs['persona'],u2s(attrs['duration']),u2s(attrs['frequency']),u2s(attrs['demands']),u2s(attrs['goals'])))
    elif (name == 'description'):
      self.inDescription = 1
      self.theDescription = ''
    elif (name =='definition'):
      self.inDefinition = 1
      self.theDefinition = ''
    elif name == 'fit_criterion':
      self.inFitCriterion = 1
      self.theFitCriterion = ''
    elif name == 'issue':
      self.inIssue = 1
      self.theIssue = ''
    elif name == 'rationale':
      self.inRationale = 1
      self.theRationale = ''
    elif name == 'originator':
      self.inOriginator = 1
      self.theOriginator = ''
    elif name == 'preconditions':
      self.inPreconditions = 1
      self.thePreconditions = ''
    elif name == 'postconditions':
      self.inPostconditions = 1
      self.thePostconditions = ''
    elif name == 'tag':
      if ((self.inDomainProperty == 1) or (self.inGoal == 1) or (self.inObstacle == 1) or (self.inUseCase == 1)):
        self.theTags.append(attrs['name'])

  def characters(self,data):
    if self.inDescription:
      self.theDescription += data
    if self.inDefinition:
      self.theDefinition += data
    elif self.inFitCriterion:
      self.theFitCriterion += data
    elif self.inIssue:
      self.theIssue += data
    elif self.inRationale:
      self.theRationale += data
    elif self.inOriginator:
      self.theOriginator += data
    elif self.inPreconditions:
      self.thePreconditions += data
    elif self.inPostconditions:
      self.thePostconditions += data


  def endElement(self,name):
    if name == 'domainproperty':
      p = DomainPropertyParameters(unescape(self.theName),unescape(self.theDefinition),self.theType,unescape(self.theOriginator),self.theTags)
      self.theDomainProperties.append(p)
      self.resetDomainPropertyAttributes()
    elif name == 'goal_environment':
      p = GoalEnvironmentProperties(self.theEnvironmentName,'',unescape(self.theDefinition),self.theCategory,self.thePriority,unescape(self.theFitCriterion),unescape(self.theIssue),[],[],self.theConcerns,self.theConcernAssociations)
      self.theEnvironmentProperties.append(p)
      self.resetGoalEnvironmentAttributes()
    elif name == 'obstacle_environment':
      p = ObstacleEnvironmentProperties(self.theEnvironmentName,'',unescape(self.theDefinition),self.theCategory,[],[],self.theConcerns)
      p.theProbability = self.theProbability
      p.theProbabilityRationale = unescape(self.theRationale)
      self.theEnvironmentProperties.append(p)
      self.resetObstacleEnvironmentAttributes()
    elif name == 'goal':
      p = GoalParameters(unescape(self.theName),unescape(self.theOriginator),self.theTags,self.theEnvironmentProperties)
      self.theGoals.append(p)
      self.resetGoalAttributes()
    elif name == 'obstacle':
      p = ObstacleParameters(unescape(self.theName),unescape(self.theOriginator),self.theTags,self.theEnvironmentProperties)
      self.theObstacles.append(p)
      self.resetObstacleAttributes()
    elif name == 'requirement':
      reqId = self.dbProxy.newId()
      r = cairis.core.RequirementFactory.build(reqId,self.theLabel,unescape(self.theName),unescape(self.theDescription),self.thePriority,unescape(self.theRationale),unescape(self.theFitCriterion),unescape(self.theOriginator),self.theType,self.theReference)
      self.theRequirements.append((r,self.theReference,self.theReferenceType))
      self.resetRequirementAttributes()
    elif name == 'exception':
      self.theCurrentStep.addException((self.theExcName,self.theExcType.lower(),self.theExcValue,self.theExcCat,unescape(self.theDefinition)))
    elif name == 'step':
      self.theCurrentStep.setTags(self.theTags)
      self.theSteps.append(self.theCurrentStep)
      self.theCurrentStep = None
    elif name == 'usecase_environment':
      vProperty,vRationale = self.theCognitiveAttribute['vigilance']
      saProperty,saRationale = self.theCognitiveAttribute['situation awareness']
      sProperty,sRationale = self.theCognitiveAttribute['stress']
      wProperty,wRationale = self.theCognitiveAttribute['workload']
      raProperty,raRationale = self.theCognitiveAttribute['risk awareness']
      p = UseCaseEnvironmentProperties(self.theEnvironmentName,unescape(self.thePreconditions),self.theSteps,unescape(self.thePostconditions),[vProperty,saProperty,sProperty,wProperty,raProperty],[vRationale,saRationale,sRationale,wRationale,raRationale])
      self.theEnvironmentProperties.append(p)
      self.resetUseCaseEnvironmentAttributes()
    elif name == 'usecase':
      p = UseCaseParameters(self.theName,self.theAuthor,unescape(self.theCode),self.theActors,unescape(self.theDescription),self.theTags,self.theEnvironmentProperties)
      self.theUseCases.append(p)
      self.resetUseCaseAttributes()
    elif name == 'countermeasure':
      p = CountermeasureParameters(self.theName,unescape(self.theDescription),self.theType,self.theTags,self.theEnvironmentProperties)
      self.theCountermeasures.append(p)
      self.resetCountermeasureAttributes()
    elif name == 'mitigating_property':
      self.theSpDict[self.thePropertyName] = (self.thePropertyValue,unescape(self.theDescription))
      self.resetMitigatingPropertyAttributes()
    elif name == 'countermeasure_environment':
      cProperty,cRationale = self.theSpDict['confidentiality']
      iProperty,iRationale = self.theSpDict['integrity']
      avProperty,avRationale = self.theSpDict['availability']
      acProperty,acRationale = self.theSpDict['accountability']
      anProperty,anRationale = self.theSpDict['anonymity']
      panProperty,panRationale = self.theSpDict['pseudonymity']
      unlProperty,unlRationale = self.theSpDict['unlinkability']
      unoProperty,unoRationale = self.theSpDict['unobservability']
      p = CountermeasureEnvironmentProperties(self.theEnvironmentName,self.theCmRequirements,self.theTargets,[cProperty,iProperty,avProperty,acProperty,anProperty,panProperty,unlProperty,unoProperty],[cRationale,iRationale,avRationale,acRationale,anRationale,panRationale,unlRationale,unoRationale],self.theCost,self.theCmRoles,self.theTaskPersonas)
      self.theEnvironmentProperties.append(p)
      self.resetCountermeasureEnvironmentAttributes()
    elif (name == 'target'):
      self.theTargets.append(Target(self.theTargetName,self.theTargetEffectiveness,unescape(self.theRationale)))
      self.theTargetResponses = []
    elif (name == 'description'):
      self.inDescription = 0
    elif (name =='definition'):
      self.inDefinition = 0
    elif name == 'fit_criterion':
      self.inFitCriterion = 0
    elif name == 'issue':
      self.inIssue = 0
    elif name == 'rationale':
      self.inRationale = 0
    elif name == 'originator':
      self.inOriginator = 0
    elif name == 'preconditions':
      self.inPreconditions = 0
    elif name == 'postconditions':
      self.inPostconditions = 0
