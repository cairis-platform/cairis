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


from .EnvironmentProperties import EnvironmentProperties

__author__ = 'Shamal Faily'

class ObstacleEnvironmentProperties(EnvironmentProperties):
  def __init__(self,environmentName,lbl='',definition='',category='',gRefs=[], sgRefs=[], concs=[]):
    EnvironmentProperties.__init__(self,environmentName)
    self.theLabel = lbl
    self.theDefinition = definition
    self.theCategory = category
    self.theGoalRefinements = gRefs
    self.theSubGoalRefinements = sgRefs
    self.theConcerns = concs
    self.theProbability = 0.0
    self.theProbabilityRationale = 'None'

  def label(self): return self.theLabel
  def definition(self): return self.theDefinition
  def category(self): return self.theCategory
  def goalRefinements(self): return self.theGoalRefinements
  def subGoalRefinements(self): return self.theSubGoalRefinements
  def concerns(self): return self.theConcerns
  def probability(self): return self.theProbability
  def probabilityRationale(self): return self.theProbabilityRationale

  def setDefinition(self,v): self.theDefinition = v
  def setCategory(self,v): self.theCategory = v
  def setProbability(self,p): self.theProbability = p
  def setProbabilityRationale(self,r): self.theProbabilityRationale = r
