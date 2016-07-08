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


import DialogClassParameters

class TraceDialogParameters(DialogClassParameters.DialogClassParameters):
  def __init__(self,winId,winLabel,dClass,createId,setterFn,creationFlag,fromObjt,fromId,toObjt,toId):
    DialogClassParameters.DialogClassParameters.__init__(self,winId,winLabel,dClass,createId,setterFn,creationFlag)
    self.theOldFromObject = fromObjt
    self.theOldFromId = fromId
    self.theOldToObject = toObjt
    self.theOldToId = toId

  def fromObject(self): return self.theOldFromObject
  def fromId(self): return self.theOldFromId
  def toObject(self): return self.theOldToObject
  def toId(self): return self.theOldToId
