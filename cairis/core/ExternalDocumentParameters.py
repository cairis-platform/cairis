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

class ExternalDocumentParameters(ObjectCreationParameters):
  def __init__(self,edName,edVersion,edDate,edAuths,edDesc):
    ObjectCreationParameters.__init__(self)
    self.theName = edName
    self.theVersion = edVersion
    self.thePublicationDate = edDate
    self.theAuthors = edAuths
    self.theDescription = edDesc

  def name(self): return self.theName
  def version(self): return self.theVersion
  def date(self): return self.thePublicationDate
  def authors(self): return self.theAuthors
  def description(self): return self.theDescription
