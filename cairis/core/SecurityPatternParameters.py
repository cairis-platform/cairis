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

class SecurityPatternParameters(ObjectCreationParameters.ObjectCreationParameters):
  def __init__(self,spName,spContext,spProb,spSol,spReqs,spAssocs):
    ObjectCreationParameters.ObjectCreationParameters.__init__(self)
    self.theName = spName
    self.theContext = spContext
    self.theProblem = spProb
    self.theSolution = spSol
    self.theRequirements = spReqs
    self.theConcernAssociations = spAssocs

  def id(self): return self.theId
  def name(self): return self.theName
  def context(self): return self.theContext
  def problem(self): return self.theProblem
  def solution(self): return self.theSolution
  def requirements(self): return self.theRequirements
  def associations(self): return self.theConcernAssociations
