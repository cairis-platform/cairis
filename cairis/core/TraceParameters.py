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

class TraceParameters(ObjectCreationParameters.ObjectCreationParameters):
  def __init__(self,fromObjt,fromName,toObjt,toName):
    ObjectCreationParameters.ObjectCreationParameters.__init__(self)
    self.theFromObject = fromObjt
    self.theFromName = fromName
    self.theToObject = toObjt
    self.theToName = toName

  def fromObject(self): return self.theFromObject
  def fromName(self): return self.theFromName
  def toObject(self): return self.theToObject
  def toName(self): return self.theToName
