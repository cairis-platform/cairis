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

from .AttackerEnvironmentProperties import AttackerEnvironmentProperties
from . import ObjectValidator

class Attacker(ObjectValidator.ObjectValidator):
  def __init__(self,attackerId,attackerName,attackerDescription,attackerImage,tags,environmentProperties):
    ObjectValidator.ObjectValidator.__init__(self)
    self.theId = attackerId
    self.theName = attackerName
    self.theDescription = attackerDescription
    self.theImage = attackerImage
    self.theTags = tags
    self.theEnvironmentProperties = environmentProperties
    self.theEnvironmentDictionary = {}
    for p in self.theEnvironmentProperties:
      environmentName = p.name()
      self.theEnvironmentDictionary[environmentName] = p
    self.isPersona = False

  def id(self): return self.theId
  def name(self): return self.theName
  def description(self): return self.theDescription 
  def image(self): return self.theImage
  def tags(self): return self.theTags
  def environmentProperties(self): return self.theEnvironmentProperties
  def persona(self): return self.isPersona

  def roles(self,environmentName,dupProperty): 
    if (dupProperty == ''):
      return (self.theEnvironmentDictionary[environmentName]).roles()
    else:
      mergedRoles = []
      for p in self.theEnvironmentProperties:
        mergedRoles += p.roles()
      return set(mergedRoles)

  def motives(self,environmentName,dupProperty): 
    if (dupProperty == ''):
      return (self.theEnvironmentDictionary[environmentName]).motives()
    else:
      mergedMotives = []
      for p in self.theEnvironmentProperties:
        mergedMotives += p.motives()
      return set(mergedMotives)

  def capability(self,environmentName,dupProperty): 
    if (dupProperty == ''):
      return (self.theEnvironmentDictionary[environmentName]).capabilities()
    else:
      mergedCapability = []
      for p in self.theEnvironmentProperties:
        mergedCapability += p.capabilities()
      return set(mergedCapability)
