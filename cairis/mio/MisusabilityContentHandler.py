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

import os
from xml.sax.handler import ContentHandler,EntityResolver
from cairis.core.ConceptReferenceParameters import ConceptReferenceParameters
from cairis.core.TaskCharacteristicParameters import TaskCharacteristicParameters
from cairis.core.Borg import Borg

__author__ = 'Shamal Faily'

class MisusabilityContentHandler(ContentHandler,EntityResolver):
  def __init__(self):
    self.theConceptReferences = []
    self.theTaskCharacteristics = []
    b = Borg()
    self.configDir = b.configDir
    self.resetConceptReferenceAttributes()
    self.resetTaskCharacteristicAttributes()

  def resolveEntity(self,publicId,systemId):
    return systemId

  def conceptReferences(self):
    return self.theConceptReferences

  def taskCharacteristics(self):
    return self.theTaskCharacteristics

  def resetConceptReferenceAttributes(self):
    self.inDescription = 0
    self.theName = ''
    self.theConcept = ''
    self.theObject = ''
    self.theDescription = ''

  def resetTaskCharacteristicAttributes(self):
    self.theTask = ''
    self.inTC = 0
    self.theModalQualifier = ''
    self.inDefinition = 0
    self.theDefinition = ''
    self.theGrounds = []
    self.theWarrants = []
    self.theRebuttals = []

  def startElement(self,name,attrs):
    self.currentElementName = name
    if name == 'concept_reference':
      self.theName = attrs['name']
      self.theConcept = attrs['concept']
      self.theObject = attrs['object']
    elif (name == 'grounds' and self.inTC == 1):
      refName = attrs['reference']
      refType = attrs['type']
      refArtifact = ''
      self.theGrounds.append((refName,'',refType))
    elif (name == 'warrant' and self.inTC == 1):
      refName = attrs['reference']
      refType = attrs['type']
      refArtifact = ''
      self.theWarrants.append((refName,'',refType))
    elif (name == 'rebuttal' and self.inTC == 1):
      refName = attrs['reference']
      refType = attrs['type']
      refArtifact = ''
    elif name == 'task_characteristic':
      self.theTask = attrs['task']
      self.theModalQualifier = attrs['modal_qualifier'] 
      self.inTC = 1
    elif name == 'definition':
      self.inDefinition = 1
      self.theDefinition = ''

  def characters(self,data):
    if self.inDefinition:
      self.theDefinition += data

  def endElement(self,name):
    if name == 'concept_reference':
      p = ConceptReferenceParameters(self.theName,self.theConcept,self.theObject,self.theDescription)
      self.theConceptReferences.append(p)
      self.resetConceptReferenceAttributes()
    elif name == 'task_characteristic':
      p = TaskCharacteristicParameters(self.theTask,self.theModalQualifier,self.theDefinition,self.theGrounds,self.theWarrants,[],self.theRebuttals)
      self.theTaskCharacteristics.append(p)
      self.resetTaskCharacteristicAttributes()
    elif name == 'definition':
      self.inDefinition = 0
