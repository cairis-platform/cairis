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

from .EnvironmentProperties import EnvironmentProperties

class TaskEnvironmentProperties(EnvironmentProperties):
  def __init__(self,environmentName,deps = '',personas = [],assets = [],concs=[],narrative = '',consequences = '', benefits = '',contribs=[],tCodes={'narrative':{},'benefits':{},'consequences':{}}):
    EnvironmentProperties.__init__(self,environmentName)
    self.thePersonas = personas
    self.theAssets = assets
    self.theDependencies = deps
    self.theNarrative = narrative
    self.theConsequences = consequences
    self.theBenefits = benefits
    self.theConcernAssociations = concs
    self.theContributions = contribs
    self.theCodes = tCodes

  def personas(self): return self.thePersonas
  def assets(self): return self.theAssets
  def narrative(self): return self.theNarrative
  def consequences(self): return self.theConsequences
  def benefits(self): return self.theBenefits
  def dependencies(self): return self.theDependencies
  def concernAssociations(self): return self.theConcernAssociations
  def contributions(self): return self.theContributions
  def codes(self,sectName = ''): 
    if sectName == '': return self.theCodes
    else: return self.theCodes[sectName]
