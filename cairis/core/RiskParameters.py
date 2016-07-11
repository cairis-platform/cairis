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


import ObjectCreationParameters

class RiskParameters(ObjectCreationParameters.ObjectCreationParameters):
  def __init__(self,riskName,threatName,vulName,mc,rTags,inTxt = '',envName = ''):
    ObjectCreationParameters.ObjectCreationParameters.__init__(self)
    self.theRiskName = riskName
    self.theThreatName = threatName
    self.theVulnerabilityName = vulName
    self.theMisuseCase = mc
    self.theTags = rTags
    self.theIntent = inTxt
    self.theEnvironmentName = envName

  def name(self): return self.theRiskName
  def threat(self): return self.theThreatName
  def vulnerability(self): return self.theVulnerabilityName
  def misuseCase(self): return self.theMisuseCase
  def tags(self): return self.theTags
  def intent(self): return self.theIntent
  def environment(self): return self.theEnvironmentName
