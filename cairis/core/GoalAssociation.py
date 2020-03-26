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

class GoalAssociation:
  def __init__(self,associationId,envName,goalName,goalDimName,aType,subGoalName,subGoalDimName,alternativeId,rationale):
    self.theId = associationId
    self.theEnvironmentName = envName
    self.theGoal = goalName
    self.theGoalDimension = goalDimName
    self.theAssociationType = aType
    self.theSubGoal = subGoalName
    self.theSubGoalDimension = subGoalDimName
    self.theAlternativeId = alternativeId
    self.theRationale = rationale

  def id(self): return self.theId
  def environment(self): return self.theEnvironmentName
  def goal(self): return self.theGoal
  def goalDimension(self): return self.theGoalDimension
  def type(self): return self.theAssociationType
  def subGoal(self): return self.theSubGoal
  def subGoalDimension(self): return self.theSubGoalDimension
  def alternative(self): return self.theAlternativeId
  def rationale(self): return self.theRationale
  def name(self): return self.theEnvironmentName + ' / ' + self.theGoal + ' / ' + self.theSubGoal
  def __str__(self): return self.theEnvironmentName + ' / ' + self.theGoal + ' / '  + self.theGoalDimension + ' / ' + self.theAssociationType + ' / ' + self.theSubGoal + ' / ' + self.theSubGoalDimension + ' / ' + str(self.theAlternativeId)
