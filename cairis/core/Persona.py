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

class Persona:
  def __init__(self,personaId,personaName,pActivities,pAttitudes,pAptitudes,pMotivations,pSkills,pIntrinsic,pContextual,image,isAssumption,pType,tags,environmentProperties,pCodes):
    self.theId = personaId
    self.theName = personaName
    self.theTags = tags
    self.theActivities = pActivities
    self.theAttitudes = pAttitudes
    self.theAptitudes = pAptitudes
    self.theMotivations = pMotivations
    self.theSkills = pSkills
    self.theIntrinsic = pIntrinsic
    self.theContextual = pContextual
    self.theImage = image
    self.isAssumption = isAssumption
    self.thePersonaType = pType
    self.theEnvironmentProperties = environmentProperties
    self.theEnvironmentDictionary = {}
    for p in self.theEnvironmentProperties:
      environmentName = p.name()
      self.theEnvironmentDictionary[environmentName] = p
    self.theCodes = pCodes

  def id(self): return self.theId
  def name(self): return self.theName
  def tags(self): return self.theTags
  def activities(self): return self.theActivities
  def attitudes(self): return self.theAttitudes
  def aptitudes(self): return self.theAptitudes
  def motivations(self): return self.theMotivations
  def skills(self): return self.theSkills
  def intrinsic(self): return self.theIntrinsic
  def contextual(self): return self.theContextual
  def image(self): return self.theImage
  def assumption(self): return self.isAssumption
  def type(self): return self.thePersonaType
  def environmentProperties(self): return self.theEnvironmentProperties
  def codes(self,sectName): return self.theCodes[sectName]

  def narrative(self,environmentName,dupProperty):
    if (dupProperty == ''):
      return (self.theEnvironmentDictionary[environmentName]).narrative()
    else:
      workingDescription = ''
      noOfEnvironments = len(self.theEnvironmentProperties)
      for p in self.theEnvironmentProperties:
        environmentName = p.name()
        workingDescription += p.narrative()
        if (noOfEnvironments > 1):
          workingDescription += ' [' + environmentName + '].  '
      return workingDescription

  def directFlag(self,environmentName,dupProperty): 
    if (dupProperty == ''):
      return str((self.theEnvironmentDictionary[environmentName]).directFlag())
    else:
      workingDirect = ''
      noOfEnvironments = len(self.theEnvironmentProperties)
      for p in self.theEnvironmentProperties:
        environmentName = p.name()
        workingDirect += p.directFlag()
        if (noOfEnvironments > 1):
          workingDirect += ' [' + environmentName + '].  '
      return workingDirect


  def roles(self,environmentName,dupProperty):
    if (dupProperty == ''):
      return (self.theEnvironmentDictionary[environmentName]).roles()
    else:
      mergedRoles = []
      for p in self.theEnvironmentProperties:
        mergedRoles += p.roles()
      return set(mergedRoles)
