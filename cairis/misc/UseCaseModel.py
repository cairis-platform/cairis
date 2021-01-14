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


class KaosModel:
  def __init__(self, associations, envName, kaosModelType = 'usecase', usecaseName = '', db_proxy=None, font_name=None, font_size=None):
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
    self.theKaosModel = kaosModelType
    if (self.theKaosModel == 'usecase'):
      self.theGraph.set_graph_defaults(rankdir='LR')
    else:
      self.theGraph.set_graph_defaults(rankdir='BT')
    self.theGraphName = b.tmpDir + '/' + self.theKaosModel + '.dot'

  def size(self):
    return len(self.theAssociations)

  def buildNode(self,dimName,objtName):
    if ((self.theKaosModel == 'template_usecase') and (dimName == 'usecase')):
      dimName = 'template_usecase'
    objtUrl = dimName + '#' + objtName
    b = Borg()
      
    if ((dimName == 'usecase') or (dimName == 'template_usecase')):
      self.theGraph.add_node(pydot.Node(objtName,shape='box',margin=0,fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
      if (objt.assumption() == True):
        objtLabel = "&lt;&lt;Assumption&gt;&gt;" + objtName 
      else:
        objtLabel = objtName
    if (self.theKaosModel == 'usecase'):
        fontColour = 'blue'
        nodeColour = 'blue'
      self.theGraph.add_node(pydot.Node(objtName,shape='box',margin=0,fontname=self.fontName,fontsize=self.fontSize,fontcolor=fontColour,color=nodeColour,URL=objtUrl))
    else:
      raise UnknownNodeType(dimName)


  def layout(self,renderer = ''):
    if (renderer == ''):
      if ((self.theKaosModel == 'usecase') or (self.theKaosModel == 'template_usecase')):
        renderer = 'dot'
      self.theGraph.write_xdot(self.theGraphName,prog=renderer)
    return open(self.theGraphName).read()


  def buildUsecaseModel(self):
    self.nodeNameSet = set([])
    edgeSet = set([])
    fontSize = '7.5'
    for association in self.theAssociations:
      UsecaseName = association.usecase()
      subUsecaseName = association.subUsecase()
      UsecaseDimName = association.UsecaseDimension()
      subUsecaseDimName = association.subUsecaseDimension()
      assocLabel = association.rationale()
      fontColour = 'black'
      edgeColour = 'black'
      edgeStyle = 'solid'
      assocDir = 'none'
      arrowHead = 'none'
      arrowTail = 'none'

      if (self.theUsecaseName != '' and UsecaseName not in self.nodeNameSet):
        self.buildNode(UsecaseDimName,UsecaseName)
        self.nodeNameSet.add(UsecaseName)
      if (self.theUsecaseName != '' and subUsecaseName not in self.nodeNameSet):
        self.buildNode(subUsecaseDimName,subUsecaseName)
        self.nodeNameSet.add(subUsecaseName)

        fontColour = 'blue'
        edgeColour = 'blue'
        arrowHead = 'empty'

      objtUrl = UsecaseDimName + '#' + subUsecaseDimName
      if ((subUsecaseName,UsecaseName,assocLabel) not in edgeSet):
        if (assocLabel == ''):
          assocLabel = ' '
        self.theGraph.add_edge(pydot.Edge(subUsecaseName,UsecaseName,style=edgeStyle,dir=assocDir,arrowhead=arrowHead,arrowtail=arrowTail,label=assocLabel,fontsize=fontSize,weight='1',fontcolor=fontColour,color=edgeColour,URL=objtUrl))
        edgeSet.add((subUsecaseName,UsecaseName,assocLabel))

  def graph(self):
    try:
      elements = []
      if (self.theKaosModel == 'usecase' and self.theUsecaseName == ''):
        elements = self.dbProxy.UsecaseModelElements(self.theEnvironmentName)

      for element in elements:
        self.buildNode(element[0],element[1])

      self.theKaosModel == 'usecase':
      self.buildUsecaseModel()
      return self.layout()
    except DatabaseProxyException as errTxt:
      raise ARMException(errTxt)

