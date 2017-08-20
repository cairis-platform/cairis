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


from . import ObjectCreationParameters

__author__ = 'Shamal Faily'

class PersonaParameters(ObjectCreationParameters.ObjectCreationParameters):
  def __init__(self,name,activities,attitudes,aptitudes,motivations,skills,intrinsic,contextual,image,isAssumption,pType,tags,properties,pCodes):
    ObjectCreationParameters.ObjectCreationParameters.__init__(self)
    self.theName = name
    self.theTags = tags
    self.theActivities = activities
    self.theAttitudes = attitudes
    self.theAptitudes = aptitudes
    self.theMotivations = motivations
    self.theSkills = skills
    self.theIntrinsic = intrinsic
    self.theContextual = contextual
    self.theImage = image
    self.isAssumption = isAssumption
    self.thePersonaType = pType
    self.theEnvironmentProperties = properties
    self.theCodes = pCodes

  def name(self): return self.theName
  def tags(self): return self.theTags
  def attitudes(self): return self.theAttitudes
  def activities(self): return self.theActivities
  def aptitudes(self): return self.theAptitudes
  def motivations(self): return self.theMotivations
  def skills(self): return self.theSkills
  def intrinsic(self): return self.theIntrinsic
  def contextual(self): return self.theContextual
  def image(self): return self.theImage
  def assumption(self): return self.isAssumption
  def type(self): return self.thePersonaType
  def environmentProperties(self): return self.theEnvironmentProperties
  def codes(self): return self.theCodes
