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

from . import ObjectValidator

class Requirement(ObjectValidator.ObjectValidator):
  def __init__(self, id, label, name='', description='', priority='1', rationale='', fitCriterion='', originator='', type='Functional', asset='', dType='asset', version=-1):
    ObjectValidator.ObjectValidator.__init__(self)
    self.theId = id
    if (version == -1):
      self.theVersion = 1
    else:
      self.theVersion = version
    self.attrs = {}
    self.theLabel = label
    self.theName = name
    self.theDescription = description
    self.thePriority = priority
    self.theRationale = rationale
    self.theOriginator = originator
    self.theFitCriterion = fitCriterion
    self.theSupportingMaterial = ''
    self.theType = type
    self.theDomain = asset
    self.theDomainType = dType
    self.dirtyAttrs = set([])

  def label(self):
    return self.theLabel

  def name(self):
    return self.theName

  def description(self):
    return self.theDescription

  def priority(self):
    return self.thePriority

  def rationale(self):
    return self.theRationale

  def fitCriterion(self):
    return self.theFitCriterion

  def version(self):
    return self.theVersion

  def originator(self):
    return self.theOriginator

  def type(self):
    return self.theType

  def domain(self):
    return self.theDomain

  def domainType(self):
    return self.theDomainType

  def dirty(self): return len(self.dirtyAttrs)

  def update(self,attr,val):
    if (attr == 'label'): self.theLabel = val
    elif (attr == 'name'): self.theName = val
    elif (attr == 'description'): self.theDescription = val
    elif (attr == 'priority'): self.thePriority = val
    elif (attr == 'rationale'): self.theRationale = val
    elif (attr == 'originator'): self.theOriginator = val
    elif (attr == 'fitCriterion'): self.theFitCriterion = val
    elif (attr == 'supportingMaterial'): self.theSupportingMaterial = val
    elif (attr == 'type'): self.theType = val
    elif (attr == 'domain'): self.theDomain = val
    self.dirtyAttrs.add(attr)

  def incrementVersion(self):
    self.theVersion += 1

  def id(self):
    return self.theId

  def asString(self):  return 'id:' + str(self.theId) + ', label:' + str(self.theLabel) + ', name: ' + self.theName + ', description:' + self.theDescription + ', priority:' + str(self.thePriority) + ', rationale:' + self.theRationale + ', fit criterion:' + self.theFitCriterion + ', originator:' + self.theOriginator + ',type:' + self.theType + ',version:' + str(self.theVersion)
