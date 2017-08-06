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

class Requirement:
  def __init__(self, id, label, name='', description='', priority='1', rationale='', fitCriterion='', originator='', type='Functional', asset='', version=-1):
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
    self.attrs['rationale'] = rationale
    self.attrs['originator'] = originator
    self.attrs['fitCriterion'] = fitCriterion
    self.attrs['supportingMaterial'] = ''
    self.attrs['type'] = type
    self.attrs['asset'] = asset
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
    return self.attrs['rationale']

  def fitCriterion(self):
    return self.attrs['fitCriterion']

  def version(self):
    return self.theVersion

  def originator(self):
    return self.attrs['originator']

  def type(self):
    return self.attrs['type']

  def asset(self):
    return self.attrs['asset']

  def dirty(self):
    return len(self.dirtyAttrs)

  def update(self,attr,val):
    if (attr == 'label'):
      self.theLabel = val
    elif (attr == 'name'):
      self.theName = val
    elif (attr == 'description'):
      self.theDescription = val
    elif (attr == 'priority'):
      self.thePriority = val
    else:
      self.attrs[attr] = str(val)
    self.dirtyAttrs.add(attr)

  def incrementVersion(self):
    self.theVersion += 1

  def id(self):
    return self.theId

  def asString(self):
    return 'id:' + str(self.theId) + ', label:' + str(self.theLabel) + ', name: ' + self.theName + ', description:' + self.theDescription + ', priority:' + str(self.thePriority) + ', rationale:' + self.attrs['rationale'] + ', fit criterion:' + self.attrs['fitCriterion'] + ', originator:' + self.attrs['originator'] + ',type:' + self.attrs['type'] + ',version:' + str(self.theVersion)
