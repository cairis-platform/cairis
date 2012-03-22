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
import gtk
from Borg import Borg
from colourcodes import threatColourCode
from colourcodes import responseColourCode
from colourcodes import usabilityColourCode

USECASE_TYPE = 0
MISUSECASE_TYPE = 1

class EnvironmentModel:
  def __init__(self,tlinks,environmentName,dp):
    self.theTraceLinks = tlinks
    self.theEnvironmentName = environmentName
    self.dbProxy = dp
    self.theGraph = pydot.Dot()
    b = Borg()
    self.fontSize = b.fontSize
    self.fontName = b.fontName

    if (os.name == 'nt'):
      self.theGraphName = 'C:\\arm\pydotout.dot'
    elif (os.uname()[0] == 'Linux'):
      self.theGraphName = '/tmp/pydotout.dot'
    elif (os.uname()[0] == 'Darwin'):
      self.theGraphName = '/tmp/pydotout.dot'
    else :
      raise ARM.UnsupportedOperatingSystem(os.name)

    self.theNodeLookup = {}

  def buildGraph(self):
    self.buildGraph()
 
  def size(self):
    return len(self.theTraceLinks)

  def buildNode(self,dimName,objtName):
    objtUrl = dimName + '#' + str(objtName)
    if (dimName == 'persona'):
      self.theGraph.add_node(pydot.Node(objtName,shape='circle',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'attacker'):
      self.theGraph.add_node(pydot.Node(objtName,shape='circle',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'asset'):
      assetObjt = self.dbProxy.dimensionObject(objtName,'asset')
      borderColour = 'black'
      if (assetObjt.critical()):
        borderColour = 'red'
      self.theGraph.add_node(pydot.Node(objtName,shape='record',color=borderColour,fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'threat'):
      self.theGraph.add_node(pydot.Node(objtName,shape='record',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'vulnerability'):
      self.theGraph.add_node(pydot.Node(objtName,shape='record',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'risk'):
      riskObjt = self.dbProxy.dimensionObject(objtName,'risk')
      riskScores = self.dbProxy.riskScore(riskObjt.threat(),riskObjt.vulnerability(),self.theEnvironmentName,objtName)
      highestScore = 0
      for riskScore in riskScores:
        currentScore = riskScore[2]
        if (currentScore > highestScore):
          highestScore = currentScore
      self.theGraph.add_node(pydot.Node(objtName,shape='diamond',style='filled',color=threatColourCode(highestScore),fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'response'):
      self.theGraph.add_node(pydot.Node(objtName,shape='note',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'countermeasure'):
      self.theGraph.add_node(pydot.Node(objtName,shape='component',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'requirement'):
      self.theGraph.add_node(pydot.Node(objtName,shape='circle',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'goal'):
      self.theGraph.add_node(pydot.Node(objtName,shape='parallelogram',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'obstacle'):
      self.theGraph.add_node(pydot.Node(objtName,shape='polygon',skew='-1',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'role'):
      self.theGraph.add_node(pydot.Node(objtName,shape='circle',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'responsibility'):
      self.theGraph.add_node(pydot.Node(objtName,shape='doubleoctagon',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'environment'):
      self.theGraph.add_node(pydot.Node(objtName,shape='doublecircle',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'domainproperty'):
      self.theGraph.add_node(pydot.Node(objtName,shape='house',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'inconsistency'):
      self.theGraph.add_node(pydot.Node(objtName,shape='polygon',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'task'):
      taskScore = self.dbProxy.taskUsabilityScore(objtName,self.theEnvironmentName)
      self.theGraph.add_node(pydot.Node(objtName,shape='ellipse',style='filled',color=usabilityColourCode(taskScore),fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))

    elif (dimName == 'misusecase'):
      self.theGraph.add_node(pydot.Node(objtName,shape='ellipse',fontname=self.fontName,fontsize=self.fontSize,style='filled',color='black',fontcolor='white',URL=objtUrl))
    else: 
      raise ARM.UnknownNodeType(dimName)

  def graph(self):
    self.nodeNameSet = set([])
    self.dimNameSet = set([])

#    envReqs = self.dbProxy.getDimensionNames('requirement',self.theEnvironmentName)
#    for envReq in envReqs:
#      self.buildNode('requirement',envReq)
#      self.nodeNameSet.add(envReq)

    for dotLink in self.theTraceLinks:
      fromDimName = dotLink.fromObject()
      self.dimNameSet.add(fromDimName)
      fromName = dotLink.fromName()
      if (fromName not in self.nodeNameSet):
        self.buildNode(fromDimName,fromName)
        self.nodeNameSet.add(fromName)
        self.theNodeLookup[fromName] = fromDimName + ' ' + dotLink.fromName()
      toDimName = dotLink.toObject()
      self.dimNameSet.add(toDimName)
      toName = dotLink.toName()
      if (toName not in self.nodeNameSet):
        self.buildNode(toDimName,toName)
        self.nodeNameSet.add(toName)
        self.theNodeLookup[toName] = toDimName + ' ' + dotLink.toName()
      edge = pydot.Edge(str(fromName),str(toName),dir='none',URL=fromDimName + '#' + toDimName)
      self.theGraph.add_edge(edge)
    return self.layout()

  def layout(self,renderer = 'fdp'):
    self.theGraph.write_xdot(self.theGraphName,prog=renderer)
    return open(self.theGraphName).read()

  def dimensions(self):
    return self.listStore(self.dimNameSet)

  def objects(self):
    return self.listStore(self.nodeNameSet)

  def listStore(self,unsortedSet):
    modelList = list(unsortedSet)
    modelList.sort(key=str.lower) 
    model = gtk.ListStore(str)
    model.append([''])
    for dim in modelList:
      model.append([dim])
    return model
