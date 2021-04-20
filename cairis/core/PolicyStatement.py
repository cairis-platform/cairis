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

class PolicyStatement:
  def __init__(self,psId,goalName,envName,subjName,acName,resName,pName):
    self.theId = psId
    self.theGoalName = goalName
    self.theEnvironmentName = envName
    self.theSubject = subjName
    self.theAccessType = acName
    self.theResource = resName
    self.thePermission = pName

  def id(self): return self.theId
  def goal(self): return self.theGoalName
  def environment(self): return self.theEnvironmentName
  def subject(self): return self.theSubject
  def accessType(self): return self.theAccessType
  def resource(self): return self.theResource
  def permission(self): return self.thePermission
  def name(self): return self.theGoalName + '/' + self.theEnvironmentName + '/' + self.theSubject + '/' + self.theAccessType + '/' + self.theResource
