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

from . import ObjectValidator

class ClassAssociation(ObjectValidator.ObjectValidator):
  def __init__(self,associationId,envName,headName,headDim,headNav,headType,headMultiplicity,headRole,tailRole,tailMultiplicity,tailType,tailNav,tailDim,tailName,rationale=''):
    ObjectValidator.ObjectValidator.__init__(self)
    self.theId = associationId
    self.theEnvironmentName = envName
    self.theHeadAsset = headName
    self.theHeadType = headType
    self.theHeadDim = headDim
    self.theHeadNavigation = headNav
    self.theHeadMultiplicity = headMultiplicity
    self.theHeadRole = headRole
    self.theTailRole = tailRole
    self.theTailMultiplicity = tailMultiplicity
    self.theTailType = tailType
    self.theTailNavigation = tailNav
    self.theTailDim = tailDim
    self.theTailAsset = tailName
    self.theRationale = rationale

  def id(self): return self.theId
  def environment(self): return self.theEnvironmentName
  def headAsset(self): return self.theHeadAsset
  def headDimension(self): return self.theHeadDim
  def headNavigation(self): return self.theHeadNavigation
  def headType(self): return self.theHeadType
  def headMultiplicity(self): return self.theHeadMultiplicity
  def headRole(self): return self.theHeadRole
  def tailRole(self): return self.theTailRole
  def tailMultiplicity(self): return self.theTailMultiplicity
  def tailType(self): return self.theTailType
  def tailNavigation(self): return self.theTailNavigation
  def tailDimension(self): return self.theTailDim
  def tailAsset(self): return self.theTailAsset
  def rationale(self): return self.theRationale
  def name(self): return self.theEnvironmentName + ' / ' + self.theHeadAsset + ' / ' + self.theTailAsset
