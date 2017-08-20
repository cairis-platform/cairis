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

class DomainPropertyParameters(ObjectCreationParameters):
  def __init__(self,name,desc,dpType,dpOrig,tags):
    ObjectCreationParameters.__init__(self)
    self.theName = name
    self.theTags = tags
    self.theDescription = desc
    self.theType = dpType
    self.theOriginator = dpOrig

  def name(self): return self.theName
  def tags(self): return self.theTags
  def description(self): return self.theDescription
  def type(self): return self.theType
  def originator(self): return self.theOriginator
