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

class Role(ObjectValidator.ObjectValidator):
  def __init__(self,roleId,roleName,rType,sCode,roleDesc,cProps):
    ObjectValidator.ObjectValidator.__init__(self)
    self.theId = roleId
    self.theName = roleName
    self.theType = rType
    self.theShortCode = sCode
    self.theDescription = roleDesc
    self.theEnvironmentProperties = cProps
    self.theEnvironmentDictionary = {}
    for p in self.theEnvironmentProperties:
      environmentName = p.name()
      self.theEnvironmentDictionary[environmentName] = p
    self.costLookup = {}
    self.costLookup['Low'] = 0
    self.costLookup['Medium'] = 1
    self.costLookup['High'] = 2


  def environmentProperties(self): return self.theEnvironmentProperties

  def id(self): return self.theId
  def name(self): return self.theName
  def type(self): return self.theType
  def shortCode(self): return self.theShortCode
  def description(self): return self.theDescription

  def responses(self,environmentName,dupProperty,overridingEnvironment): 
    if (len(self.theEnvironmentProperties) == 0):
      return []
    if (dupProperty == ''):
      return (self.theEnvironmentDictionary[environmentName]).responses()
    else:
      responseDictionary = {}
      for p in self.theEnvironmentProperties:
        environmentName = p.name()
        for response,cost in p.responses():
          if (response in responseDictionary):
            if (dupProperty == 'Override'):
              if (environmentName != overridingEnvironment):
                continue
              else:
                responseDictionary[response] = cost
            else:
              workingCost = responseDictionary[response]
              if (self.costLookup[cost] > self.costLookup[workingCost]):
                responseDictionary[response] = cost
          else:
            responseDictionary[response] = cost
      responseList = []
      for responseName in responseDictionary:
        responseList.append((responseName,responseDictionary[responseName]))
      return responseList

  def countermeasures(self,environmentName,dupProperty,overridingEnvironment): 
    if (len(self.theEnvironmentProperties) == 0):
      return []
    if (dupProperty == ''):
      return (self.theEnvironmentDictionary[environmentName]).countermeasures()
    else:
      cmDictionary = {}
      for p in self.theEnvironmentProperties:
        environmentName = p.name()
        for cm in p.countermeasures():
          if (cm in cmDictionary):
            if (dupProperty == 'Override'):
              if (environmentName != overridingEnvironment):
                continue
              else:
                cmDictionary[cm] = cost
            else:
              workingCost = cmDictionary[cm]
              if (self.costLookup[cost] > self.costLookup[workingCost]):
                cmDictionary[cm] = cost
          else:
            cmDictionary[cm] = cost
      cmList = []
      for cmName in cmDictionary:
        cmList.append((cmName,cmDictionary[cmName]))
      return cmList
