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

class ComponentModel:
  def __init__(self,interfaces,associations):
    self.theInterfaces = interfaces
    self.theAssociations = associations
    self.theComponentNames = set([])
    self.theInterfaceNames = set([])

    b = Borg()
    self.dbProxy = b.dbProxy
    self.fontName = b.fontName
    self.fontSize = b.fontSize
    self.theGraph = pydot.Dot()
    self.theGraph.set_graph_defaults(rankdir='LR')
    self.theGraphName = b.tmpDir + '/component.dot'

    for componentName,interfaceName,reqId in interfaces:
      self.buildInterface(componentName,interfaceName,reqId)

    for fromName,fromIF,toName,toIF in associations:
      self.buildAssociation(fromName,fromIF,toName,toIF)

  def size(self):
    return len(self.theAssociations)

  def buildInterface(self,componentName,interfaceName,reqId):
    componentUrl = 'component#' + componentName
    if componentName not in self.theComponentNames:
      self.theComponentNames.add(componentName)
      componentLabel = "<<component>>\\n" + componentName
      self.theGraph.add_node(pydot.Node(componentName,label=componentLabel,shape='rectangle',fontname=self.fontName,fontsize=self.fontSize,URL=componentUrl))

    if interfaceName not in self.theInterfaceNames:
      self.theInterfaceNames.add(interfaceName)
      objtName = componentName + '_' + interfaceName
      interfaceUrl = ''
      if reqId == 1:
        interfaceUrl = 'required_interface#'
      else:
        interfaceUrl = 'provided_interface#'
      interfaceUrl += objtName
      self.theGraph.add_node(pydot.Node(objtName,shape='circle',label='',width='.2',height='.2',fontname=self.fontName,fontsize=self.fontSize,URL=interfaceUrl))

    self.theGraph.add_edge(pydot.Edge(componentName,objtName,arrowhead='none',arrowtail='obox',dir='both',weight='1'))

  def buildAssociation(self,fromName,fromInterface,toName,toInterface):
    fromObjtName = fromName + '_' + fromInterface
    toObjtName = toName + '_' + toInterface
    self.theGraph.add_edge(pydot.Edge(fromObjtName,toObjtName,dir='none',weight='1'))

  def layout(self,renderer = ''):
    self.theGraph.write_xdot(self.theGraphName,prog='dot')
    return open(self.theGraphName).read()

  def graph(self):
    return self.layout()

