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

class GoalContribution:
  def __init__(self,src,srcType,dest,destType,me,cont):
    self.theSource = src
    self.theSourceType = srcType
    self.theDestination = dest
    self.theDestinationType = destType
    self.theMeansEnd = me
    self.theContribution = cont

  def source(self): return self.theSource
  def sourceType(self): return self.theSourceType
  def destination(self): return self.theDestination
  def destinationType(self): return self.theDestinationType
  def meansEnd(self): return self.theMeansEnd
  def contribution(self): return self.theContribution
  def name(self): return self.theSource + ' / ' + self.theDestination
