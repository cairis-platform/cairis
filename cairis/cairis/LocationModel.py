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


from Borg import Borg
import DotTrace
import pydot
import os
import gtk

class LocationModel:
  def __init__(self,locsName):
    b = Borg()
    self.theLocs = b.dbProxy.getLocations(locsName)
    self.theGraph = pydot.Dot()
    self.fontName = b.fontName
    self.fontSize = b.fontSize
    self.theGraph.set_node_defaults(shape='rectangle',fontname=self.fontName,fontsize=self.fontSize)
    self.nodeList= set([])
    self.theGraphName = b.tmpDir + '/location.dot'

  def size(self):
    return len(self.theAssociations)

  def layout(self,renderer = 'dot'):
    self.theGraph.write_xdot(self.theGraphName,prog=renderer)
    return open(self.theGraphName).read()

  def graph(self):
    locs = self.theLocs[2]
    edgeList = set([])

    for location in locs:
      locName = location[0]
      assetInstances = location[1]
      personaInstances = location[2]
      locLinks = location[3]

      for linkLoc in locLinks:
        if ((linkLoc,locName) not in edgeList) and ((locName,linkLoc) not in edgeList):
          edgeList.add((linkLoc,locName))
      
      locCluster = pydot.Cluster(locName,label=locName)
      locCluster.add_node(pydot.Node('point_' + locName,shape="none",fontcolor="white"))
      for inst in assetInstances:
        instName = inst[0]
        assetName = inst[1] 
        locCluster.add_node(pydot.Node(instName,URL=assetName + '#' + instName))

      for personaName in personaInstances:
        instName = inst[0]
        personaName = inst[1] 
        locCluster.add_node(pydot.Node(instName,shape='circle',URL=personaName + '#' + instName))
      self.theGraph.add_subgraph(locCluster)

    for edges in edgeList:
      self.theGraph.add_edge(pydot.Edge('point_' + edges[0],'point_' + edges[1],arrowhead='none',arrowtail='none',dir='both'))
    return self.layout()
