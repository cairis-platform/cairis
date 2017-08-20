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

class CodeParameters(ObjectCreationParameters):
  def __init__(self,codeName,cType,codeDesc,incCriteria,codeEg):
    ObjectCreationParameters.__init__(self)
    self.theName = codeName
    self.theType = cType
    self.theDescription = codeDesc
    self.theInclusionCriteria = incCriteria
    self.theExample = codeEg

  def name(self): return self.theName
  def type(self): return self.theType
  def description(self): return self.theDescription
  def inclusionCriteria(self): return self.theInclusionCriteria
  def example(self): return self.theExample
