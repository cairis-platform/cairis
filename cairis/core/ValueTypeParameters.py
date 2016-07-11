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

class ValueTypeParameters(ObjectCreationParameters.ObjectCreationParameters):
  def __init__(self,vtName,vtDesc,vType,envName = '',vtScore = -1,vtRat = ''):
    ObjectCreationParameters.ObjectCreationParameters.__init__(self)
    self.theName = vtName
    self.theDescription = vtDesc
    self.theType = vType
    self.theEnvironmentName = envName
    self.theScore = vtScore
    self.theRationale = vtRat

  def name(self): return self.theName
  def description(self): return self.theDescription
  def type(self): return self.theType
  def environment(self): return self.theEnvironmentName
  def score(self): return self.theScore
  def rationale(self): return self.theRationale
