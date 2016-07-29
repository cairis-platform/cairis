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


class WeaknessTarget:
  def __init__(self,targetName):
    self.theTargetName = targetName
    self.theComponents = set([])
    self.theTemplateAssets = set([])
    self.theAssets = set([])
    self.theTreatmentRequirement = ''
    self.theTreatmentAsset = ''
    self.theTreatmentEffectiveness = 'None'
    self.theTreatmentRationale = ''

  def name(self): return self.theTargetName
  def components(self): return self.theComponents
  def templateAssets(self): return self.theTemplateAssets
  def assets(self): return self.theAssets

  def addComponent(self,cName): self.theComponents.add(cName)
  def addAsset(self,aName): self.theAssets.add(aName)
  def addTemplateAsset(self,taName): 
    self.theTemplateAssets.add(taName)

  def addTreatment(self,reqName,assetName,effValue,effRationale):
    self.theTreatmentRequirement = reqName
    self.theTreatmentAsset = assetName
    self.theTreatmentEffectiveness = effValue
    self.theTreatmentRationale = effRationale

  def requirement(self): return self.theTreatmentRequirement
  def asset(self): return self.theTreatmentAsset
  def effectiveness(self): return self.theTreatmentEffectiveness
  def rationale(self): return self.theTreatmentRationale
