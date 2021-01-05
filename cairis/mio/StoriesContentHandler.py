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


from xml.sax.handler import ContentHandler,EntityResolver
from cairis.core.UserStory import UserStory 
from cairis.core.Borg import Borg

__author__ = 'Shamal Faily'

class StoriesContentHandler(ContentHandler,EntityResolver):
  def __init__(self,session_id = None):
    b = Borg()
    self.dbProxy = b.get_dbproxy(session_id)
    self.configDir = b.configDir
    self.theUserStories = []
    self.resetUserStoryAttributes()

  def resolveEntity(self,publicId,systemId):
    return systemId

  def userStories(self):
    return self.theUserStories

  def resetUserStoryAttributes(self):
    self.inDescription = 0
    self.inUserGoal = 0
    self.inAcceptanceCriteria = 0
    self.theName = ''
    self.theAuthor = ''
    self.theRole = ''
    self.theDescription = ''
    self.theUserGoal = ''
    self.theCurrentAcceptanceCriteria = ''
    self.theAcceptanceCriteria = []
    self.theTags = []


  def startElement(self,name,attrs):
    self.currentElementName = name
    if name == 'userstory':
      self.theName = attrs['name']
      self.theAuthor = attrs['author']
      self.theRole = attrs['role']
    elif name == 'tag':
      self.theTags.append(attrs['name'])
    elif name == 'description':
      self.inDescription = 1
      self.theDescription = ''
    elif name == 'user_goal':
      self.inUserGoal = 1
      self.theUserGoal = ''
    elif name == 'acceptance_criteria':
      self.inAcceptanceCriteria = 1
      self.theCurrentAcceptanceCriteria = ''

  def characters(self,data):
    if self.inDescription:
      self.theDescription += data
    elif self.inUserGoal:
      self.theUserGoal += data
    elif self.inAcceptanceCriteria:
      self.theCurrentAcceptanceCriteria += data


  def endElement(self,name):
    if name == 'userstory':
      self.theUserStories.append(UserStory(-1,self.theName,self.theAuthor,self.theRole,self.theDescription,self.theUserGoal,self.theAcceptanceCriteria,self.theTags))
      self.resetUserStoryAttributes()
    elif name == 'description':
      self.inDescription = 0
    elif name == 'user_goal':
      self.inUserGoal = 0
    elif name == 'acceptance_criteria':
      self.inAcceptanceCriteria = 0
      self.theAcceptanceCriteria.append(self.theCurrentAcceptanceCriteria)

