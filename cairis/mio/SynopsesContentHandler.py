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

  def startElement(self,name,attrs):
    self.currentElementName = name
    if name == 'characteristic_synopsis':
      cName = attrs['characteristic']
      synName = attrs['synopsis']
      dimName = attrs['dimension']
      aType = attrs['actor_type']
      aName = attrs['actor']
      self.theCharacteristicSynopses.append(ReferenceSynopsis(-1,cName,synName,dimName,aType,aName))
    elif name == 'reference_synopsis':
      refName = attrs['reference']
      synName = attrs['synopsis']
      dimName = attrs['dimension']
      aType = attrs['actor_type']
      aName = attrs['actor']
      self.theReferenceSynopses.append(ReferenceSynopsis(-1,refName,synName,dimName,aType,aName))
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
