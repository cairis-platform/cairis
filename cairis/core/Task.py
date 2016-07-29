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

__author__ = 'Shamal Faily'

class Task:
  def __init__(self,tId,tName,tShortCode,tObjt,isAssumption,tAuth,tags,cProps):
    self.theId = tId
    self.theName = tName
    self.theShortCode = tShortCode
    self.theObjective = tObjt
    self.isAssumption = isAssumption
    self.theAuthor = tAuth
    self.theTags = tags
    self.theEnvironmentProperties = cProps
    self.theEnvironmentDictionary = {}
    for p in self.theEnvironmentProperties:
      environmentName = p.name()
      self.theEnvironmentDictionary[environmentName] = p
    self.scoreLookup = {}
    self.scoreLookup['None'] = 0
    self.scoreLookup['Low'] = 1
    self.scoreLookup['Medium'] = 2
    self.scoreLookup['High'] = 3

  def environmentProperties(self): return self.theEnvironmentProperties

  def id(self): return self.theId
  def name(self): return self.theName
  def shortCode(self): return self.theShortCode
  def objective(self): return self.theObjective
  def assumption(self): return self.isAssumption
  def author(self): return self.theAuthor
  def tags(self): return self.theTags

  def dependencies(self,environmentName,dupProperty):
    if (dupProperty == ''):
      return (self.theEnvironmentDictionary[environmentName]).dependencies()
    else:
      workingDependencies = ''
      noOfEnvironments = len(self.theEnvironmentProperties)
      for p in self.theEnvironmentProperties:
        environmentName = p.name()
        workingDependencies += p.dependencies()
        if (noOfEnvironments > 1):
          workingDependencies += ' [' + environmentName + '].  '
      return workingDependencies

  def narrative(self,environmentName,dupProperty): 
    if (dupProperty == ''):
      return (self.theEnvironmentDictionary[environmentName]).narrative()
    else:
      workingNarrative = ''
      noOfEnvironments = len(self.theEnvironmentProperties)
      for p in self.theEnvironmentProperties:
        environmentName = p.name()
        workingNarrative += p.narrative()
        if (noOfEnvironments > 1):
          workingNarrative += ' [' + environmentName + '].  '
      return workingNarrative

  def assets(self,environmentName,dupProperty):
    if (dupProperty == ''):
      return (self.theEnvironmentDictionary[environmentName]).assets()
    else:
      mergedAssets = []
      for p in self.theEnvironmentProperties:
        mergedAssets += p.assets()
      return set(mergedAssets)

  def personas(self,environmentName,dupProperty,overridingEnvironment):
    if (dupProperty == ''):
      return (self.theEnvironmentDictionary[environmentName]).personas()
    else:
      mergedPersonas = []
      taskPersonas = []
      for p in self.theEnvironmentProperties:
        environmentName = p.name()
        for persona in p.personas():
          if (dupProperty == 'Override'):
            if (p.name() != overridingEnvironment):
              continue
            else:
              mergedPersonas.append((persona[0] + '[' + p.name() + ']',persona[1],persona[2],persona[3],persona[4]))
          else:
            taskPersonas.append((persona[0] + '[' + p.name() + ']',persona[1],persona[2],persona[3],persona[4]))
            mergedPersonas += taskPersonas
            taskPersonas = []
      return set(mergedPersonas)

  def personaUsability(self,pScore):
    duration = self.scoreLookup[pScore[1]]
    frequency = self.scoreLookup[pScore[2]]
    demands = self.scoreLookup[pScore[3]]
    goalSupport = self.scoreLookup[pScore[4]]
    efficiencyScore = (duration + frequency) / 2
    usabilityScore = goalSupport + efficiencyScore + demands
    return usabilityScore

  def usability(self,environmentName,dupProperty):
    if (dupProperty == ''):
      return self.personaUsability(((self.theEnvironmentDictionary[environmentName]).personas())[0])
