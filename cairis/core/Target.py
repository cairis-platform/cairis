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


class Target:
  def __init__(self,tName,tEffectiveness,tRat):
    self.theName = tName
    self.theEffectiveness = tEffectiveness
    self.theRationale = tRat

  def name(self): return self.theName
  def effectiveness(self): return self.theEffectiveness
  def rationale(self): return self.theRationale
 
  def __getitem__(self,idx): 
    if (idx == 0): 
      return self.theName
    elif (idx == 1):
      return self.theEffectiveness
    else:
      return self.theRationale
