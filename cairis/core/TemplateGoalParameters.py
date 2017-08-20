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

from . import ObjectCreationParameters

class TemplateGoalParameters(ObjectCreationParameters.ObjectCreationParameters):
  def __init__(self,goalName,goalDef,goalRat,goalConcerns,goalResp):
    ObjectCreationParameters.ObjectCreationParameters.__init__(self)
    self.theName = goalName
    self.theDefinition = goalDef
    self.theRationale = goalRat
    self.theConcerns = goalConcerns
    self.theResponsibilities = goalResp

  def name(self): return self.theName
  def definition(self): return self.theDefinition
  def rationale(self): return self.theRationale
  def concerns(self): return self.theConcerns
  def responsibilities(self): return self.theResponsibilities
