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
import os
from cairis.core.ARM import *

__author__ = 'Shamal Faily'

class ConceptMapModel:
  def __init__(self,associations,envName = 'all',conceptName = 'all', isAsset = False, cfSet = False,db_proxy=None, font_name=None,font_size=None):
    self.theAssociations = associations
    self.theEnvironmentName = envName
    self.theConceptName = conceptName
    if (isAsset == True):
      self.theRequirementsDimension = 'asset'
    else:
      self.theRequirementsDimension = 'environment'
    self.isAsset = isAsset
    self.dbProxy = db_proxy
    self.fontName = font_name
    self.fontSize = font_size
    self.theGraph = pydot.Dot()
    self.theGraph.set_graph_defaults(rankdir='LR')
    b = Borg()
    if font_size is None or font_name is None:
      self.fontName = b.fontName
      self.fontSize = b.fontSize

    if (cfSet == True):
      self.theGraph.set_node_defaults(shape='circle',colorscheme='set14',color='1',fontname=self.fontName,fontsize=self.fontSize)
    else:
      self.theGraph.set_node_defaults(shape='rectangle',colorscheme='spectral3',color='1',fontname=self.fontName,fontsize=self.fontSize)
    self.theGraph.set_edge_defaults(arrowhead='vee')
    self.cfSet = cfSet
    self.theClusters = {}
    self.theEdges = []
    self.theGraphName = b.tmpDir + '/concept.dot'

  def size(self):
    return len(self.theAssociations)

  def buildNode(self,objtName):
    objtUrl = 'requirement#' + objtName
    reqObjt = self.dbProxy.dimensionObject(objtName,'requirement')
    refName = reqObjt.domain()
    refLabel = refName.replace(' ','_')
    if refName not in self.theClusters:
      self.theClusters[refName] = pydot.Cluster(refLabel,label=str(refName))
    tScore = self.dbProxy.traceabilityScore(objtName)
    fontColour = 'black'
    if (reqObjt.priority() == 1):
      if tScore != 3: fontColour = 1
    n = pydot.Node(objtName,color=str(tScore),margin=0,fontcolor=str(fontColour),fontsize='5',URL=objtUrl)
    if (self.cfSet == False):
      n.obj_dict['attributes']['style'] = '"rounded,filled"'
    self.theClusters[refName].add_node(n)

  def layout(self,renderer = 'dot'):
    self.theGraph.write_xdot(self.theGraphName,prog=renderer)
    return open(self.theGraphName).read()

  def graph(self):
    self.conceptNameSet = set([])
    self.assocSet = set([])

    if ((self.theEnvironmentName == 'all') and (self.theConceptName == 'all')):
      reqNodes = self.dbProxy.getDimensionNames('requirement','')
      for nodeName in reqNodes:
        self.buildNode(nodeName)
        self.conceptNameSet.add(nodeName)
    elif self.theConceptName == 'all':
      reqNodes = self.dbProxy.dimensionRequirements(self.theRequirementsDimension,self.theEnvironmentName)
      for nodeName in reqNodes:
        self.buildNode(nodeName)
        self.conceptNameSet.add(nodeName)
    else:
      self.buildNode(self.theConceptName)
      self.conceptNameSet.add(self.theConceptName)

    
    for association in self.theAssociations:
      fromName = association.fromName()
      toName = association.toName()
      lbl = association.label()
      fromEnv = association.fromEnvironment()
      toEnv = association.toEnvironment()
      if (fromName not in self.conceptNameSet):
        self.buildNode(fromName)
        self.conceptNameSet.add(fromName)
      if (toName not in self.conceptNameSet):
        self.buildNode(toName)
        self.conceptNameSet.add(fromName)

      conceptTriple = (fromName,toName,lbl)
      if (conceptTriple not in self.assocSet):
        self.theEdges.append(pydot.Edge(str(fromName),str(toName),label=str(lbl), fontname=self.fontName,fontsize=self.fontSize, arrowhead='vee',URL=fromName+ '#' + toName))

    for envName in self.theClusters:
      self.theGraph.add_subgraph(self.theClusters[envName])
    for edge in self.theEdges:
      self.theGraph.add_edge(edge)
    return self.layout()
