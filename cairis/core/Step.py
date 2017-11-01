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

from . import ObjectValidator

__author__ = 'Shamal Faily'

class Step(ObjectValidator.ObjectValidator):
  def __init__(self,stepTxt = '',stepSyn = '',stepActor = '',stepActorType = '',stepTags = []):
    ObjectValidator.ObjectValidator.__init__(self)
    self.theExceptions = {}
    self.theStepText = stepTxt
    self.theSynopsis = stepSyn
    self.theActor = stepActor
    self.theActorType = stepActorType
    self.theTags = stepTags

  def synopsis(self): return self.theSynopsis

  def actor(self): return self.theActor

  def actorType(self): return self.theActorType

  def tags(self): return self.theTags

  def setSynopsis(self,s): self.theSynopsis = s

  def setActor(self,a): self.theActor = a

  def setActorType(self,at): self.theActorType = at

  def setTags(self,t): self.theTags = t

  def __str__(self): return self.theStepText

  def addException(self,exc): self.theExceptions[exc[0]] = exc

  def deleteException(self,excName): del self.theExceptions[excName]
    
  def text(self): return self.theStepText

  def setText(self,txt): self.theStepText = txt

  def exceptions(self):
    if len(self.theExceptions) > 0:
      return list(self.theExceptions.keys())
    else:
      return []

  def exception(self,excName): return self.theExceptions[excName]

  def setException(self,oldExcName,exc):
    del self.theExceptions[oldExcName] 
    self.theExceptions[exc[0]] = exc
