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

class CodeNetworkModel:
  def __init__(self,codeNetwork,personaName,graphName = 'codenetwork'):
    self.theCodeNetwork = codeNetwork
    self.thePersonaName = personaName
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theGraph = pydot.Dot()
    self.theGraph.set_graph_defaults(rankdir='LR')
    self.theGraph.set_node_defaults(shape='rectangle',style='filled',color='gray')
    self.theGraph.set_edge_defaults(arrowhead='vee',dir='both',arrowtail='none')
    self.theGraphName = b.tmpDir + '/' + graphName + '.dot'
    self.theGraphImage = b.tmpDir + '/' + graphName + '.png'

  def buildNode(self,objtName,codeType):
    typeColour = 'gray'
    if codeType == 'context':
      typeColour = 'cadetblue1'
    self.theGraph.add_node(pydot.Node(objtName,color=typeColour))

  def graph(self):
    self.nodeNameSet = set([])
    for fromName,fromType,toName,toType,rType in self.theCodeNetwork:
      if (fromName not in self.nodeNameSet):
        self.buildNode(fromName,fromType)
        self.nodeNameSet.add(fromName)
      if (toName not in self.nodeNameSet):
        self.buildNode(toName,toType)
        self.nodeNameSet.add(toName)

      rTypeLabel = ''
      if rType == 'associated':
        rTypeLabel = '=='
      elif rType == 'implies':
        rTypeLabel = '=>'
      elif rType == 'conflict':
        rTypeLabel = '<>'
      elif rType == 'part-of':
        rTypeLabel = '<>'

      tailLabel = 'none'
      if rTypeLabel == '==' or rTypeLabel == '<>':
        tailLabel = 'vee'
      edge = pydot.Edge(fromName,toName,arrowtail=tailLabel,label=rTypeLabel)
      self.theGraph.add_edge(edge)
    self.theGraph.write_png(self.theGraphImage,prog='dot')
