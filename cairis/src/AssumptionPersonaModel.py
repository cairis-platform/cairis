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


import DotTrace
import pydot
import wx
import os
import ARM
from Borg import Borg

class AssumptionPersonaModel:
  def __init__(self,tlinks):
    self.theTraceLinks = tlinks
    b = Borg()
    self.dbProxy = b.dbProxy
    self.fontName = b.fontName
    self.fontSize = b.apFontSize
    self.theGraph = pydot.Dot()
    if (os.name == 'nt'):
      self.theGraphName = 'C:\\arm\\ap.dot'
    elif (os.uname()[0] == 'Linux'):
      self.theGraphName = '/tmp/ap.dot'
    elif (os.uname()[0] == 'Darwin'):
      self.theGraphName = '/tmp/ap.dot'
    else :
      raise ARM.UnsupportedOperatingSystem(os.name)
    self.theGraph.set_graph_defaults(rankdir='LR')

    self.theNodeLookup = {}

  def buildGraph(self):
    self.buildGraph()
 
  def size(self):
    return len(self.theTraceLinks)

  def buildNode(self,dimName,objtName):
    objtUrl = dimName + '#' + str(objtName)
    if (dimName == 'persona'):
      self.theGraph.add_node(pydot.Node(objtName,shape='circle',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'persona_characteristic'):
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
      self.theGraph.add_node(pydot.Node(objtName,shape='point',fontname=self.fontName,label='',fontsize=self.fontSize,URL=objtUrl))

  def graph(self):
    self.nodeNameSet = set([])
    self.dimNameSet = set([])
    self.personaNames = set([])
    self.personaCharacteristics = set([])
    self.behaviouralVariableTypes = set([])

    for fromName,fromDim,toName,toDim,personaName,bvName,pcName in self.theTraceLinks:
      self.personaNames.add(personaName)
      self.behaviouralVariableTypes.add(bvName)
      self.personaCharacteristics.add(pcName)

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

  def personas(self):
    return self.listStore(self.personaNames)

  def characteristics(self):
    return self.listStore(self.personaCharacteristics)

  def behaviouralVariables(self):
    return self.listStore(self.behaviouralVariableTypes)

  def listStore(self,unsortedSet):
    modelList = list(unsortedSet)
    modelList.sort(key=str.lower)
    import gtk
    model = gtk.ListStore(str)
    model.append([''])
    for dim in modelList:
      model.append([dim])
    return model

