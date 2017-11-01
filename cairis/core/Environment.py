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

from . import ObjectValidator

__author__ = 'Shamal Faily'

class Environment(ObjectValidator.ObjectValidator):
  def __init__(self,id,name,sc,description,environments,duplProperty,overridingEnvironment,envTensions):
    ObjectValidator.ObjectValidator.__init__(self)
    self.theId = id
    self.theName = name
    self.theShortCode = sc
    self.theDescription = description
    self.theEnvironments = environments
    self.theDuplicateProperty = duplProperty
    self.theOverridingEnvironment = overridingEnvironment
    self.theTensions = envTensions

  def id(self): return self.theId
  def name(self): return self.theName
  def shortCode(self): return self.theShortCode
  def description(self): return self.theDescription
  def environments(self): return self.theEnvironments
  def duplicateProperty(self): return self.theDuplicateProperty
  def overridingEnvironment(self): return self.theOverridingEnvironment
  def tensions(self): return self.theTensions

  def __str__(self): return 'id: ' + str(self.theId) + ', name: ' + self.theName + ', short code:' + self.theShortCode + ', description: ' + self.theDescription + ', environments: ' + str(self.theEnvironments) + ', dupProperty: ' + self.theDuplicateProperty + ', overridingEnv: ' + self.theOverridingEnvironment
