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
import cairis.core.RequirementFactory
from cairis.core.Borg import Borg

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
  def __init__(self):
    b = Borg()
    self.dbProxy = b.dbProxy
    self.configDir = b.configDir
    self.theDomainProperties = []
    self.theGoals = []
    self.theObstacles = []
    self.theRequirements = []
    self.theCountermeasures = []

    self.resetDomainPropertyAttributes()
    self.resetGoalAttributes()
    self.resetObstacleAttributes()
    self.resetRequirementAttributes()
    self.resetGoalAttributes()
    self.resetCountermeasureAttributes()

  def resolveEntity(self,publicId,systemId):
    return self.configDir + '/goals.dtd'

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

  def countermeasures(self):
    return self.theCountermeasures

  def resetDomainPropertyAttributes(self):
    self.theName = ''
    self.theTags = []
    self.theType = ''
    self.theDescription = ''
    self.theOriginator = ''

  def resetGoalAttributes(self):
    self.theName = ''
    self.theTags = []
    self.theOriginator = ''
    self.theEnvironmentProperties = []
    self.resetGoalEnvironmentAttributes()

  def resetObstacleAttributes(self):
    self.theName = ''
    self.theTags = []
    self.theOriginator = ''
    self.theEnvironmentProperties = []
    self.resetObstacleEnvironmentAttributes()

  def resetGoalEnvironmentAttributes(self):
    self.inDescription = 0
    self.inFitCriterion = 0
    self.inIssue = 0
    self.theEnvironmentName = ''
    self.theCategory = ''
    self.thePriority = ''
    self.theDescription = ''
    self.theConcerns = []
    self.theConcernAssociations = []

  def resetObstacleEnvironmentAttributes(self):
    self.inDescription = 0
    self.theEnvironmentName = ''
    self.theCategory = ''
    self.theDescription = ''
    self.theConcerns = []

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
      self.theName = attrs['name']
      self.theType = attrs['type']
      self.theOriginator = attrs['originator']
    elif name == 'goal':
      self.theName = attrs['name']
      self.theOriginator = attrs['originator']
    elif name == 'obstacle':
      self.theName = attrs['name']
      self.theOriginator = attrs['originator']
    elif name == 'goal_environment':
      self.theEnvironmentName = attrs['name']
      self.theCategory = attrs['category']
      self.thePriority = attrs['priority']
    elif name == 'obstacle_environment':
      self.theEnvironmentName = attrs['name']
      self.theCategory = u2s(attrs['category'])
    elif name == 'concern':
      self.theConcerns.append(attrs['name'])
    elif name == 'concern_association':
      self.theConcernAssociations.append((attrs['source_name'],a2s(attrs['source_nry']),attrs['link_name'],attrs['target_name'],a2s(attrs['target_nry'])))
    elif name == 'requirement':
      self.theReference = attrs['reference']
      try:
        self.theName = attrs['name']
      except KeyError:
        self.theName = ''
      self.theReferenceType = attrs['reference_type']
      self.theLabel = attrs['label']
      self.theType = u2s(attrs['type'])
      self.thePriority = attrs['priority']
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
      self.inDescription = 1
      self.theDescription = ''
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
    elif name == 'tag':
      self.theTags.append(attrs['name'])

  def characters(self,data):
    if self.inDescription:
      self.theDescription += data
    elif self.inFitCriterion:
      self.theFitCriterion += data
    elif self.inIssue:
      self.theIssue += data
    elif self.inRationale:
      self.theRationale += data
    elif self.inOriginator:
      self.theOriginator += data

  def endElement(self,name):
    if name == 'domainproperty':
      p = DomainPropertyParameters(self.theName,self.theDescription,self.theType,self.theOriginator,self.theTags)
      self.theDomainProperties.append(p)
      self.resetDomainPropertyAttributes()
    elif name == 'goal_environment':
      p = GoalEnvironmentProperties(self.theEnvironmentName,'',self.theDescription,self.theCategory,self.thePriority,self.theFitCriterion,self.theIssue,[],[],self.theConcerns,self.theConcernAssociations)
      self.theEnvironmentProperties.append(p)
      self.resetGoalEnvironmentAttributes()
    elif name == 'obstacle_environment':
      p = ObstacleEnvironmentProperties(self.theEnvironmentName,'',self.theDescription,self.theCategory,[],[],self.theConcerns)
      self.theEnvironmentProperties.append(p)
      self.resetObstacleEnvironmentAttributes()
    elif name == 'goal':
      p = GoalParameters(self.theName,self.theOriginator,self.theTags,self.theEnvironmentProperties)
      self.theGoals.append(p)
      self.resetGoalAttributes()
    elif name == 'obstacle':
      p = ObstacleParameters(self.theName,self.theOriginator,self.theTags,self.theEnvironmentProperties)
      self.theObstacles.append(p)
      self.resetObstacleAttributes()
    elif name == 'requirement':
      reqId = self.dbProxy.newId()
      r = cairis.core.RequirementFactory.build(reqId,self.theLabel,self.theName,self.theDescription,self.thePriority,self.theRationale,self.theFitCriterion,self.theOriginator,self.theType,self.theReference)
      self.theRequirements.append((r,self.theReference,self.theReferenceType))
      self.resetRequirementAttributes()
    elif name == 'countermeasure':
      p = CountermeasureParameters(self.theName,self.theDescription,self.theType,self.theTags,self.theEnvironmentProperties)
      self.theCountermeasures.append(p)
      self.resetCountermeasureAttributes()
    elif name == 'mitigating_property':
      self.theSpDict[self.thePropertyName] = (self.thePropertyValue,self.theDescription)
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
      self.theTargets.append(Target(self.theTargetName,self.theTargetEffectiveness,self.theRationale))
      self.theTargetResponses = []
    elif (name == 'description'):
      self.inDescription = 0
    elif (name =='definition'):
      self.inDescription = 0
    elif name == 'fit_criterion':
      self.inFitCriterion = 0
    elif name == 'issue':
      self.inIssue = 0
    elif name == 'rationale':
      self.inRationale = 0
    elif name == 'originator':
      self.inOriginator = 0
