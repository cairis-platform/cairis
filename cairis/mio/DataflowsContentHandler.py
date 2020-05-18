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
from cairis.core.TrustBoundary import TrustBoundary

__author__ = 'Shamal Faily'

class DataflowsContentHandler(ContentHandler,EntityResolver):
  def __init__(self):
    self.theDataFlows = []
    self.theTrustBoundaries = []
    self.resetDataFlowAttributes()
    self.resetTrustBoundaryAttributes()

  def resolveEntity(self,publicId,systemId):
    return systemId

  def dataflows(self):
    return self.theDataFlows

  def trustBoundaries(self):
    return self.theTrustBoundaries

  def resetDataFlowAttributes(self):
    self.theName = ''
    self.theEnvironmentName = ''
    self.theFromName = ''
    self.theFromType = ''
    self.theToName = ''
    self.theToType = ''
    self.theAssets = []
    self.theObstacles = []

  def resetTrustBoundaryAttributes(self):
    self.inDescription = 0
    self.theDescription = ''
    self.theName = ''
    self.theEnvironmentName = ''
    self.theEnvironmentComponents = {}
    self.theComponents = []
    self.theEnvironmentPrivileges = {}

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
    elif name == 'dataflow_obstacle':
      dfObs = attrs['name']
      self.theObstacles.append(dfObs)
    elif name == 'trust_boundary':
      self.theName = attrs['name']
    elif name == 'description':
      self.inDescription = 1
      self.theDescription = ''
    elif name == 'trust_boundary_environment':
      self.theEnvironmentName = attrs['name']
      pLevel = 'None'
      if ('privilege' in attrs):
        pLevel = attrs['privilege']
      self.theEnvironmentPrivileges[self.theEnvironmentName] = pLevel
    elif name == 'trust_boundary_component':
      self.theComponents.append((attrs['type'],attrs['name']))

  def characters(self,data):
    if self.inDescription:
      self.theDescription += data

  def endElement(self,name):
    if name == 'dataflow':
      self.theDataFlows.append(DataFlowParameters(self.theName,self.theEnvironmentName,self.theFromName,self.theFromType,self.theToName,self.theToType,self.theAssets,self.theObstacles))
      self.resetDataFlowAttributes()
    elif name == 'trust_boundary_environment':
      self.theEnvironmentComponents[self.theEnvironmentName] = self.theComponents
      self.theComponents = []
      self.theEnvironmentName = ''
    elif name == 'trust_boundary':
      self.theTrustBoundaries.append(TrustBoundary(-1,self.theName,self.theDescription,self.theEnvironmentComponents,self.theEnvironmentPrivileges))
      self.resetTrustBoundaryAttributes()
    elif name == 'description':
      self.inDescription = 0
