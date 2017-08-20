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

class ClassAssociationParameters(ObjectCreationParameters.ObjectCreationParameters):
  def __init__(self,envName,headName,headDim,headNav,headType,headMultiplicity,headRole,tailRole,tailMultiplicity,tailType,tailNav,tailDim,tailName,rationale = ''):
    ObjectCreationParameters.ObjectCreationParameters.__init__(self)
    self.theEnvironmentName = envName
    self.theHeadAsset = headName
    self.theHeadDim = headDim
    self.theHeadNav = headNav
    self.theHeadType = headType
    self.theHeadMultiplicity = headMultiplicity
    self.theHeadRole = headRole
    self.theTailRole = tailRole
    self.theTailMultiplicity = tailMultiplicity
    self.theTailType = tailType
    self.theTailNav = tailNav
    self.theTailDim = tailDim
    self.theTailAsset = tailName
    self.theRationale = rationale

  def environment(self): return self.theEnvironmentName
  def headAsset(self): return self.theHeadAsset
  def headDimension(self): return self.theHeadDim
  def headNavigation(self): return self.theHeadNav
  def headType(self): return self.theHeadType
  def headMultiplicity(self): return self.theHeadMultiplicity
  def headRole(self): return self.theHeadRole
  def tailRole(self): return self.theTailRole
  def tailMultiplicity(self): return self.theTailMultiplicity
  def tailType(self): return self.theTailType
  def tailNavigation(self): return self.theTailNav
  def tailDimension(self): return self.theTailDim
  def tailAsset(self): return self.theTailAsset
  def rationale(self): return self.theRationale
