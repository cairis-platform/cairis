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
import gtk
from cairis.core.colourcodes import threatColourCode
from cairis.core.colourcodes import riskTextColourCode

__author__ = 'Shamal Faily'

class LocationModel:
  def __init__(self,locsName,envName,riskOverlay):
    b = Borg()
    locsId = b.dbProxy.getDimensionId(locsName,'locations')
    self.theLocs = (b.dbProxy.getLocations(locsId))[locsName]
    self.theEnvironmentName = envName
    self.theGraph = pydot.Dot()
    self.fontName = b.fontName
    self.fontSize = b.fontSize
    self.theGraph.set_graph_defaults(rankdir='LR')
    self.theGraph.set_node_defaults(shape='rectangle',fontname=self.fontName,fontsize=self.fontSize)
    self.nodeList= set([])
    self.theGraphName = b.tmpDir + '/location.dot'
    self.theOverlayTraces = riskOverlay

  def size(self):
    return len(self.theAssociations)

  def layout(self,renderer = 'dot'):
    self.theGraph.write_xdot(self.theGraphName,prog=renderer)
    return open(self.theGraphName).read()

  def graph(self):

    for location in self.theLocs.locations():
      locName = location.name()
      assetInstances = location.assetInstances()
      personaInstances = location.personaInstances()

      locCluster = pydot.Cluster(locName,label=locName,URL='location#' + locName)
      locCluster.add_node(pydot.Node('point_' + locName,label='',shape="none",fontcolor="white",URL='location#' + locName))
      for inst in assetInstances:
        instName = inst[0]
        assetName = inst[1] 
        locCluster.add_node(pydot.Node(instName,URL='asset#' + assetName))

      for persona in personaInstances:
        instName = persona[0]
        personaName = persona[1] 
        locCluster.add_node(pydot.Node(instName,shape='circle',URL='persona#' + personaName))
      self.theGraph.add_subgraph(locCluster)

    for edges in self.theLocs.links():
      self.theGraph.add_edge(pydot.Edge('point_' + edges[0],'point_' + edges[1],arrowhead='none',arrowtail='none',dir='both'))

    edgeList = set([])
    b = Borg()
    risks = set([])
    for trace in self.theOverlayTraces:
      riskName = trace.fromName()
      locName = trace.toName()
      if (riskName,locName) not in edgeList:
        edgeList.add((riskName,locName))

      if riskName not in risks:
        risks.add(riskName)
        riskObjt = b.dbProxy.dimensionObject(riskName,'risk')
        riskScores = b.dbProxy.riskScore(riskObjt.threat(),riskObjt.vulnerability(),self.theEnvironmentName,riskName)
        highestScore = 0
        for riskScore in riskScores:
          currentScore = riskScore[2]
          if (currentScore > highestScore):
            highestScore = currentScore
        self.theGraph.add_node(pydot.Node(riskName,shape='diamond',style='filled',color=threatColourCode(highestScore),fontcolor=riskTextColourCode(highestScore),fontname=self.fontName,fontsize=self.fontSize,URL='risk#'+riskName))

    for edges in edgeList:
      self.theGraph.add_edge(pydot.Edge(edges[0],'point_' + edges[1]))
    return self.layout()
