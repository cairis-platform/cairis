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

from . import ObjectValidator

__author__ = 'Shamal Faily'


class UserStory(ObjectValidator.ObjectValidator):
  def __init__(self,usId,usName,usAuth,usRole,usDesc,ugName,ac,usTags = []):
    ObjectValidator.ObjectValidator.__init__(self)
    self.theId = usId
    self.theName = usName
    self.theAuthor = usAuth
    self.theRole = usRole
    self.theDescription = usDesc
    self.theUserGoal = ugName
    self.theAcceptanceCriteria = ac
    self.theTags = usTags

  def id(self): return self.theId
  def name(self): return self.theName
  def author(self): return self.theAuthor
  def role(self): return self.theRole
  def description(self): return self.theDescription
  def userGoal(self): return self.theUserGoal
  def acceptanceCriteria(self): return self.theAcceptanceCriteria
  def tags(self): return self.theTags
