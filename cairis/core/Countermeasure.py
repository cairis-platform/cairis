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


from .PropertyHolder import PropertyHolder;
from numpy import *
from . import ObjectValidator

__author__ = 'Shamal Faily'

class Countermeasure(ObjectValidator.ObjectValidator):
  def __init__(self,cmId,cmName,cmDesc,cmType,tags,cProps):
    ObjectValidator.ObjectValidator.__init__(self)
    self.theId = cmId
    self.theName = cmName
    self.theTags = tags
    self.theDescription = cmDesc
    self.theType = cmType
    self.theEnvironmentProperties = cProps
    self.theEnvironmentDictionary = {}
    self.theCountermeasurePropertyDictionary = {}
    for p in self.theEnvironmentProperties:
      environmentName = p.name()
      self.theEnvironmentDictionary[environmentName] = p
      self.theCountermeasurePropertyDictionary[environmentName] = PropertyHolder(p.properties(),p.rationale())
    self.costLookup = {}
    self.costLookup['Low'] = 0
    self.costLookup['Medium'] = 1
    self.costLookup['High'] = 2
    self.effectivenessLookup = {}
    self.effectivenessLookup['Low'] = 1
    self.effectivenessLookup['Medium'] = 2
    self.effectivenessLookup['High'] = 3


  def id(self): return self.theId
  def name(self): return self.theName
  def tags(self): return self.theTags
  def type(self): return self.theType
  def description(self): return self.theDescription
  def environmentProperties(self): return self.theEnvironmentProperties

  def requirements(self,environmentName,dupProperty,overridingEnvironment):
    if (len(dupProperty) == 0):
      return (self.theEnvironmentDictionary[environmentName]).requirements()
    else:
      workingReqs = []
      for p in self.theEnvironmentProperties:
        environmentName = p.name()
        currentReqs = p.requirements()
        if (dupProperty == 'Override'):
          if (environmentName != overridingEnvironment):
            continue
          else:
            workingReqs = currentReqs
        else:
          workingReqs += currentReqs
      return set(workingReqs)

  def targets(self,environmentName,dupProperty,overridingEnvironment):
    if (len(dupProperty) == 0):
      return (self.theEnvironmentDictionary[environmentName]).targets()
    else:
      workingTargets = {}
      for p in self.theEnvironmentProperties:
        environmentName = p.name()
        currentTargets = p.targets()
        if (dupProperty == 'Override'):
          if (environmentName != overridingEnvironment):
            continue
          else:
            return currentTargets 
        else:
          for t in currentTargets:
            currentTargetName = t.name()
            if currentTargetName in workingTargets:
              if (self.effectivenessLookup[t.effectiveness()] > self.effectivenessLookup[ (workingTargets[currentTargetName]).effectiveness() ]):
                workingTargets[currentTargetName] = t
            else:
              workingTargets[currentTargetName] = t
      return list(workingTargets.values())

  def propertyList(self,environmentName,dupProperty,overridingEnvironment):
    if (len(dupProperty) == 0):
      return (self.theCountermeasurePropertyDictionary[environmentName]).propertyList()
    else:
      workingProperties = array((0,0,0,0))
      for p in self.theEnvironmentProperties:
        environmentName = p.name()
        currentEnvironmentProperties = p.properties()
        for idx,value in enumerate(currentEnvironmentProperties):
          if (workingProperties[idx] == 0 and value != 0):
            workingProperties[idx] = value
          elif (value != 0):
            if (dupProperty == 'Override'):
              if (environmentName != overridingEnvironment):
                continue
              else:
                workingProperties[idx] = value
            else:
              if (value > workingProperties[idx]):
                workingProperties[idx] = value
      return PropertyHolder(workingProperties).propertyList()

  def cost(self,environmentName,dupProperty,overridingEnvironment):
    if (dupProperty == ''):
      return (self.theEnvironmentDictionary[environmentName]).cost()
    else:
      workingCost = 'Low'
      for p in self.theEnvironmentProperties:
        environmentName = p.name()
        currentCost = p.cost()
        if (dupProperty == 'Override'):
          if (environmentName != overridingEnvironment):
            continue
          else:
            workingCost = currentCost
        else:
          if (self.costLookup[currentCost] > self.costLookup[workingCost]):
            workingCost = currentCost
      return workingCost

  def roles(self,environmentName,dupProperty,overridingEnvironment):
    if (dupProperty == ''):
      return (self.theEnvironmentDictionary[environmentName]).roles()
    else:
      roleList = []
      for p in self.theEnvironmentProperties:
        environmentName = p.name()
        for role in p.roles():
          if (dupProperty == 'Override'):
            if (environmentName != overridingEnvironment):
              continue
            else:
              roleList.append(role)
          else:
            roleList.append(role)
      return set(roleList)

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
              mergedPersonas.append((persona[0] + '[' + p.name() + ']',persona[1],persona[2],persona[3],persona[4],persona[5]))
          else:
            taskPersonas.append((persona[0] + '[' + p.name() + ']',persona[1],persona[2],persona[3],persona[4],persona[5]))
            mergedPersonas += taskPersonas
            taskPersonas = []
      return set(mergedPersonas)

  def environments(self):
    return list(self.theEnvironmentDictionary.keys())
