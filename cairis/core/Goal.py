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

from . import ObjectValidator
from .GoalEnvironmentProperties import GoalEnvironmentProperties

__author__ = 'Shamal Faily'

class Goal(ObjectValidator.ObjectValidator):
  def __init__(self,goalId,goalName,goalOrig,tags,environmentProperties):
    ObjectValidator.ObjectValidator.__init__(self)
    self.theId = goalId
    self.theName = goalName
    self.theTags = tags
    self.theOriginator = goalOrig
    self.theColour = 'black'
    self.theEnvironmentProperties = environmentProperties
    self.theEnvironmentDictionary = {}
    for p in self.theEnvironmentProperties:
      environmentName = p.name()
      self.theEnvironmentDictionary[environmentName] = p

  def id(self): return self.theId
  def setId(self,v): self.theId = v
  def name(self): return self.theName
  def tags(self): return self.theTags
  def originator(self): return self.theOriginator
  def environmentProperties(self): return self.theEnvironmentProperties
  def environmentProperty(self,envName): return self.theEnvironmentDictionary[envName]
  def setColour(self,c): self.theColour = c
  def colour(self): return self.theColour

  def label(self,environmentName):
    return (self.theEnvironmentDictionary[environmentName]).label()

  def definition(self,environmentName,dupProperty=''):
    if (dupProperty == ''):
      return (self.theEnvironmentDictionary[environmentName]).definition()
    else:
      workingAttr = ''
      noOfEnvironments = len(self.theEnvironmentProperties)
      for p in self.theEnvironmentProperties:
        environmentName = p.name()
        workingAttr += p.definition()
        if (noOfEnvironments > 1):
          workingAttr += ' [' + environmentName + '].  '
      return workingAttr

  def category(self,environmentName,dupProperty=''):
    if (dupProperty == ''):
      return (self.theEnvironmentDictionary[environmentName]).category()
    else:
      workingAttr = ''
      noOfEnvironments = len(self.theEnvironmentProperties)
      for p in self.theEnvironmentProperties:
        environmentName = p.name()
        workingAttr += p.category()
        if (noOfEnvironments > 1):
          workingAttr += ' [' + environmentName + '].  '
      return workingAttr

  def priority(self,environmentName,dupProperty=''):
    if (dupProperty == ''):
      return (self.theEnvironmentDictionary[environmentName]).priority()
    else:
      workingAttr = ''
      noOfEnvironments = len(self.theEnvironmentProperties)
      for p in self.theEnvironmentProperties:
        environmentName = p.name()
        workingAttr += p.priority()
        if (noOfEnvironments > 1):
          workingAttr += ' [' + environmentName + '].  '
      return workingAttr

  def fitCriterion(self,environmentName,dupProperty=''):
    if (dupProperty == ''):
      return (self.theEnvironmentDictionary[environmentName]).fitCriterion()
    else:
      workingAttr = ''
      noOfEnvironments = len(self.theEnvironmentProperties)
      for p in self.theEnvironmentProperties:
        environmentName = p.name()
        workingAttr += p.fitCriterion()
        if (noOfEnvironments > 1):
          workingAttr += ' [' + environmentName + '].  '
      return workingAttr

  def issue(self,environmentName,dupProperty=''):
    if (dupProperty == ''):
      return (self.theEnvironmentDictionary[environmentName]).issue()
    else:
      workingAttr = ''
      noOfEnvironments = len(self.theEnvironmentProperties)
      for p in self.theEnvironmentProperties:
        environmentName = p.name()
        workingAttr += p.issue()
        if (noOfEnvironments > 1):
          workingAttr += ' [' + environmentName + '].  '
      return workingAttr

  def setName(self, v): self.theName = v

  def setOriginator(self, v):  self.theOriginator = v

  def setDefinition(self,environmentName,v):  (self.theEnvironmentDictionary[environmentName]).setDefinition(v)

  def setCategory(self,environmentName,v):  (self.theEnvironmentDictionary[environmentName]).setCategory(v)

  def setPriority(self,environmentName,v):  (self.theEnvironmentDictionary[environmentName]).setPriority(v)

  def setFitCriterion(self,environmentName,v):  (self.theEnvironmentDictionary[environmentName]).setFitCriterion(v)

  def setIssue(self,environmentName,v):  (self.theEnvironmentDictionary[environmentName]).setIssue(v)

  def refinements(self,environmentName):
    for assoc in ((self.theEnvironmentDictionary[environmentName]).subGoalRefinements()):
      if assoc[1] == 'goal':
        return True
    return False
