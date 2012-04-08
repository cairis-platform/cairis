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


class TemplateAsset:
  def __init__(self,assetId,assetName,shortCode,assetDescription,assetSig,assetType,cFlag,cRationale,cProperty,iProperty,avProperty,acProperty,anProperty,panProperty,unlProperty,unoProperty,ifs,cRat = '',iRat = '',avRat = '',acRat = '',anRat = '',panRat = '',unlRat = '',unoRat = ''):
    self.theId = assetId
    self.theName = assetName
    self.theShortCode = shortCode
    self.theDescription = assetDescription
    self.theSignificance = assetSig
    self.theType = assetType
    self.isCritical = cFlag
    self.theCriticalRationale = cRationale
    self.theConfidentialityProperty = cProperty
    self.theIntegrityProperty = iProperty
    self.theAvailabilityProperty = avProperty
    self.theAccountabilityProperty = acProperty
    self.theAnonymityProperty = anProperty
    self.thePseudonymityProperty = panProperty
    self.theUnlinkabilityProperty = unlProperty
    self.theUnobservabilityProperty = unoProperty
    self.theConfidentialityRationale = cRat
    self.theIntegrityRationale = iRat
    self.theAvailabilityRationale = avRat
    self.theAccountabilityRationale = acRat
    self.theAnonymityRationale = anRat
    self.thePseudonymityRationale = panRat
    self.theUnlinkabilityRationale = unlRat
    self.theUnobservabilityRationale = unoRat
    self.theInterfaces = ifs

    self.valueLookup = {}
    self.valueLookup['None'] = 0
    self.valueLookup['Low'] = 1
    self.valueLookup['Medium'] = 2
    self.valueLookup['High'] = 3

  def id(self): return self.theId
  def name(self): return self.theName
  def shortCode(self): return self.theShortCode
  def description(self): return self.theDescription
  def significance(self): return self.theSignificance
  def type(self): return self.theType
  def critical(self): return self.isCritical
  def criticalRationale(self): return self.theCriticalRationale
  def confidentialityProperty(self): return self.theConfidentialityProperty
  def integrityProperty(self): return self.theIntegrityProperty
  def availabilityProperty(self): return self.theAvailabilityProperty
  def accountabilityProperty(self): return self.theAccountabilityProperty
  def anonymityProperty(self): return self.theAnonymityProperty
  def pseudonymityProperty(self): return self.thePseudonymityProperty
  def unlinkabilityProperty(self): return self.theUnlinkabilityProperty
  def unobservabilityProperty(self): return self.theUnobservabilityProperty
  def interfaces(self): return self.theInterfaces

  def securityProperties(self):
    cValue = self.valueLookup[self.theConfidentialityProperty]
    iValue = self.valueLookup[self.theIntegrityProperty]
    avValue = self.valueLookup[self.theAvailabilityProperty]
    acValue = self.valueLookup[self.theAccountabilityProperty]
    anValue = self.valueLookup[self.theAnonymityProperty]
    panValue = self.valueLookup[self.thePseudonymityProperty]
    unlValue = self.valueLookup[self.theUnlinkabilityProperty]
    unoValue = self.valueLookup[self.theUnobservabilityProperty]
    return [cValue,iValue,avValue,acValue,anValue,panValue,unlValue,unoValue]

  def rationale(self):
    return [self.theConfidentialityRationale,self.theIntegrityRationale,self.theAvailabilityRationale,self.theAccountabilityRationale,self.theAnonymityRationale,self.thePseudonymityRationale,self.theUnlinkabilityRationale,self.theUnobservabilityRationale]
