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


C_IDX = 0
I_IDX = 1
AV_IDX = 2
AC_IDX = 3
AN_IDX = 4
PAN_IDX = 5
UNL_IDX = 6
UNO_IDX = 7

NONE_ID = 0
LOW_ID = 1
MED_ID = 2
HIGH_ID = 3

class PropertyHolder:
  def __init__(self,syProps):
    self.theSecurityProperties = syProps

  def properties(self): return self.theSecurityProperties

  def propertyStrings(self):
    setProperties = []
    for idx,p in enumerate(self.theSecurityProperties):
      if (p > 0): setProperties.append(idx)

    properties = ''
    for idx,pr in enumerate(setProperties):
      if (pr == C_IDX):
        properties += 'C=' + self.confidentialityPropertyChar() 
      elif (pr == I_IDX):
        properties += 'I=' + self.integrityPropertyChar() 
      elif (pr == AV_IDX):
        properties += 'Av=' + self.availabilityPropertyChar() 
      elif (pr == AC_IDX):
        properties += 'Ac=' + self.accountabilityPropertyChar() 
      elif (pr == AN_IDX):
        properties += 'An=' + self.anonymityPropertyChar() 
      elif (pr == PAN_IDX):
        properties += 'Pan=' + self.pseudonymityPropertyChar() 
      elif (pr == UNL_IDX):
        properties += 'Unl=' + self.unlinkabilityPropertyChar() 
      else:
        properties += 'Uno=' + self.unobservabilityPropertyChar() 

      if (idx != (len(setProperties) - 1)):
        properties += ','
    return properties

  def propertyList(self):
    setProperties = []
    for idx,p in enumerate(self.theSecurityProperties):
      if (p > 0): setProperties.append(idx)

    properties = []
    for idx,pr in enumerate(setProperties):
      if (pr == C_IDX):
        properties.append(['Confidentiality',self.confidentialityPropertyString()]) 
      elif (pr == I_IDX):
        properties.append(['Integrity',self.integrityPropertyString()]) 
      elif (pr == AV_IDX):
        properties.append(['Availability',self.availabilityPropertyString()])
      elif (pr == AC_IDX):
        properties.append(['Accountability',self.accountabilityPropertyString()])
      elif (pr == AN_IDX):
        properties.append(['Anonymity',self.anonymityPropertyString()])
      elif (pr == PAN_IDX):
        properties.append(['Pseudonymity',self.pseudonymityPropertyString()])
      elif (pr == UNL_IDX):
        properties.append(['Unlinkability',self.unlinkabilityPropertyString()])
      else:
        properties.append(['Unobservability',self.unobservabilityPropertyString()])
    return properties

  def propertyChar(self,pValue):
    if (pValue == NONE_ID) : return ''
    elif (pValue == LOW_ID): return 'L'
    elif (pValue == MED_ID): return 'M'
    elif (pValue == HIGH_ID): return 'H'

  def propertyString(self,pValue):
    if (pValue == NONE_ID): return 'None'
    elif (pValue == LOW_ID): return 'Low'
    elif (pValue == MED_ID): return 'Medium'
    elif (pValue == HIGH_ID): return 'High'
  

  def confidentialityProperty(self): return self.theSecurityProperties[C_IDX]
  def confidentialityPropertyChar(self): return self.propertyChar(self.theSecurityProperties[C_IDX])
  def confidentialityPropertyString(self): return self.propertyString(self.theSecurityProperties[C_IDX])
  def integrityProperty(self): return self.theSecurityProperties[I_IDX]
  def integrityPropertyChar(self): return self.propertyChar(self.theSecurityProperties[I_IDX])
  def integrityPropertyString(self): return self.propertyString(self.theSecurityProperties[I_IDX])
  def availabilityProperty(self): return self.theSecurityProperties[AV_IDX]
  def availabilityPropertyChar(self): return self.propertyChar(self.theSecurityProperties[AV_IDX])
  def availabilityPropertyString(self): return self.propertyString(self.theSecurityProperties[AV_IDX])
  def accountabilityProperty(self): return self.theSecurityProperties[AC_IDX]
  def accountabilityPropertyChar(self): return self.propertyChar(self.theSecurityProperties[AC_IDX])
  def accountabilityPropertyString(self): return self.propertyString(self.theSecurityProperties[AC_IDX])
  def anonymityProperty(self): return self.theSecurityProperties[AN_IDX]
  def anonymityPropertyChar(self): return self.propertyChar(self.theSecurityProperties[AN_IDX])
  def anonymityPropertyString(self): return self.propertyString(self.theSecurityProperties[AN_IDX])
  def pseudonymityProperty(self): return self.theSecurityProperties[PAN_IDX]
  def pseudonymityPropertyChar(self): return self.propertyChar(self.theSecurityProperties[PAN_IDX])
  def pseudonymityPropertyString(self): return self.propertyString(self.theSecurityProperties[PAN_IDX])
  def unlinkabilityProperty(self): return self.theSecurityProperties[UNL_IDX]
  def unlinkabilityPropertyChar(self): return self.propertyChar(self.theSecurityProperties[UNL_IDX])
  def unlinkabilityPropertyString(self): return self.propertyString(self.theSecurityProperties[UNL_IDX])
  def unobservabilityProperty(self): return self.theSecurityProperties[UNO_IDX]
  def unobservabilityPropertyChar(self): return self.propertyChar(self.theSecurityProperties[UNO_IDX])
  def unobservabilityPropertyString(self): return self.propertyString(self.theSecurityProperties[UNO_IDX])
