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

class MisuseCase(ObjectValidator.ObjectValidator):
  def __init__(self,mcId,mcName,cProps,riskName):
    ObjectValidator.ObjectValidator.__init__(self)
    self.theId = mcId
    self.theName = mcName
    self.theEnvironmentProperties = cProps
    self.theRiskName = riskName
    self.theThreatName = ''
    self.theVulnerabilityName = ''
    self.theEnvironmentDictionary = {}
    for p in self.theEnvironmentProperties:
      environmentName = p.name()
      self.theEnvironmentDictionary[environmentName] = p

  def environmentProperties(self): return self.theEnvironmentProperties

  def id(self): return self.theId
  def name(self): return self.theName
  def risk(self): return self.theRiskName
  def threat(self): return self.theThreatName
  def vulnerability(self): return self.theVulnerabilityName

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
