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
from cairis.core.ReferenceSynopsis import ReferenceSynopsis
from cairis.core.ReferenceContribution import ReferenceContribution
from cairis.core.TaskContribution import TaskContribution
from cairis.core.Borg import Borg

__author__ = 'Shamal Faily'

class SynopsesContentHandler(ContentHandler,EntityResolver):
  def __init__(self,session_id = None):
    b = Borg()
    self.dbProxy = b.get_dbproxy(session_id)
    self.configDir = b.configDir
    self.theCharacteristicSynopses = []
    self.theReferenceSynopses = []
    self.theStepSynopses = []
    self.theReferenceContributions = []
    self.theUseCaseContributions = []
    self.theTaskContributions = []
    self.resetSynopsisAttributes()

  def resolveEntity(self,publicId,systemId):
    return systemId

  def characteristicSynopses(self):
    return self.theCharacteristicSynopses

  def referenceSynopses(self):
    return self.theReferenceSynopses

  def stepSynopses(self):
    return self.theStepSynopses

  def referenceContributions(self):
    return self.theReferenceContributions

  def useCaseContributions(self):
    return self.theUseCaseContributions

  def taskContributions(self):
    return self.theTaskContributions

  def resetSynopsisAttributes(self):
    self.theCharacteristic = ''
    self.theReference = ''
    self.theSynopsis = ''
    self.theDimensionName = ''
    self.theActorType = ''
    self.theActor = ''
    self.theInitialSatisfaction = 'None'
    self.theSystemGoals = []

  def startElement(self,name,attrs):
    self.currentElementName = name
    if name == 'characteristic_synopsis':
      self.theCharacteristic = attrs['characteristic']
      self.theSynopsis = attrs['synopsis']
      self.theDimensionName = attrs['dimension']
      self.theActorType = attrs['actor_type']
      self.theActor = attrs['actor']
      try:
        self.theInitialSatisfaction = attrs['satisfaction']
      except KeyError:
        pass 
    elif name == 'reference_synopsis':
      self.theReference = attrs['reference']
      self.theSynopsis = attrs['synopsis']
      self.theDimensionName = attrs['dimension']
      self.theActorType = attrs['actor_type']
      self.theActor = attrs['actor']
      try:
        self.theInitialSatisfaction = attrs['satisfaction']
      except KeyError:
        pass 
    elif name == 'system_goal':
      self.theSystemGoals.append(attrs['name'])
    elif name == 'step_synopsis':
      ucName = attrs['usecase']
      envName = attrs['environment']
      stepNo = attrs['step_no']    
      synName = attrs['synopsis']
      aType = attrs['actor_type']
      aName = attrs['actor']
      self.theStepSynopses.append((ucName,envName,stepNo,synName,aType,aName))
    elif name == 'reference_contribution':
      src = attrs['source']
      dest = attrs['destination']
      me = attrs['means_end']
      cont = attrs['contribution']
      self.theReferenceContributions.append(ReferenceContribution(src,dest,me,cont))
    elif name == 'usecase_contribution':
      ucName = attrs['usecase']
      refName = attrs['referent']
      me = attrs['means_end']
      cont = attrs['contribution']
      self.theUseCaseContributions.append(ReferenceContribution(ucName,refName,me,cont))
    elif name == 'task_contribution':
      taskName = attrs['task']
      envName = attrs['environment']
      refName = attrs['referent']
      cont = attrs['contribution']
      self.theTaskContributions.append(TaskContribution(taskName,refName,envName,cont))

  def endElement(self,name):
    if name == 'characteristic_synopsis':
      self.theCharacteristicSynopses.append(ReferenceSynopsis(-1,self.theCharacteristic,self.theSynopsis,self.theDimensionName,self.theActorType,self.theActor,'persona_characteristic',self.theInitialSatisfaction,self.theSystemGoals))
      self.resetSynopsisAttributes()
    elif name == 'reference_synopsis':
      self.theReferenceSynopses.append(ReferenceSynopsis(-1,self.theReference,self.theSynopsis,self.theDimensionName,self.theActorType,self.theActor,'document_reference',self.theInitialSatisfaction,self.theSystemGoals))
      self.resetSynopsisAttributes()
