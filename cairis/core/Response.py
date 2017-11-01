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

from . import ObjectValidator

class Response(ObjectValidator.ObjectValidator):
  def __init__(self,respId,respName,respRisk,tags,cProps,respType):
    ObjectValidator.ObjectValidator.__init__(self)
    self.theId = respId
    self.theName = respName
    self.theTags = tags
    self.theRisk = respRisk
    self.theEnvironmentProperties = cProps
    self.theResponseType = respType
    self.theEnvironmentDictionary = {}
    for p in self.theEnvironmentProperties:
      environmentName = p.name()
      self.theEnvironmentDictionary[environmentName] = p
    self.costLookup = {}
    self.costLookup['Low'] = 0
    self.costLookup['Medium'] = 1
    self.costLookup['High'] = 2


  def id(self): return self.theId
  def name(self): return self.theName
  def tags(self): return self.theTags
  def risk(self): return self.theRisk
  def environmentProperties(self): return self.theEnvironmentProperties
  def responseType(self): return self.theResponseType

  def roles(self,environmentName,dupProperty,overridingEnvironment):
    if (self.theResponseType != 'Transfer'):
      return []

    if (dupProperty == ''):
      return (self.theEnvironmentDictionary[environmentName]).roles()
    else:
      roleDictionary = {}
      for p in self.theEnvironmentProperties:
        environmentName = p.name()
        for role,cost in p.roles():
          if (role in roleDictionary):
            if (dupProperty == 'Override'):
              if (environmentName != overridingEnvironment):
                continue
              else:
                roleDictionary[role] = cost
            else:
              if (self.costLookup[cost] > self.costLookup[(roleDictionary[role])]):
                roleDictionary[role] = cost
          else:
            roleDictionary[role] = (role,cost)
      return list(roleDictionary.values())

  def roleNames(self,environmentName,dupProperty,overridingEnvironment):
    if (self.theResponseType != 'Transfer'):
      return []

    if (dupProperty == ''):
      return (self.theEnvironmentDictionary[environmentName]).roles()
    else:
      roleDictionary = {}
      for p in self.theEnvironmentProperties:
        environmentName = p.name()
        for role,cost in p.roles():
          if (role in roleDictionary):
            if (dupProperty == 'Override'):
              if (environmentName != overridingEnvironment):
                continue
              else:
                roleDictionary[role] = cost
            else:
              if (self.costLookup[cost] > self.costLookup[(roleDictionary[role])]):
                roleDictionary[role] = cost
          else:
            roleDictionary[role] = (role,cost)
      return list(roleDictionary.keys())


  def cost(self,environmentName,dupProperty,overridingEnvironment):
    if (self.theResponseType != 'Accept'):
      return ''

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

  def description(self,environmentName,dupProperty,overridingEnvironment):
    if (self.theResponseType == 'Mitigate') :
      return ''
    if (dupProperty == ''):
      return (self.theEnvironmentDictionary[environmentName]).description()
    else:
      workingDescription = ''
      noOfEnvironments = len(self.theEnvironmentProperties)
      for p in self.theEnvironmentProperties:
        environmentName = p.name()
        workingDescription += p.description()
        if (noOfEnvironments > 1):
          workingDescription += ' [' + environmentName + '].  '
      return workingDescription

  def detectionPoint(self,environmentName,dupProperty,overridingEnvironment):
    if (self.theResponseType != 'Mitigate') :
      return ''
    if (dupProperty == ''):
      return (self.theEnvironmentDictionary[environmentName]).detectionPoint()
    else:
      workingDetPt = ''
      noOfEnvironments = len(self.theEnvironmentProperties)
      for p in self.theEnvironmentProperties:
        environmentName = p.name()
        workingDetPt += p.detectionPoint()
        if (noOfEnvironments > 1):
          workingDetPt += ' [' + environmentName + '].  '
      return workingDetPt


  def detectionMechanisms(self,environmentName,dupProperty,overridingEnvironment):
    if (self.theResponseType != 'Mitigate'):
      return ''

    if (dupProperty == ''):
      return (self.theEnvironmentDictionary[environmentName]).detectionMechanisms()
    else:
      workingDms = []
      for p in self.theEnvironmentProperties:
        environmentName = p.name()
        currentDms = p.detectionMechanisms()
        if (dupProperty == 'Override'):
          if (environmentName != overridingEnvironment):
            continue
          else:
            workingDms = currentDms
        else:
          workingDms += currentDms
      return workingDms

  def type(self,environmentName,dupProperty,overridingEnvironment):
    if (self.theResponseType != 'Mitigate'):
      return ''
    if (dupProperty == ''):
      return (self.theEnvironmentDictionary[environmentName]).type()
    else:
      return (self.theEnvironmentProperties[0]).type()
