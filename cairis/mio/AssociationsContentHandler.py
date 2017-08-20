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
from cairis.core.GoalAssociationParameters import GoalAssociationParameters
from cairis.core.DependencyParameters import DependencyParameters
from cairis.core.Borg import Borg
from cairis.core.ARM import *

__author__ = 'Shamal Faily'

def a2s(aStr):
  if aStr == 'a':
    return '*'
  elif aStr == '1..a':
    return '1..*'
  else:
    return aStr

def u2s(aStr):
  outStr = ''
  for c in aStr:
    if (c == '_'):
      outStr += ' '
    else:
      outStr += c
  return outStr
  
class AssociationsContentHandler(ContentHandler,EntityResolver):
  def __init__(self,session_id = None):
    b = Borg()
    self.dbProxy = b.get_dbproxy(session_id)
    self.configDir = b.configDir
    self.theManualAssociations = set([])
    self.theGoalAssociations = []
    self.theDependencyAssociations = []

    self.resetManualAssociationAttributes()
    self.resetGoalAssociationAttributes()
    self.resetDependencyAssociationAttributes()

  def resolveEntity(self,publicId,systemId):
    return systemId

  def manualAssociations(self):
    return self.theManualAssociations

  def goalAssociations(self):
    return self.theGoalAssociations

  def dependencyAssociations(self):
    return self.theDependencyAssociations

  def resetManualAssociationAttributes(self):
    self.theFromName = ''
    self.theFromDim = ''
    self.theToName = ''
    self.theToDim = ''
    self.theReferenceType = ''

  def resetGoalAssociationAttributes(self):
    self.theEnvironmentName = ''
    self.theGoalName = ''
    self.theGoalDim = ''
    self.theReferenceType = ''
    self.theSubGoalName = ''
    self.theSubGoalDim = ''
    self.isAlternative = 0
    self.inRationale = 0
    self.theRationale = ''

  def resetDependencyAssociationAttributes(self):
    self.theDepender = ''
    self.theDependee = ''
    self.theDepType = ''
    self.theDependency = ''
    self.theEnvironmentName = ''
    self.inRationale = 0
    self.theRationale = ''

  def startElement(self,name,attrs):
    self.currentElementName = name
    if name == 'manual_association':
      self.theFromName = attrs['from_name']
      self.theFromDim = attrs['from_dim']
      self.theToName = attrs['to_name']
      self.theToDim = attrs['to_dim']
      if (self.theFromDim == 'requirement') and (self.theToDim == 'task' or self.theToDim == 'usecase'):
        try:
          self.theReferenceType = attrs['ref_type']
        except KeyError:
          self.theReferenceType = 'and'

      if (self.theFromDim == 'requirement') and (self.theToDim == 'requirement'):
        try:
          self.theReferenceType = attrs['label']
        except KeyError:
          self.theReferenceType = ''

    elif name == 'goal_association':
      self.theEnvironmentName = attrs['environment']
      self.theGoalName = attrs['goal_name']
      self.theGoalDim = attrs['goal_dim']
      self.theReferenceType = attrs['ref_type']
      self.theSubGoalName = attrs['subgoal_name']
      self.theSubGoalDim = attrs['subgoal_dim']
      self.isAlternative = attrs['alternative_id']
    elif name == 'dependency':
      self.theDepender = attrs['depender']
      self.theDependee = attrs['dependee']
      self.theDepType = attrs['dependency_type']
      self.theDependency = attrs['dependency']
      self.theEnvironmentName = attrs['environment']
    elif name == 'rationale':
      self.inRationale = 1
      self.theRationale = ''

  def characters(self,data):
    if self.inRationale:
      self.theRationale += data

  def endElement(self,name):
    if name == 'manual_association':
      try:
        fromId = self.dbProxy.getDimensionId(self.theFromName,self.theFromDim)
        toId = self.dbProxy.getDimensionId(self.theToName,self.theToDim)
        tableName = self.theFromDim + '_' + self.theToDim
        if (tableName,fromId,toId,self.theReferenceType) not in self.theManualAssociations:
          self.theManualAssociations.add((tableName,fromId,toId,self.theReferenceType))
      except DatabaseProxyException as e:
        pass # skipping invalid trace
      self.resetManualAssociationAttributes()
    elif name == 'goal_association':
      p = GoalAssociationParameters(self.theEnvironmentName,self.theGoalName,self.theGoalDim,self.theReferenceType,self.theSubGoalName,self.theSubGoalDim,self.isAlternative,self.theRationale)
      self.theGoalAssociations.append(p)
      self.resetGoalAssociationAttributes()
    elif name == 'dependency':
      p = DependencyParameters(self.theEnvironmentName,self.theDepender,self.theDependee,self.theDepType,self.theDependency,self.theRationale)
      self.theDependencyAssociations.append(p)
      self.resetDependencyAssociationAttributes()
    elif name == 'rationale':
      self.inRationale = 0
