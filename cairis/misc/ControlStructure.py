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

def edgeColour(dfType):
  if dfType == 'Control':
    return 'green'
  elif dfType == 'Feedback':
    return 'brown'
  else:
    return 'black'

class ControlStructure:
  def __init__(self,associations, envName,db_proxy=None,font_name=None, font_size=None):
    self.theAssociations = associations
    self.theEnvironmentName = envName
    self.fontName = font_name
    self.fontSize = font_size
    self.dbProxy = db_proxy

    b = Borg()

    if font_size is None or font_name is None:
      self.fontName = b.fontName
      self.fontSize = b.fontSize

    self.theGraph = pydot.Dot()
    self.theGraph.set_graph_defaults(rankdir='TB')
    self.theGraphName = b.tmpDir + '/' + 'cs.dot'

  def size(self):
    return len(self.theAssociations)

  def buildNode(self,dimName,objtName):
    
    if (dimName == 'entity'):
      objtUrl = 'asset#' + objtName
      self.theGraph.add_node(pydot.Node(objtName,shape='rectangle',margin=0,style='filled',fillcolor='white',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'trust_boundary'):
      objtUrl = 'trust_boundary#' + objtName
      self.theGraph.add_node(pydot.Node(objtName,shape='rectangle',margin=0,fillcolor='white',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    else:
      raise UnknownNodeType(dimName)

  def layout(self,renderer = 'dot'):
    self.theGraph.write_dot(self.theGraphName,prog=renderer)
    return open(self.theGraphName).read()

  def graph(self):
    try:
      nodeNameSet = set([])
      edgeSet = set([])

      for dfName,fromName,fromType,toName,toType,dfType in self.theAssociations:

        if (fromName not in nodeNameSet):
          self.buildNode(fromType,fromName)
          nodeNameSet.add(fromName)

        if (toName not in nodeNameSet):
          self.buildNode(toType,toName)
          nodeNameSet.add(toName)

        if ((fromName,toName) not in edgeSet):
          objtUrl = 'dataflow#' + dfName + '#' + self.theEnvironmentName
          df = pydot.Edge(fromName,toName,dir='forward',label=dfName,arrowhead='vee',color=edgeColour(dfType), fontname=self.fontName,fontsize=self.fontSize,fontcolor=edgeColour(dfType),URL=objtUrl)
          self.theGraph.add_edge(df)
      return self.layout()
    except DatabaseProxyException as errTxt:
      raise ARMException(errTxt)
