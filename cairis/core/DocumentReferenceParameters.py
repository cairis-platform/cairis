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


from .ObjectCreationParameters import ObjectCreationParameters

__author__ = 'Shamal Faily'

class DocumentReferenceParameters(ObjectCreationParameters):
  def __init__(self,refName,docName,cName,docExc):
    ObjectCreationParameters.__init__(self)
    self.theName = refName
    self.theDocName = docName
    self.theContributor = cName
    self.theExcerpt = docExc

  def name(self): return self.theName
  def document(self): return self.theDocName
  def contributor(self): return self.theContributor
  def description(self): return self.theExcerpt
