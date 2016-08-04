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


import cairis.core.DotTrace
import pydot
import os
from cairis.core.ARM import *
from cairis.core.Borg import Borg

__author__ = 'Shamal Faily'

class PersonaModel:
  def __init__(self,tlinks,font_name = None, font_size = None):
    self.theTraceLinks = tlinks
    b = Borg()
    self.dbProxy = b.dbProxy
    self.fontName = font_name or b.fontName
    self.fontSize = font_size or b.fontSize
    self.theGraph = pydot.Dot()
    self.theGraphName = b.tmpDir + '/ap.dot'
    self.theGraph.set_graph_defaults(rankdir='LR')

    self.theNodeLookup = {}

  def buildGraph(self):
    self.buildGraph()
 
  def size(self):
    return len(self.theTraceLinks)

  def buildNode(self,dimName,objtName):
    objtUrl = dimName + '#' + str(objtName)
    b = Borg()
    if (dimName == 'persona'):
      self.theGraph.add_node(pydot.Node(objtName,shapefile=b.staticDir + '/images/modelActor.png',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl,peripheries='0'))
    elif (dimName == 'persona_characteristic'):
      self.theGraph.add_node(pydot.Node(objtName,shape='record',fontname=self.fontName,style='filled',fillcolor='green',fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'implied_characteristic'):
      self.theGraph.add_node(pydot.Node(objtName,shape='record',fontname=self.fontName,style='filled',fillcolor='green',fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'rebuttal'):
      self.theGraph.add_node(pydot.Node(objtName,shape='record',fontname=self.fontName,style='filled',fillcolor='red',fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'qualifier'):
      self.theGraph.add_node(pydot.Node(objtName,shape='rectangle',fontname=self.fontName,style='dashed',fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'warrant'):
      self.theGraph.add_node(pydot.Node(objtName,shape='record',fontname=self.fontName,style='filled',fillcolor='darkslategray3',fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'backing'):
      self.theGraph.add_node(pydot.Node(objtName,shape='record',fontname=self.fontName,style='filled',fillcolor='gray95',fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'grounds'):
      self.theGraph.add_node(pydot.Node(objtName,shape='record',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    else: 
      self.theGraph.add_node(pydot.Node(objtName,shape='point',fontname=self.fontName,label=' ',fontsize=self.fontSize,URL=objtUrl))

  def graph(self):
    self.nodeNameSet = set([])
    self.dimNameSet = set([])

    for fromName,fromDim,toName,toDim,personaName,bvName,pcName in self.theTraceLinks:
      self.dimNameSet.add(fromDim)
      if (fromName not in self.nodeNameSet):
        self.buildNode(fromDim,fromName)
        self.nodeNameSet.add(fromName)
        self.theNodeLookup[fromName] = fromDim + ' ' + fromName
      self.dimNameSet.add(toDim)
      if (toName not in self.nodeNameSet):
        self.buildNode(toDim,toName)
        self.nodeNameSet.add(toName)
        self.theNodeLookup[toName] = toDim + ' ' + toName
      edge = pydot.Edge(str(fromName),str(toName),URL=fromDim + '#' + toDim)
      self.theGraph.add_edge(edge)
    return self.layout()

  def layout(self,renderer = 'dot'):
    self.theGraph.write_xdot(self.theGraphName,prog=renderer)
    return open(self.theGraphName).read()
