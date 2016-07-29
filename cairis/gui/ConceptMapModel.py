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

from cairis.core.Borg import Borg
import cairis.core.DotTrace
import pydot
import wx
import os
from cairis.core.ARM import *
import gtk

__author__ = 'Shamal Faily'

class ConceptMapModel:
  def __init__(self,associations,envName,conceptName = '',cfSet = False):
    self.theAssociations = associations
    self.theEnvironmentName = envName
    self.theConceptName = conceptName
    b = Borg()
    self.dbProxy = b.dbProxy
    self.fontName = b.fontName
    self.fontSize = b.fontSize
    self.theGraph = pydot.Dot()
    self.theGraph.set_graph_defaults(rankdir='LR')
    if (cfSet == True):
      self.theGraph.set_node_defaults(shape='ellipse',colorscheme='set14',color='1',fontname=self.fontName,fontsize=self.fontSize,style='filled')
    else:
      self.theGraph.set_node_defaults(shape='rectangle',colorscheme='spectral3',color='1',fontname=self.fontName,fontsize=self.fontSize)
    self.theGraph.set_edge_defaults(arrowhead='vee')
    self.cfSet = cfSet
    self.theClusters = {}
    self.theEdges = []
    self.theGraphName = b.tmpDir + '/concept.dot'

  def size(self):
    return len(self.theAssociations)

  def buildNode(self,objtName,envName):
    objtUrl = 'requirement#' + objtName
    envLabel = envName.replace(' ','_')
    if envName not in self.theClusters:
      self.theClusters[envName] = pydot.Cluster(envLabel,label=str(envName))
    reqObjt = self.dbProxy.dimensionObject(objtName,'requirement')
    tScore = self.dbProxy.traceabilityScore(objtName)
    fontColour = 'black'
    if (reqObjt.priority() == 1):
      if tScore != 3: fontColour = 1

    n = pydot.Node(objtName,color=str(tScore),fontcolor=str(fontColour),URL=objtUrl)
    if (self.cfSet == False):
      n.obj_dict['attributes']['style'] = '"rounded,filled"'
    self.theClusters[envName].add_node(n)

  def layout(self,renderer = 'dot'):
    self.theGraph.write_xdot(self.theGraphName,prog=renderer)
    return open(self.theGraphName).read()

  def graph(self):
    self.conceptNameSet = set([])
    self.assocSet = set([])

    reqNodes = self.dbProxy.getDimensionNames('requirement',self.theEnvironmentName)
    for nodeName in reqNodes:
      self.buildNode(nodeName,self.theEnvironmentName)
      self.conceptNameSet.add(nodeName)
    
    for association in self.theAssociations:
      fromName = association.fromName()
      toName = association.toName()
      lbl = association.label()
      fromEnv = association.fromEnvironment()
      toEnv = association.toEnvironment()
      if (fromName not in self.conceptNameSet):
        self.buildNode(fromName,fromEnv)
        self.conceptNameSet.add(fromName)
      if (toName not in self.conceptNameSet):
        self.buildNode(toName,toEnv)
        self.conceptNameSet.add(fromName)

      conceptTriple = (fromName,toName,lbl)
      if (conceptTriple not in self.assocSet):
        self.theEdges.append(pydot.Edge(str(fromName),str(toName),label=str(lbl), fontname=self.fontName,fontsize=self.fontSize, arrowhead='vee',URL=fromName+ '#' + toName))

    for envName in self.theClusters:
      self.theGraph.add_subgraph(self.theClusters[envName])
    for edge in self.theEdges:
      self.theGraph.add_edge(edge)
    return self.layout()
