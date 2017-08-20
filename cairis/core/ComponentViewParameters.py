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

class ComponentViewParameters(ObjectCreationParameters.ObjectCreationParameters):
  def __init__(self,cName,cSyn,cmt,cRoles,cAssets,cReqs,cGoals,cCom,cCon,asm = [0,0,0]):
    ObjectCreationParameters.ObjectCreationParameters.__init__(self)
    self.theName = cName
    self.theSynopsis = cSyn
    self.theMetricTypes = cmt
    self.theRoles = cRoles
    self.theAssets = cAssets
    self.theRequirements = cReqs
    self.theGoals = cGoals
    self.theComponents = cCom
    self.theConnectors = cCon
    self.theAttackSurfaceMetric = asm

  def name(self): return self.theName
  def synopsis(self): return self.theSynopsis
  def metricTypes(self): return self.theMetricTypes
  def roles(self): return self.theRoles
  def assets(self): return self.theAssets
  def requirements(self): return self.theRequirements
  def goals(self): return self.theGoals
  def components(self): return self.theComponents
  def connectors(self): return self.theConnectors
  def attackSurfaceMetric(self): return self.theAttackSurfaceMetric
