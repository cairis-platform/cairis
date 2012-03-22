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


#$URL $Id: Domain.py 249 2010-05-30 17:07:31Z shaf $

class Domain:
  def __init__(self,rmId,modName,shortCode,modDesc,domType,giveInd,domains):
    self.theId = rmId
    self.theModuleName = modName
    self.theShortCode = shortCode
    self.theDescription = modDesc
    self.theType = domType
    self.isGiven = giveInd
    self.theDomains = domains

  def id(self): return self.theId
  def name(self): return self.theModuleName
  def shortCode(self): return self.theShortCode
  def description(self): return self.theDescription
  def type(self): return self.theType
  def given(self): return self.isGiven
  def domains(self): return self.theDomains
