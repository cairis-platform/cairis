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

class AssumptionTaskModel:
  def __init__(self,tlinks,db_proxy = None, font_name = None, font_size = None):
    self.theTraceLinks = tlinks
    self.dbProxy = db_proxy
    self.fontName = font_name
    self.fontSize = font_size
    self.theGraph = pydot.Dot()
    b = Borg()
    self.theGraphName = b.tmpDir + '/at.dot'
    self.theGraph.set_graph_defaults(rankdir='LR')

    self.theNodeLookup = {}

  def buildGraph(self):
    self.buildGraph()
 
  def size(self):
    return len(self.theTraceLinks)

  def buildNode(self,dimName,objtName):
    objtUrl = dimName + '#' + str(objtName)
    if (dimName == 'task'):
      self.theGraph.add_node(pydot.Node(objtName,shape='ellipse',margin=0,fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'domainproperty'):
      self.theGraph.add_node(pydot.Node(objtName,shape='house',margin=0,fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'task_characteristic'):
      self.theGraph.add_node(pydot.Node(objtName,shape='record',margin=0,fontname=self.fontName,style='filled',fillcolor='green',fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'rebuttal'):
      self.theGraph.add_node(pydot.Node(objtName,shape='record',margin=0,fontname=self.fontName,style='filled',fillcolor='red',fontcolor='white',fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'qualifier'):
      self.theGraph.add_node(pydot.Node(objtName,shape='rectangle',margin=0,fontname=self.fontName,style='dashed',fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'warrant'):
      self.theGraph.add_node(pydot.Node(objtName,shape='record',margin=0,fontname=self.fontName,style='filled',fillcolor='darkslategray3',fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'backing'):
      self.theGraph.add_node(pydot.Node(objtName,shape='record',margin=0,fontname=self.fontName,style='filled',fillcolor='gray95',fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'grounds'):
      self.theGraph.add_node(pydot.Node(objtName,shape='record',margin=0,fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    else: 
      self.theGraph.add_node(pydot.Node(objtName,shape='point',fontname=self.fontName,label='',fontsize=self.fontSize))

  def graph(self):
    self.nodeNameSet = set([])
    self.dimNameSet = set([])
    self.taskNames = set([])
    self.taskCharacteristics = set([])
    edges = set([])

    for fromName,fromDim,toName,toDim,taskName,tcName in self.theTraceLinks:
      self.taskNames.add(taskName)
      self.taskCharacteristics.add(tcName)

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
      if ((fromName,toName) not in edges):
        edges.add((fromName,toName)) 
        edge = pydot.Edge(str(fromName),str(toName))
        self.theGraph.add_edge(edge)
    return self.layout()

  def layout(self,renderer = 'dot'):
    self.theGraph.write_xdot(self.theGraphName,prog=renderer)
    return open(self.theGraphName).read()

  def tasks(self):
    return self.listStore(self.taskNames)

  def characteristics(self):
    return self.listStore(self.taskCharacteristics)

  def listStore(self,unsortedSet):
    modelList = list(unsortedSet)
    modelList.sort(key=str.lower) 
    model = gtk.ListStore(str)
    model.append([''])
    for dim in modelList:
      model.append([dim])
    return model
