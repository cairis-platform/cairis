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
import wx
import os
import ARM
import gtk

class ContextModel:
  def __init__(self,associations,envName = ''):
    self.theAssociations = associations
    self.theEnvironmentName = envName
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theGraph = pydot.Dot()
    self.theGraphName = b.tmpDir + '/context.dot'
    self.theGraph.set_graph_defaults(rankdir='LR')

  def size(self):
    return len(self.theAssociations)

  def buildNode(self,objtType,objtName):
    objtUrl = objtType + '#' + objtName
    if (objtType == 'machine'):
      self.theGraph.add_node(pydot.Node(objtName,label = '\r ' + objtName,shape='record',fontsize='10',URL=objtUrl))
    else:
      self.theGraph.add_node(pydot.Node(objtName,shape='record',fontsize='10',URL=objtUrl))

  def layout(self,renderer = 'dot'):
    self.theGraph.write_xdot(self.theGraphName,prog=renderer)
    return open(self.theGraphName).read()

  def graph(self):
    try:
      domains = self.dbProxy.contextModelElements(self.theEnvironmentName)
      for domain in domains:
        self.buildNode(domain[0],domain[1])

      edgeList = set([])
      for association in self.theAssociations:
        headName = association.headDomain()
        tailName = association.tailDomain()
        connectionDomain = association.connectionDomain()
        if (connectionDomain == ''):
          edge = pydot.Edge(headName,tailName,label=association.phenomena(),dir='none',fontsize='5.0')
          self.theGraph.add_edge(edge)
          edgeList.add((headName,tailName))
        else:
          objtUrl = 'connection#' + headName + connectionDomain + tailName
          self.theGraph.add_node(pydot.Node(objtUrl,label='',shape='point',fontsize='1',URL=objtUrl))
          edge1 = pydot.Edge(headName,objtUrl,label=association.phenomena(),dir='none',fontsize='5.0')
          edgeList.add((headName,objtUrl))
          self.theGraph.add_edge(edge1)
          edge2 = pydot.Edge(objtUrl,connectionDomain,label='',dir='none',fontsize='5.0')
          edgeList.add((objtUrl,connectionDomain))
          self.theGraph.add_edge(edge2)
          edge3 = pydot.Edge(objtUrl,tailName,label='',dir='none',fontsize='5.0')
          edgeList.add((objtUrl,tailName))
          self.theGraph.add_edge(edge3)
      return self.layout()
    except ARM.DatabaseProxyException, errTxt:
      raise ARM.ARMException(errTxt)
