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


#$URL$ $Id: UseCase.py 530 2011-11-16 19:29:16Z shaf $

class UseCase:
  def __init__(self,ucId,ucName,ucAuth,ucCode,ucActors,ucDesc,tags,cProps):
    self.theId = ucId
    self.theName = ucName
    self.theTags = tags
    self.theAuthor = ucAuth
    self.theCode = ucCode
    self.theActors = ucActors
    self.theDescription = ucDesc
    self.theEnvironmentProperties = cProps
    self.theEnvironmentDictionary = {}
    for p in self.theEnvironmentProperties:
      environmentName = p.name()
      self.theEnvironmentDictionary[environmentName] = p

  def environmentProperties(self): return self.theEnvironmentProperties

  def id(self): return self.theId
  def name(self): return self.theName
  def tags(self): return self.theTags
  def author(self): return self.theAuthor
  def code(self): return self.theCode
  def actors(self): return self.theActors
  def description(self): return self.theDescription

  def steps(self,environmentName,dupProperty = ''):
    return (self.theEnvironmentDictionary[environmentName]).steps()

  def preconditions(self,environmentName,dupProperty = ''):
    return (self.theEnvironmentDictionary[environmentName]).preconditions()

  def postconditions(self,environmentName,dupProperty = ''):
    return (self.theEnvironmentDictionary[environmentName]).postconditions()
