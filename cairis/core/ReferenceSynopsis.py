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

class ReferenceSynopsis:
  def __init__(self,rsId,refName,synName,dimName,aType,aName,synDim = 'document_reference',initialSatisfaction = 'None',goals=[]):
    self.theId = rsId
    self.theReference = refName
    self.theSynopsis = synName
    self.theDimension = dimName
    self.theActorType = aType
    self.theActor = aName
    self.theSynopsisDimension = synDim
    self.theInitialSatisfaction = initialSatisfaction
    self.theRelatedGoals = goals

  def id(self): return self.theId
  def setId(self,newId): self.theId = newId
  def reference(self): return self.theReference
  def synopsis(self): return self.theSynopsis
  def dimension(self): return self.theDimension
  def actorType(self): return self.theActorType
  def actor(self): return self.theActor 
  def synopsisDimension(self): return self.theSynopsisDimension
  def satisfaction(self): return self.theInitialSatisfaction
  def goals(self): return self.theRelatedGoals
  def name(self): return self.theSynopsis
