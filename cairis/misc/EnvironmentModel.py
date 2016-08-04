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


import pydot
from cairis.core.ARM import *
from cairis.core.Borg import Borg
from cairis.core.colourcodes import threatColourCode
from cairis.core.colourcodes import threatLikelihoodColourCode
from cairis.core.colourcodes import vulnerabilitySeverityColourCode
from cairis.core.colourcodes import usabilityColourCode
from cairis.core.colourcodes import riskTextColourCode

USECASE_TYPE = 0
MISUSECASE_TYPE = 1

def arrayToAssetSecurityPropertiesTable(spArray,objtName):
  colorScheme = ["black","red","green","blue","yellow","cyan","purple","gray"]
  buf = '<<TABLE cellborder="1" border="0" cellspacing="2">'
  buf += '<TR><TD colspan="3">' + objtName + '</TD></TR>' 
  ci = 0 
  for x in spArray:
    if x != 0:
      i = x
      buf += '<TR>'
      while i > 0:
        buf += '<TD bgcolor="' + colorScheme[ci] + '"></TD>'
        i-= 1
      buf += '</TR>'
    ci += 1
  buf += '</TABLE>>'
  return buf

def arrayToThreatSecurityPropertiesTable(spArray,objtName):
  colorScheme = ["black","red","green","blue","yellow","cyan","purple","gray"]
  buf = '<<TABLE cellborder="0" border="0" cellspacing="2">'
  buf += '<TR><TD colspan="3">' + objtName + '</TD></TR>' 
  ci = 0 
  for x in spArray:
    if x != 0:
      if x == 1: buf += '<TR><TD></TD><TD></TD><TD bgcolor="' + colorScheme[ci] + '"></TD></TR>'
      elif x == 2: buf += '<TR><TD></TD><TD bgcolor="' + colorScheme[ci] + '" border="1"></TD><TD bgcolor="' + colorScheme[ci] + '" border="1"></TD></TR>'
      else: buf += '<TR><TD bgcolor="' + colorScheme[ci] + '" border="1"></TD><TD bgcolor="' + colorScheme[ci] + '" border="1"></TD><TD bgcolor="' + colorScheme[ci] + '" border="1"></TD></TR>'
    ci += 1
  buf += '</TABLE>>'
  return buf



class EnvironmentModel:
  def __init__(self,tlinks,environmentName,dp, fontName=None, fontSize=None):
    self.theTraceLinks = tlinks
    self.theEnvironmentName = environmentName
    self.dbProxy = dp
    self.theEnvironmentObject = self.dbProxy.dimensionObject(self.theEnvironmentName,'environment')
    self.theGraph = pydot.Dot()
    b = Borg()
    self.fontSize = fontSize or b.fontSize
    self.fontName = fontName or b.fontName
    self.theGraphName = b.tmpDir + '/pydotout.dot'

    self.theNodeLookup = {}

  def buildGraph(self):
    self.buildGraph()
 
  def size(self):
    return len(self.theTraceLinks)

  def buildNode(self,dimName,objtName):
    b = Borg()
    objtUrl = dimName + '#' + str(objtName)
    if (dimName == 'persona'):
      self.theGraph.add_node(pydot.Node(objtName,shapefile=b.staticDir + '/images/modelActor.png',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl,peripheries='0'))
    elif (dimName == 'tag'):
      self.theGraph.add_node(pydot.Node(objtName,shape='note',style='filled',pencolor='black',color='yellow',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'attacker'):
      self.theGraph.add_node(pydot.Node(objtName,shapefile=b.staticDir + '/images/modelAttacker.png',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl,peripheries='0'))
    elif (dimName == 'asset'):
      assetObjt = self.dbProxy.dimensionObject(objtName,'asset')
      borderColour = 'black'
      if (assetObjt.critical()):
        borderColour = 'red'
      self.theGraph.add_node(pydot.Node(objtName,shape='record',color=borderColour,fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl,width='0',height='0',margin='0',style='filled',fillcolor='white',label=arrayToAssetSecurityPropertiesTable(assetObjt.securityProperties(self.theEnvironmentName),objtName)))
    elif (dimName == 'threat'):
      thrObjt = self.dbProxy.dimensionObject(objtName,'threat')
      thrLhood = thrObjt.likelihood(self.theEnvironmentName,self.theEnvironmentObject.duplicateProperty(),self.theEnvironmentObject.overridingEnvironment())
      self.theGraph.add_node(pydot.Node(objtName,shape='record',style='filled',colorscheme='orrd5',color='black',fillcolor=threatLikelihoodColourCode(thrLhood),fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl,label=arrayToThreatSecurityPropertiesTable(thrObjt.securityProperties(self.theEnvironmentName),objtName)))
    elif (dimName == 'vulnerability'):
      vulObjt = self.dbProxy.dimensionObject(objtName,'vulnerability')
      vulSev = vulObjt.severity(self.theEnvironmentName,self.theEnvironmentObject.duplicateProperty(),self.theEnvironmentObject.overridingEnvironment())
      self.theGraph.add_node(pydot.Node(objtName,shape='record',style='filled',colorscheme='orrd4',color='black',fillcolor=vulnerabilitySeverityColourCode(vulSev),fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'risk'):
      riskObjt = self.dbProxy.dimensionObject(objtName,'risk')
      riskScores = self.dbProxy.riskScore(riskObjt.threat(),riskObjt.vulnerability(),self.theEnvironmentName,objtName)
      highestScore = 0
      for riskScore in riskScores:
        currentScore = riskScore[2]
        if (currentScore > highestScore):
          highestScore = currentScore
      self.theGraph.add_node(pydot.Node(objtName,shape='diamond',style='filled',color='black',fillcolor=threatColourCode(highestScore),fontcolor=riskTextColourCode(highestScore),fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'response'):
      self.theGraph.add_node(pydot.Node(objtName,shape='note',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'countermeasure'):
      self.theGraph.add_node(pydot.Node(objtName,shape='component',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'component'):
      self.theGraph.add_node(pydot.Node(objtName,shape='component',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'requirement'):
      self.theGraph.add_node(pydot.Node(objtName,shape='circle',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'goal'):
      self.theGraph.add_node(pydot.Node(objtName,shape='parallelogram',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'obstacle'):
      self.theGraph.add_node(pydot.Node(objtName,shape='polygon',skew='-1',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'role'):
      self.theGraph.add_node(pydot.Node(objtName,shapefile=b.staticDir + '/images/modelRole.png',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl,peripheries='0'))
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
      raise UnknownNodeType(dimName)

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
