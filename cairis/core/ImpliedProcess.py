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

class ImpliedProcess:
  def __init__(self,ipId,ipName,ipDesc,pName,cNet,ipSpec,chs):
    self.theId = ipId
    self.theName = ipName
    self.theDescription = ipDesc
    self.thePersonaName = pName
    self.theCodeNetwork = cNet
    self.theSpecification = ipSpec
    self.theChannels = chs
  
  def id(self): return self.theId
  def name(self): return self.theName
  def description(self): return self.theDescription
  def persona(self): return self.thePersonaName
  def network(self): return self.theCodeNetwork
  def specification(self): return self.theSpecification
  def channels(self): return self.theChannels

