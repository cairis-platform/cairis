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

import pydot

from cairis.core.Borg import Borg
from cairis.core.ARM import *
from cairis.core.colourcodes import usecaseColourCode

class UsecaseModel:
  def __init__(self, associations, envName, usecaseName = '', graphName='usecase.dot', db_proxy=None, font_name=None, font_size=None):
    self.theAssociations = associations
    self.theEnvironmentName = envName
    self.theUsecaseName = usecaseName
    self.dbProxy = db_proxy
    self.fontName = font_name
    self.fontSize = font_size

    b = Borg()
    if db_proxy is None: 
      self.dbProxy = b.dbProxy

    if font_size is None or font_name is None:
      self.fontName = b.fontName
      self.fontSize = b.fontSize

    self.theGraph = pydot.Dot()
    self.theGraphName = os.path.join(b.tmpDir, graphName)

  def size(self):
    return len(self.theAssociations)

  def buildNode(self,dimName,objtName):
    objtUrl = dimName + '#' + objtName
    b = Borg()
    if (dimName == 'usecase'):
      ucAvgObjt = self.dbProxy.dimensionObject(objtName,'usecase')
      ucAvg = ucAvgObjt.average(self.theEnvironmentName,self.theEnvironmentObject.duplicateProperty(),self.theEnvironmentObject.overridingEnvironment())
      self.theGraph.add_node(pydot.Node(objtName,shape='box',style='filled',margin=0,color='black',fontcolor=white,fillcolor=usecaseColourCode(ucAvg),fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl)
    else: 
      raise UnknownNodeType(dimName)

  def layout(self,renderer = 'dot'):
    self.theGraph.write_xdot(self.theGraphName,prog=renderer)
    return open(self.theGraphName).read()

  def buildUsecaseModel(self):  
  b = Borg()
  self.nodeNameSet = set([])
  refNodes = set([])
  edgeSet = set([])

  for association in self.theAssociations:
      ucName = association.usecase()
      subucName = association.subusecase()
      ucDimName = association.usecaseDimension()
      subucDimName = association.subusecaseDimension()
      ucEnv = association.environment()
                             
      if ((self.theucName != '') and ucName not in self.nodeNameSet):
        self.buildNode(ucDimName,ucName)
      if ((self.theucName != '') and subucName not in self.nodeNameSet):
        self.buildNode(subucDimName,subucName)

       if ((refNodeName,goalName) not in edgeSet):
        self.theGraph.add_edge(goalEdge)
        edgeSet.add((refNodeName,goalName))
        refNodes.add(refNodeName)

      if ((subGoalName,refNodeName) not in edgeSet):
        self.theGraph.add_edge(pydot.Edge(subGoalName,refNodeName,dir='none',weight='1',URL=objtUrl))
        edgeSet.add((subGoalName,refNodeName))
      else:
          pass

  def graph(self):
    try:
      elements = []
      elements = self.dbProxy.usecaseModelElements(self.theEnvironmentName)

      for element in elements:
        self.buildNode(element[0],element[1])

      self.buildUsecaseModel()
      return self.layout()
    except DatabaseProxyException as errTxt:
      raise ARMException(errTxt)
