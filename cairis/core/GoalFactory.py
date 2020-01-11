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


from . import Mitigation
from .ARM import *
from .GoalEnvironmentProperties import GoalEnvironmentProperties
from .GoalParameters import GoalParameters
from .Borg import Borg

__author__ = 'Shamal Faily'

def preventDeterText(response,dbProxy):
  genGoalDef = 'Under normal operating conditions, the system shall '
  if (response.type('','None','') == 'Prevent'):
    genGoalDef += 'prevent ' 
    goalCat = 'Prevent'
  else:
    genGoalDef += 'deter ' 
    goalCat = 'Deter'
  genGoalDef += 'an occurrence of ' 
  riskGoalDef = genGoalDef
  thrGoalDef = genGoalDef
  vulGoalDef = genGoalDef
  riskName = response.risk()
  
  if (dbProxy == None):
    b = Borg()
    dbProxy = b.dbProxy
  thrName,vulName = dbProxy.riskComponents(riskName)
  riskGoalDef += 'risk ' + response.risk() + '.'
  thrGoalDef += 'threat ' + thrName + '.'
  vulGoalDef += 'vulnerability ' + vulName + '.'
  riskGoalName = goalCat + response.risk()
  thrGoalName = goalCat + thrName
  vulGoalName = goalCat + vulName
  return [(riskGoalName,riskGoalDef,goalCat),(thrGoalName,thrGoalDef,goalCat),(vulGoalName,vulGoalDef,goalCat)]

def detectText(response,dbProxy):
  goalCategory = 'Detect'
  riskName = response.risk()
  if (dbProxy == None):
    b = Borg()
    dbProxy = b.dbProxy
  thrName,vulName = dbProxy.riskComponents(riskName)
  riskGoalName = goalCategory + riskName
  thrGoalName = goalCategory + thrName
  vulGoalName = goalCategory + vulName
  detPoint = (response.environmentProperties()[0]).detectionPoint()
  riskGoalDef = 'The system shall detect risk ' + riskName
  thrGoalDef = 'The system shall detect threat ' + thrName
  vulGoalDef = 'The system shall detect vulnerability ' + vulName
  if (detPoint == 'Before'): 
    riskGoalDef += ' before '
    thrGoalDef += ' before '
    vulGoalDef += ' before '
  if (detPoint == 'At'): 
    riskGoalDef += ' during '
    thrGoalDef += ' during '
    vulGoalDef += ' during '
  if (detPoint == 'After'): 
    riskGoalDef += ' after '
    thrGoalDef += ' after '
    vulGoalDef += ' after '
  riskGoalDef += 'its occurrence.'
  thrGoalDef += 'its occurrence.'
  vulGoalDef += 'its occurrence.'
  return [(riskGoalName,riskGoalDef,goalCategory),(thrGoalName,thrGoalDef,goalCategory),(vulGoalName,vulGoalDef,goalCategory)]

def reactText(response,dbProxy):
  goalCat = 'React'
  riskName = response.risk()

  if (dbProxy == None):
    b = Borg()
    dbProxy = b.dbProxy
  thrName,vulName = dbProxy.riskComponents(riskName)
 
  riskGoalName = goalCat + riskName
  thrGoalName = goalCat + thrName
  vulGoalName = goalCat + vulName
  detMechs = (response.environmentProperties()[0]).detectionMechanisms()
  riskGoalDef = 'The system shall react to an occurrence of ' + riskName + ' detected by '
  thrGoalDef = 'The system shall react to an occurrence of ' + thrName + ' detected by '
  vulGoalDef = 'The system shall react to an occurrence of ' + vulName + ' detected by '
  if (len(detMechs) == 1):
    riskGoalDef += ' detection mechanism ' + detMechs[0] + '.'
    thrGoalDef += ' detection mechanism ' + detMechs[0] + '.'
    vulGoalDef += ' detection mechanism ' + detMechs[0] + '.'
  else:
    riskGoalDef += ' detection mechanisms '
    thrGoalDef += ' detection mechanisms '
    vulGoalDef += ' detection mechanisms '
    for idx,dm in enumerate(detMechs):
      riskGoalDef += dm
      thrGoalDef += dm
      vulGoalDef += dm
      if (idx != (len(detMechs) - 1)):
        riskGoalDef += ', '
        thrGoalDef += ', '
        vulGoalDef += ', '
  return [(riskGoalName,riskGoalDef,goalCat),(thrGoalName,thrGoalDef,goalCat),(vulGoalName,vulGoalDef,goalCat)]

def transferText(response):
  goalCat = 'Transfer'
  goalName = goalCat + response.risk()
  goalDef = 'The roles of ' + ",".join(response.roleNames('','Maximise','')) + ' shall be accountable for mitigating ' + response.risk() + '.'
  return goalName,goalDef

def mitigateText(response,dbProxy):
  environmentProperties = response.environmentProperties()
  firstResponse = environmentProperties[0]
  firstMitType = firstResponse.type()
  firstDetPoint = firstResponse.detectionPoint()
  firstDetMechs = firstResponse.detectionMechanisms()

  for p in environmentProperties:
    currentType = p.type()
    if (currentType != firstMitType):
      exceptionText = 'Mitigation ' + response.name() + ' does not have the same mitigation type in all of its situated environments.'
      raise ConflictingType(exceptionText)
    elif ((firstMitType == 'Detect') and (firstMitType == 'Detect')):
      if (p.detectionPoint() != firstDetPoint): 
        exceptionText = 'Detection mitigation ' + response.name() + ' needs to detect at the same point in all of its situated environments.'
        raise ConflictingType(exceptionText)
    elif ((firstMitType == 'React') and (firstMitType == 'React')):
      if (p.detectionMechanisms() != firstDetMechs): 
        exceptionText = 'React mitigation ' + response.name() + ' needs to use the same countermeasure in each of its situated environments.'
        raise ConflictingType(exceptionText)
   
  if ((firstMitType == 'Prevent') or (firstMitType == 'Deter')):
    return preventDeterText(response,dbProxy)
  elif (firstMitType == 'Detect'):
    return detectText(response,dbProxy)
  else:
    return reactText(response,dbProxy)
 
def build(response,dbProxy = None):
  goalCategory = response.responseType()
  goalOriginator = 'Response ' + response.name()
  goalPriority = 'Medium'
  goalFitCriterion = 'None'
  goalIssue = 'None'

  if (goalCategory == 'Transfer'):
    goalName,goalDef = transferText(response)
    goalEnvProperties = []
    for p in response.environmentProperties():
      envName = p.name()
      goalEnvProperties.append(GoalEnvironmentProperties(envName,'',goalDef,goalCategory,goalPriority,goalFitCriterion,goalIssue))
    tParameters = GoalParameters(goalName,goalOriginator,[],goalEnvProperties)
    return [tParameters]
  elif (goalCategory != 'Accept'):
    mitText = mitigateText(response,dbProxy)
    riskText = mitText[0]
    riskGoalName= riskText[0]
    riskGoalDef = riskText[1]
    riskGoalCategory = riskText[2] 

    thrText = mitText[1]
    vulText = mitText[2]

    thrGoalName= thrText[0]
    thrGoalDef = thrText[1]
    thrGoalCategory = thrText[2] 
    vulGoalName= vulText[0]
    vulGoalDef = vulText[1]
    vulGoalCategory = vulText[2] 

    riskGoalEnvProperties = []
    thrGoalEnvProperties = []
    vulGoalEnvProperties = []
    environmentProperties = response.environmentProperties()
    for p in environmentProperties:
      envName = p.name()
      riskGoalEnvProperties.append(GoalEnvironmentProperties(envName,'',riskGoalDef,riskGoalCategory,goalPriority,goalFitCriterion,goalIssue))
    riskParameters = GoalParameters(riskGoalName,goalOriginator,[],riskGoalEnvProperties)

    for p in environmentProperties:
      envName = p.name()
      thrGoalRef = [(riskGoalName,'goal','or','No','')]
      thrGoalEnvProperties.append(GoalEnvironmentProperties(envName,'',thrGoalDef,thrGoalCategory,goalPriority,goalFitCriterion,goalIssue,thrGoalRef))
    threatParameters = GoalParameters(thrGoalName,goalOriginator,[],thrGoalEnvProperties)

    for p in environmentProperties:
      envName = p.name()
      vulGoalRef = [(riskGoalName,'goal','or','No','')]
      vulGoalEnvProperties.append(GoalEnvironmentProperties(envName,'',vulGoalDef,vulGoalCategory,goalPriority,goalFitCriterion,goalIssue,vulGoalRef))
    vulnerabilityParameters = GoalParameters(vulGoalName,goalOriginator,[],vulGoalEnvProperties)

    return [riskParameters,threatParameters,vulnerabilityParameters]

