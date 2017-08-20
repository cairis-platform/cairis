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

from . import ObjectCreationParameters

class TaskParameters(ObjectCreationParameters.ObjectCreationParameters):
  def __init__(self,tName,tSName,tObjt,isAssumption,tAuth,tags,cProps):
    ObjectCreationParameters.ObjectCreationParameters.__init__(self)
    self.theName = tName
    self.theTags = tags
    self.theShortCode = tSName
    self.theObjective = tObjt
    self.isAssumption = isAssumption
    self.theAuthor = tAuth
    self.theEnvironmentProperties = cProps

  def name(self): return self.theName
  def tags(self): return self.theTags
  def shortCode(self): return self.theShortCode
  def objective(self): return self.theObjective
  def assumption(self): return self.isAssumption
  def author(self): return self.theAuthor
  def environmentProperties(self): return self.theEnvironmentProperties
