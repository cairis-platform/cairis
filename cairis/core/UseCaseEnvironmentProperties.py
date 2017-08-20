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


from .EnvironmentProperties import EnvironmentProperties
from .Steps import Steps

class UseCaseEnvironmentProperties(EnvironmentProperties):
  def __init__(self,environmentName,preCond='',steps = None,postCond=''):
    EnvironmentProperties.__init__(self,environmentName)
    self.thePreCond = preCond
    self.theSteps = steps
    self.thePostCond = postCond

  def preconditions(self): return self.thePreCond
  def steps(self): return self.theSteps
  def postconditions(self): return self.thePostCond
