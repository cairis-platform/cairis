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

from .Step import Step

class Steps:
  def __init__(self): self.theSteps = []
  def __getitem__(self,stepNo): return self.theSteps[stepNo]
  def __setitem__(self,stepNo,s): self.theSteps[stepNo] = s
  def size(self): return len(self.theSteps)
  def append(self,s): self.theSteps.append(s)
  def remove(self,stepNo): self.theSteps.pop(stepNo)
  def insert(self,pos,s): self.theSteps.insert(pos,s)
