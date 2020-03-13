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


from .ObstacleEnvironmentProperties import ObstacleEnvironmentProperties
from . import ObjectValidator

__author__ = 'Shamal Faily'

class Obstacle(ObjectValidator.ObjectValidator):
  def __init__(self,obsId,obsName,obsOrig,tags,environmentProperties):
    ObjectValidator.ObjectValidator.__init__(self)
    self.theId = obsId
    self.theName = obsName
    self.theTags = tags
    self.theOriginator = obsOrig
    self.theEnvironmentProperties = environmentProperties
    self.theEnvironmentDictionary = {}
    for p in environmentProperties:
      environmentName = p.name()
      self.theEnvironmentDictionary[environmentName] = p

  def id(self): return self.theId
  def setId(self,v): self.theId = v
  def name(self): return self.theName
  def tags(self): return self.theTags
  def originator(self): return self.theOriginator
  def environmentProperties(self): return self.theEnvironmentProperties
  def environmentProperty(self,envName): return self.theEnvironmentDictionary[envName]

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

  def setName(self, v):
    self.theName = v

  def setOriginator(self, v):
    self.theOriginator = v

  def setDefinition(self,environmentName,v):
    (self.theEnvironmentDictionary[environmentName]).setDefinition(v)

  def setCategory(self,environmentName,v):
    (self.theEnvironmentDictionary[environmentName]).setCategory(v)

  def refinements(self,environmentName):
    for assoc in ((self.theEnvironmentDictionary[environmentName]).subGoalRefinements()):
      if assoc[1] == 'obstacle':
        return True
    return False

