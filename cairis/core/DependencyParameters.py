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


from . import ObjectCreationParameters

__author__ = 'Shamal Faily'

class DependencyParameters(ObjectCreationParameters.ObjectCreationParameters):
  def __init__(self,envName,depender,dependee,dependencyType,dependency,rationale):
    ObjectCreationParameters.ObjectCreationParameters.__init__(self)
    self.theEnvironmentName = envName
    self.theDepender = depender
    self.theDependee = dependee
    self.theDependencyType = dependencyType
    self.theDependency = dependency
    self.theRationale = rationale

  def environment(self): return self.theEnvironmentName
  def depender(self): return self.theDepender
  def dependee(self): return self.theDependee
  def dependencyType(self): return self.theDependencyType
  def dependency(self): return self.theDependency
  def rationale(self): return self.theRationale
