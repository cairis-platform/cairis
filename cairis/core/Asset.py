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
from .PropertyHolder import PropertyHolder;
from numpy import *

class Asset(ObjectValidator.ObjectValidator):
  def __init__(self,assetId,assetName,shortCode,assetDescription,assetSig,assetType,cFlag,cRationale,tags,ifs,cProps):
    ObjectValidator.ObjectValidator.__init__(self)
    self.theId = assetId
    self.theName = assetName
    self.theShortCode = shortCode
    self.theDescription = assetDescription
    self.theSignificance = assetSig
    self.theType = assetType
    self.isCritical = cFlag
    self.theCriticalRationale = cRationale
    self.theTags = tags
    self.theInterfaces = ifs
    self.theEnvironmentProperties = cProps
    self.theEnvironmentDictionary = {}
    self.theAssetPropertyDictionary = {}
    for p in self.theEnvironmentProperties:
      environmentName = p.name()
      self.theEnvironmentDictionary[environmentName] = p
      self.theAssetPropertyDictionary[environmentName] = PropertyHolder(p.properties(),p.rationale())

  def securityProperties(self,environmentName,dupProperty='',overridingEnvironment=''):
    try:
      return (self.theAssetPropertyDictionary[environmentName]).properties()
    except KeyError:
      workingProperties = array((0,0,0,0,0,0,0,0))
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
      return workingProperties
      

  def id(self): return self.theId
  def name(self): return self.theName
  def shortCode(self): return self.theShortCode
  def description(self): return self.theDescription
  def significance(self): return self.theSignificance
  def type(self): return self.theType
  def tags(self): return self.theTags
  def interfaces(self): return self.theInterfaces
  def critical(self): return self.isCritical
  def criticalRationale(self): return self.theCriticalRationale
  def environmentProperties(self): return self.theEnvironmentProperties
  def propertyList(self,environmentName,dupProperty,overridingEnvironment): 
    if (len(dupProperty) == 0):
      return (self.theAssetPropertyDictionary[environmentName]).propertyList()
    else:
      workingProperties = array((0,0,0,0,0,0,0,0))
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
