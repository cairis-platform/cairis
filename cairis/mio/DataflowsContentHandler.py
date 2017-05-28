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
from cairis.core.DataFlowParameters import DataFlowParameters

__author__ = 'Shamal Faily'

class DataflowsContentHandler(ContentHandler,EntityResolver):
  def __init__(self):
    self.theDataFlows = []
    self.resetDataFlowAttributes()

  def resolveEntity(self,publicId,systemId):
    return systemId

  def dataflows(self):
    return self.theDataFlows

  def resetDataFlowAttributes(self):
    self.theName = ''
    self.theEnvironmentName = ''
    self.theFromName = ''
    self.theFromType = ''
    self.theToName = ''
    self.theToType = ''
    self.theAssets = []

  def startElement(self,name,attrs):
    self.currentElementName = name
    if name == 'dataflow':
      self.theName = attrs['name']
      self.theEnvironmentName = attrs['environment']
      self.theFromName = attrs['from_name']
      self.theFromType = attrs['from_type']
      self.theToName = attrs['to_name']
      self.theToType = attrs['to_type']
    elif name == 'dataflow_asset':
      dfAsset = attrs['name']
      self.theAssets.append(dfAsset)

  def endElement(self,name):
    if name == 'dataflow':
      self.theDataFlows.append(DataFlowParameters(self.theName,self.theEnvironmentName,self.theFromName,self.theFromType,self.theToName,self.theToType,self.theAssets))
      self.resetDataFlowAttributes()
