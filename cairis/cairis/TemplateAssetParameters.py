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


import ObjectCreationParameters

class TemplateAssetParameters(ObjectCreationParameters.ObjectCreationParameters):
  def __init__(self,assetName,shortCode,assetDesc,assetSig,assetType,sType,aRight,spValues,tags,ifs):
    ObjectCreationParameters.ObjectCreationParameters.__init__(self)
    self.theName = assetName
    self.theShortCode = shortCode
    self.theDescription = assetDesc
    self.theSignificance = assetSig
    self.theProperties = spValues
    self.theConfidentialityProperty = spValues[0][0]
    self.theConfidentialityRationale = spValues[0][1]
    self.theIntegrityProperty = spValues[1][0]
    self.theIntegrityRationale = spValues[1][1]
    self.theAvailabilityProperty = spValues[2][0]
    self.theAvailabilityRationale = spValues[2][1]
    self.theAccountabilityProperty = spValues[3][0]
    self.theAccountabilityRationale = spValues[3][1]
    self.theAnonymityProperty = spValues[4][0]
    self.theAnonymityRationale = spValues[4][1]
    self.thePseudonymityProperty = spValues[5][0]
    self.thePseudonymityRationale = spValues[5][1]
    self.theUnlinkabilityProperty = spValues[6][0]
    self.theUnlinkabilityRationale = spValues[6][1]
    self.theUnobservabilityProperty = spValues[7][0]
    self.theUnobservabilityRationale = spValues[7][1]
    self.theType = assetType
    self.theSurfaceType = sType
    self.theAccessRight = aRight
    self.theTags = tags
    self.theInterfaces = ifs

  def name(self): return self.theName
  def properties(self): return self.theProperties
  def shortCode(self): return self.theShortCode
  def description(self): return self.theDescription
  def significance(self): return self.theSignificance
  def type(self): return self.theType
  def surfaceType(self): return self.theSurfaceType
  def accessRight(self): return self.theAccessRight
  def confidentialityProperty(self): return self.theConfidentialityProperty
  def confidentialityRationale(self): return self.theConfidentialityRationale
  def integrityProperty(self): return self.theIntegrityProperty
  def integrityRationale(self): return self.theIntegrityRationale
  def availabilityProperty(self): return self.theAvailabilityProperty
  def availabilityRationale(self): return self.theAvailabilityRationale
  def accountabilityProperty(self): return self.theAccountabilityProperty
  def accountabilityRationale(self): return self.theAccountabilityRationale
  def anonymityProperty(self): return self.theAnonymityProperty
  def anonymityRationale(self): return self.theAnonymityRationale
  def pseudonymityProperty(self): return self.thePseudonymityProperty
  def pseudonymityRationale(self): return self.thePseudonymityRationale
  def unlinkabilityProperty(self): return self.theUnlinkabilityProperty
  def unlinkabilityRationale(self): return self.theUnlinkabilityRationale
  def unobservabilityProperty(self): return self.theUnobservabilityProperty
  def unobservabilityRationale(self): return self.theUnobservabilityRationale
  def interfaces(self): return self.theInterfaces
  def tags(self): return self.theTags
