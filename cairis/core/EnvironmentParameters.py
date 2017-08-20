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


from .ObjectCreationParameters import ObjectCreationParameters

__author__ = 'Shamal Faily'

class EnvironmentParameters(ObjectCreationParameters):
  def __init__(self,conName,conSc,conDesc,environments = [],duplProperty = 'None',overridingEnvironment = '', envTensions = None):
    ObjectCreationParameters.__init__(self)
    self.theName = conName
    self.theShortCode = conSc
    self.theDescription = conDesc
    self.theEnvironments = environments
    self.theDuplicateProperty = duplProperty 
    self.theOverridingEnvironment = overridingEnvironment
    self.theAssetValues = None
    if (envTensions == None):
      self.theTensions = {}
      defaultTension = (0,'None')
      idx = 0
      while idx < 4:
        iidx = 4
        while iidx < 8:
          self.theTensions[(idx,iidx)] = defaultTension
          iidx += 1
        idx += 1
    else:
      self.theTensions = envTensions

  def setAssetValues(self,avs):
    self.theAssetValues = avs

  def name(self): return self.theName
  def shortCode(self): return self.theShortCode
  def description(self): return self.theDescription
  def environments(self): return self.theEnvironments
  def duplicateProperty(self): return self.theDuplicateProperty
  def overridingEnvironment(self): return self.theOverridingEnvironment
  def assetValues(self): return self.theAssetValues
  def tensions(self): return self.theTensions
