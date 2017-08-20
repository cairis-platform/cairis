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

class AssetParameters(ObjectCreationParameters.ObjectCreationParameters):
  def __init__(self,assetName,shortCode,assetDesc,assetSig,assetType,cFlag,cRationale,tags,ifs,cProperties):
    ObjectCreationParameters.ObjectCreationParameters.__init__(self)
    self.theName = assetName
    self.theShortCode = shortCode
    self.theDescription = assetDesc
    self.theSignificance = assetSig
    self.theEnvironmentProperties = cProperties
    self.theType = assetType
    self.isCritical = cFlag
    self.theCriticalRationale = cRationale
    self.theTags = tags
    self.theInterfaces = ifs

  def name(self): return self.theName
  def shortCode(self): return self.theShortCode
  def description(self): return self.theDescription
  def significance(self): return self.theSignificance
  def type(self): return self.theType
  def environmentProperties(self): return self.theEnvironmentProperties
  def critical(self): return self.isCritical
  def criticalRationale(self): return self.theCriticalRationale
  def tags(self): return self.theTags
  def interfaces(self): return self.theInterfaces
