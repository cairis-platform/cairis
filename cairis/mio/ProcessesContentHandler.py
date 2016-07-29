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
from cairis.core.InternalDocumentParameters import InternalDocumentParameters
from cairis.core.CodeParameters import CodeParameters
from cairis.core.MemoParameters import MemoParameters
from cairis.core.ImpliedProcessParameters import ImpliedProcessParameters
from cairis.core.ImpliedCharacteristicParameters import ImpliedCharacteristicParameters
from cairis.core.Borg import Borg

__author__ = 'Shamal Faily'

class ProcessesContentHandler(ContentHandler,EntityResolver):
  def __init__(self):
    self.theInternalDocuments = []
    self.theCodes = []
    self.theMemos = []
    self.theQuotations = []
    self.theCodeNetworks = []
    self.theImpliedCharacteristics = []
    self.theProcesses = []
    self.theIntentions = [] 
    self.theContributions = []
    b = Borg()
    self.configDir = b.configDir
    self.resetInternalDocumentAttributes()
    self.resetCodeAttributes()
    self.resetMemoAttributes()
    self.resetQuotationAttributes()
    self.resetCodeNetworkAttributes()
    self.resetImpliedCharacteristicAttributes()
    self.resetProcessAttributes()

  def resolveEntity(self,publicId,systemId):
    return systemId

  def internalDocuments(self):
    return self.theInternalDocuments

  def codes(self):
    return self.theCodes

  def memos(self):
    return self.theMemos

  def quotations(self):
    return self.theQuotations

  def codeNetworks(self):
    return self.theCodeNetworks

  def impliedCharacteristics(self):
    return self.theImpliedCharacteristics

  def processes(self):
    return self.theProcesses

  def intentions(self):
    return self.theIntentions

  def contributions(self):
    return self.theContributions

  def resetInternalDocumentAttributes(self):
    self.inDescription = 0
    self.inContent = 0
    self.theName = ''
    self.theDescription = ''
    self.theContent = ''

  def resetCodeAttributes(self):
    self.inDescription = 0
    self.inInclusionCriteria = 0
    self.inExample = 0
    self.theName = ''
    self.theType = ''
    self.theDescription = ''
    self.theInclusionCriteria = ''
    self.theExample = ''

  def resetMemoAttributes(self):
    self.inDescription = 0
    self.theName = ''
    self.theDescription = ''

  def resetQuotationAttributes(self):
    self.inLabel = 0
    self.inSynopsis = 0
    self.theType = 'code'
    self.theCode = ''
    self.theArtifactType = ''
    self.theArtifactName = ''
    self.theEnvironment = 'None'
    self.theSection = ''
    self.theStartIndex = ''
    self.theEndIndex = ''
    self.theLabel = ''
    self.theSynopsis = ''

  def resetCodeNetworkAttributes(self):
    self.thePersona = ''
    self.theRelationshipType = ''
    self.theFromCode = ''
    self.theToCode = ''

  def resetProcessAttributes(self):
    self.inDescription = 0
    self.inSpecification = 0
    self.theName = ''
    self.thePersona = ''
    self.theDescription = ''
    self.theSpecification = ''
    self.theProcessNetwork = []
    self.theChannels = []

  def resetImpliedCharacteristicAttributes(self):
    self.theImpliedCharacteristicName = ''
    self.theImpliedCharacteristicQualifier = ''
    self.theImpliedCharacteristicType = ''
    self.theFromLabels = []
    self.theToLabels = []
    self.theLabelName = ''

  def startElement(self,name,attrs):
    self.currentElementName = name
    if name == 'internal_document':
      self.theName = attrs['name']
    elif name == 'code':
      self.theName = attrs['name']
      self.theType = attrs['type']
    elif name == 'memo':
      self.theName = attrs['name']
    elif name == 'quotation':
      self.theType = attrs['type']
      self.theCode = attrs['code']
      self.theArtifactType = attrs['artifact_type']
      self.theArtifactName = attrs['artifact_name']
      try:
        self.theEnvironment = attrs['environment']
      except KeyError:
        self.theEnvironment = 'None'
      self.theSection = attrs['section']
      self.theStartIndex = int(attrs['start_index'])
      self.theEndIndex = int(attrs['to_index'])
    elif name == 'code_network':
      self.thePersona = attrs['persona']
      self.theRelationshipType = attrs['relationship_type']
      self.theFromCode = attrs['from_code']
      self.theToCode = attrs['to_code']
      self.theCodeNetworks.append((self.thePersona,self.theRelationshipType,self.theFromCode,self.theToCode))
    elif name == 'implied_characteristic':
      self.theImpliedCharacteristicName = attrs['name']
      self.theImpliedCharacteristicQualifier = attrs['qualifier']
      self.theImpliedCharacteristicType = attrs['type']
    elif name == 'intention':
      intentionName = attrs['name']
      intentionType = attrs['type']
      if (self.theImpliedCharacteristicName != ''):
        refName = self.theImpliedCharacteristicName
        refType = 'implied_characteristic'
      else:
        refName = self.theLabel
        refType = 'implied_characteristic_element'
      self.theIntentions.append((refName,refType,intentionName,intentionType))
    elif name == 'contribution':
      srcName = self.theLabelName
      destName = self.theImpliedCharacteristicName
      meansEnd = attrs['means_end']
      valName = attrs['value']
      self.theContributions.append((srcName,destName,meansEnd,valName))
    elif name == 'from_label':
      self.theLabelName = attrs['name']
      fromRefType = attrs['reference_type']
      self.theFromLabels.append((self.theLabelName,fromRefType))
    elif name == 'to_label':
      self.theLabelName = attrs['name']
      toRefType = attrs['reference_type']
      self.theToLabels.append((self.theLabelName,toRefType))
    elif name == 'implied_process':
      self.theName = attrs['name']
      self.thePersona = attrs['persona']
    elif name == 'channel':
      channelName = attrs['name']
      dataType = ''
      try:
        dataType = attrs['data_type']
      except KeyError:
        pass
      self.theChannels.append((channelName,dataType))
    elif name == 'relationship':
      self.theProcessNetwork.append((attrs['from_code'],'',attrs['to_code'],'',attrs['relationship_type']))
    elif name == 'description':
      self.inDescription = 1
      self.theDescription = ''
    elif name == 'inclusion_criteria':
      self.inInclusionCriteria = 1
      self.theInclusionCriteria = ''
    elif name == 'example':
      self.inExample = 1
      self.theExample = ''
    elif name == 'specification':
      self.inSpecification = 1
      self.theSpecification = ''
    elif name == 'content':
      self.inContent = 1
      self.theContent = ''
    elif name == 'label':
      self.inLabel = 1
      self.theLabel = ''
    elif name == 'synopsis':
      self.inSynopsis = 1
      self.theSynopsis = ''

  def characters(self,data):
    if self.inDescription:
      self.theDescription += data
    elif self.inInclusionCriteria:
      self.theInclusionCriteria += data
    elif self.inExample:
      self.theExample += data
    elif self.inSpecification:
      self.theSpecification += data
    elif self.inContent:
      self.theContent += data
    elif self.inLabel:
      self.theLabel += data
    elif self.inSynopsis:
      self.theSynopsis += data

  def endElement(self,name):
    if name == 'internal_document':
      p = InternalDocumentParameters(self.theName,self.theDescription,self.theContent,[],[])
      self.theInternalDocuments.append(p)
      self.resetInternalDocumentAttributes()
    elif name == 'code':
      p = CodeParameters(self.theName,self.theType,self.theDescription,self.theInclusionCriteria,self.theExample)
      self.theCodes.append(p)
      self.resetCodeAttributes()
    elif name == 'memo':
      p = MemoParameters(self.theName,self.theDescription)
      self.theMemos.append(p)
      self.resetMemoAttributes()
    elif name == 'implied_process':
      p = ImpliedProcessParameters(self.theName,self.theDescription,self.thePersona,self.theProcessNetwork,self.theSpecification,self.theChannels)
      self.theProcesses.append(p)
      self.resetProcessAttributes()
    elif name == 'quotation':
      self.theQuotations.append((self.theType,self.theCode,self.theArtifactType,self.theArtifactName,self.theEnvironment,self.theSection,self.theStartIndex,self.theEndIndex,self.theLabel,self.theSynopsis))
      self.resetQuotationAttributes()
    elif name == 'implied_characteristic':
      p = ImpliedCharacteristicParameters(self.thePersona,self.theFromCode,self.theToCode,self.theRelationshipType,self.theImpliedCharacteristicName,self.theImpliedCharacteristicQualifier,self.theFromLabels,self.theToLabels,self.theImpliedCharacteristicType) 
      self.theImpliedCharacteristics.append(p)
      self.resetImpliedCharacteristicAttributes()
    elif name == 'description':
      self.inDescription = 0
    elif name == 'inclusion_criteria':
      self.inInclusionCriteria = 0
    elif name == 'example':
      self.inExample = 0
    elif name == 'specification':
      self.inSpecification = 0
    elif name == 'content':
      self.inContent = 0
    elif name == 'label':
      self.inLabel = 0
    elif name == 'synopsis':
      self.inSynopsis = 0
