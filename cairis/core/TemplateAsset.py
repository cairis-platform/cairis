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

class TemplateAsset:
  def __init__(self,assetId,assetName,shortCode,assetDescription,assetSig,assetType,sType,aRight,spValues,spRat,tags,ifs):
    self.theId = assetId
    self.theName = assetName
    self.theShortCode = shortCode
    self.theDescription = assetDescription
    self.theSignificance = assetSig
    self.theType = assetType
    self.theSurfaceType = sType
    self.theAccessRight = aRight
    self.theProperties = spValues
    self.theRationale = spRat
    self.theTags = tags
    self.theInterfaces = ifs

  def id(self): return self.theId
  def name(self): return self.theName
  def properties(self): return self.theProperties
  def rationale(self): return self.theRationale
  def shortCode(self): return self.theShortCode
  def description(self): return self.theDescription
  def significance(self): return self.theSignificance
  def type(self): return self.theType
  def surfaceType(self): return self.theSurfaceType
  def accessRight(self): return self.theAccessRight

  def confidentialityProperty(self): return self.theProperties[0]
  def confidentialityRationale(self): return self.theRationale[0]
  def integrityProperty(self): return self.theProperties[1]
  def integrityRationale(self): return self.theRationale[1]
  def availabilityProperty(self): return self.theProperties[2]
  def availabilityRationale(self): return self.theRationale[2]
  def accountabilityProperty(self): return self.theProperties[3]
  def accountabilityRationale(self): return self.theRationale[3]
  def anonymityProperty(self): return self.theProperties[4]
  def anonymityRationale(self): return self.theRationale[4]
  def pseudonymityProperty(self): return self.theProperties[5]
  def pseudonymityRationale(self): return self.theRationale[5]
  def unlinkabilityProperty(self): return self.theProperties[6]
  def unlinkabilityRationale(self): return self.theRationale[6]
  def unobservabilityProperty(self): return self.theProperties[7]
  def unobservabilityRationale(self): return self.theRationale[7]

  def interfaces(self): return self.theInterfaces
  def tags(self): return self.theTags
  def securityProperties(self): return self.properties()
