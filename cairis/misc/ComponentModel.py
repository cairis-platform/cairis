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

LOW_VALUE = 5
MED_VALUE =  10
HIGH_VALUE = 15

LOW_COLOR = "1" 
MED_COLOR = "2"
HIGH_COLOR = "3"

def resolveColour(cValue):
  if cValue <= LOW_VALUE:
    return LOW_COLOR
  elif cValue > LOW_VALUE and cValue < HIGH_VALUE:
    return MED_COLOR
  else:
    return HIGH_COLOR

class ComponentModel:
  def __init__(self,interfaces,connectors,db_proxy = None, font_name = None, font_size = None):
    self.theInterfaces = interfaces
    self.theConnectors = connectors
    self.theComponentNames = set([])
    self.theInterfaceNames = set([])
    self.dbProxy = db_proxy
    self.fontName = font_name
    self.fontSize = font_size
    self.theGraph = pydot.Dot()
    self.theGraph.set_graph_defaults(rankdir='LR')

    b = Borg()
    if font_size is None or font_name is None:
      self.fontName = b.fontName
      self.fontSize = b.fontSize

    self.theGraph.set_node_defaults(shape="rectangle",pencolor="black",style="filled",colorscheme="reds3",fontname=self.fontName,fontsize=self.fontSize);
    self.theGraph.set_edge_defaults(dir="both",arrowhead="obox",arrowtail="obox",weight="1");
    self.theGraphName = b.tmpDir + '/component.dot'

    for componentName,interfaceName,reqId in interfaces:
      self.buildInterface(componentName,interfaceName,reqId)

    for cnName,fromName,fromRole,fromIF,toName,toIF,toRole,assetName,pName,arName in connectors:
      self.buildConnector(cnName,fromName,toName,pName,arName)

  def size(self):
    return len(self.theConnectors)

  def buildInterface(self,componentName,interfaceName,reqId):
    componentUrl = 'component#' + componentName
    if componentName not in self.theComponentNames:
      self.theComponentNames.add(componentName)
      componentLabel = "<<component>>\\n" + componentName
      self.theGraph.add_node(pydot.Node(componentName,label=componentLabel,margin=0,fillcolor=resolveColour(self.dbProxy.componentAttackSurface(componentName)),URL=componentUrl))

  def buildConnector(self,cnName,fromName,toName,protocolName,arName):
    fromObjtName = fromName
    toObjtName = toName 
    lbl = "\<<" + protocolName + "\>>"
    urlName = 'connector#' + toObjtName + '_' + fromObjtName

    self.theGraph.add_edge(pydot.Edge(fromObjtName,toObjtName,label=lbl,URL=urlName))

  def layout(self,renderer = ''):
    self.theGraph.write_xdot(self.theGraphName,prog='dot')
    return open(self.theGraphName).read()

  def graph(self):
    return self.layout()

