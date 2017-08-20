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


from .ObjectCreationParameters import ObjectCreationParameters

__author__ = 'Shamal Faily'

class ImpliedCharacteristicParameters(ObjectCreationParameters):
  def __init__(self,pName,fromCode,toCode,rtName,charName,qualName,lhsCodes,rhsCodes,charType):
    ObjectCreationParameters.__init__(self)
    self.thePersonaName = pName
    self.theFromCode = fromCode
    self.theToCode = toCode
    self.theRelationshipType = rtName
    self.theCharacteristicName = charName
    self.theQualifierName = qualName
    self.theLhsCodes = lhsCodes
    self.theRhsCodes = rhsCodes
    self.theCharacteristicType = charType
    self.theIntention = ''
    self.theIntentionType = ''

  def setIntention(self,v): self.theIntention = v
  def setIntentionType(self,v): self.theIntentionType = v

  def persona(self): return self.thePersonaName
  def fromCode(self): return self.theFromCode
  def toCode(self): return self.theToCode
  def relationshipType(self): return self.theRelationshipType
  def characteristic(self): return self.theCharacteristicName
  def qualifier(self): return self.theQualifierName
  def lhsCodes(self): return self.theLhsCodes
  def rhsCodes(self): return self.theRhsCodes
  def characteristicType(self): return self.theCharacteristicType
  def intention(self): return self.theIntention
  def intentionType(self): return self.theIntentionType
