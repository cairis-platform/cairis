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
from cairis.core.colourcodes import usabilityTextColourCode
from cairis.core.colourcodes import probabilityTextColourCode
from cairis.core.colourcodes import obstacleColourCode
from cairis.core.colourcodes import riskTextColourCode
from cairis.core.colourcodes import threatTextColour
from cairis.core.colourcodes import vulnerabilityTextColour

USECASE_TYPE = 0
MISUSECASE_TYPE = 1

def arrayToAssetSecurityPropertiesTable(spArray,objtName):
  colorScheme = ["black","red","green","blue","yellow","cyan","purple","gray"]
  buf = '<<TABLE cellborder="1" border="1" cellspacing="2">'
  buf += '<TR><TD colspan="3" bgcolor="white" border="0" align="center">' + objtName + '</TD></TR>' 
  ci = 0 
  for x in spArray:
    if x == 0:
      buf += '<TR><TD border="0"></TD></TR>'
    else:
      buf += '<TR><TD bgcolor="' + colorScheme[ci] + '" colspan="' + str(x) + '"></TD></TR>'
    ci += 1
  buf += '</TABLE>>'
  return buf

def arrayToThreatSecurityPropertiesTable(spArray,objtName):
  colorScheme = ["black","red","green","blue","yellow","cyan","purple","gray"]
  buf = '<<TABLE cellborder="1" border="0" cellspacing="2">'
  buf += '<TR><TD border="0" colspan="3">' + objtName + '</TD></TR>' 
  ci = 0 
  for x in spArray:
    if x == 0:
      buf += '<TR><TD border="0"></TD></TR>'
    else:
      if x == 1: buf += '<TR><TD border="0" colspan="2"></TD><TD bgcolor="' + colorScheme[ci] + '"></TD></TR>'
      elif x == 2: buf += '<TR><TD border="0" colspan="1"></TD><TD bgcolor="' + colorScheme[ci] + '" colspan="2"></TD></TR>'
      else: buf += '<TR><TD bgcolor="' + colorScheme[ci] + '" colspan="3"></TD></TR>'
    ci += 1
  buf += '</TABLE>>'
  return buf



class EnvironmentModel:
  def __init__(self,tlinks,environmentName,dp, modelLayout, fontName=None, fontSize=None,isTagged=False,rankDir='TB'):
    self.theTraceLinks = tlinks
    self.theEnvironmentName = environmentName
    self.dbProxy = dp
    self.theEnvironmentObject = self.dbProxy.dimensionObject(self.theEnvironmentName,'environment')
    self.theGraph = pydot.Dot()
    b = Borg()
    self.fontSize = fontSize or b.fontSize
    self.fontName = fontName or b.fontName
    self.theGraphName = b.tmpDir + '/pydotout.dot'
    self.theRenderer = modelLayout
    self.theGraph.set_graph_defaults(rankdir=rankDir)
    self.theNodeLookup = {}
    self.isTagged = isTagged

  def buildGraph(self):
    self.buildGraph()
 
  def size(self):
    return len(self.theTraceLinks)

  def buildNode(self,dimName,objtName):
    b = Borg()
    actorFile = b.assetDir + '/modelActor.png'
    attackerFile = b.assetDir + '/modelAttacker.png'
    roleFile = b.assetDir + '/modelRole.png'
    objtUrl = dimName + '#' + str(objtName)
    if (dimName == 'persona'):
      self.theGraph.add_node(pydot.Node(objtName,label='',xlabel=objtName,shapefile=actorFile,fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl,peripheries='0'))
    elif (dimName == 'tag'):
      self.theGraph.add_node(pydot.Node(objtName,shape='note',style='filled',margin=0,pencolor='black',color='yellow',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'attacker'):
      self.theGraph.add_node(pydot.Node(objtName,label='',xlabel=objtName,shapefile=attackerFile,fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl,peripheries='0'))
    elif (dimName == 'asset'):
      assetObjt = self.dbProxy.dimensionObject(objtName,'asset')
      borderColour = 'black'
      if (assetObjt.critical()):
        borderColour = 'red'
      self.theGraph.add_node(pydot.Node(objtName,shape='record',color=borderColour,margin=0,fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl,width='0',height='0',style='filled',pencolor='black',fillcolor='white',label=arrayToAssetSecurityPropertiesTable(assetObjt.securityProperties(self.theEnvironmentName),objtName)))
    elif (dimName == 'threat'):
      thrObjt = self.dbProxy.dimensionObject(objtName,'threat')
      thrLhood = thrObjt.likelihood(self.theEnvironmentName,self.theEnvironmentObject.duplicateProperty(),self.theEnvironmentObject.overridingEnvironment())
      self.theGraph.add_node(pydot.Node(objtName,shape='record',style='filled',margin=0,color='black',fontcolor=threatTextColour(thrLhood),fillcolor=threatLikelihoodColourCode(thrLhood),fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl,label=arrayToThreatSecurityPropertiesTable(thrObjt.securityProperties(self.theEnvironmentName),objtName)))
    elif (dimName == 'vulnerability'):
      vulObjt = self.dbProxy.dimensionObject(objtName,'vulnerability')
      vulSev = vulObjt.severity(self.theEnvironmentName,self.theEnvironmentObject.duplicateProperty(),self.theEnvironmentObject.overridingEnvironment())
      self.theGraph.add_node(pydot.Node(objtName,shape='record',style='filled',margin=0,colorscheme='orrd4',fontcolor=vulnerabilityTextColour(vulSev),fillcolor=vulnerabilitySeverityColourCode(vulSev),fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'risk'):
      riskObjt = self.dbProxy.dimensionObject(objtName,'risk')
      riskScores = self.dbProxy.riskScore(riskObjt.threat(),riskObjt.vulnerability(),self.theEnvironmentName,objtName)
      highestScore = 0
      for riskScore in riskScores:
        currentScore = riskScore[2]
        if (currentScore > highestScore):
          highestScore = currentScore
      self.theGraph.add_node(pydot.Node(objtName,shape='diamond',style='filled',margin=0,color='black',fillcolor=threatColourCode(highestScore),fontcolor=riskTextColourCode(highestScore),fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'response'):
      self.theGraph.add_node(pydot.Node(objtName,shape='note',margin=0,fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'countermeasure'):
      self.theGraph.add_node(pydot.Node(objtName,shape='component',margin=0,fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'component'):
      self.theGraph.add_node(pydot.Node(objtName,shape='component',margin=0,fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'requirement'):
      self.theGraph.add_node(pydot.Node(objtName,shape='circle',margin=0,fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'goal'):
      self.theGraph.add_node(pydot.Node(objtName,shape='parallelogram',margin=0,fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'obstacle'):
      obsId = self.dbProxy.getDimensionId(objtName,'obstacle')
      envId = self.dbProxy.getDimensionId(self.theEnvironmentName,'environment')
      obsProb,obsRationale = self.dbProxy.obstacleProbability(obsId,envId)
      self.theGraph.add_node(pydot.Node(objtName,shape='polygon',margin=0,skew='-0.4',style='filled',pencolor='black',colorscheme='ylorrd9',fillcolor=obstacleColourCode(obsProb),fontname=self.fontName,fontsize=self.fontSize,fontcolor=probabilityTextColourCode(obsProb),URL=objtUrl))
    elif (dimName == 'role'):
      self.theGraph.add_node(pydot.Node(objtName,label='',xlabel=objtName,shapefile=roleFile,fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl,peripheries='0'))
    elif (dimName == 'responsibility'):
      self.theGraph.add_node(pydot.Node(objtName,shape='doubleoctagon',margin=0,fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'environment'):
      self.theGraph.add_node(pydot.Node(objtName,shape='doublecircle',margin=0,fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'domainproperty'):
      self.theGraph.add_node(pydot.Node(objtName,shape='house',margin=0,fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'inconsistency'):
      self.theGraph.add_node(pydot.Node(objtName,shape='polygon',margin=0,fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'document_reference'):
      self.theGraph.add_node(pydot.Node(objtName,shape='rectangle',style='filled',fillcolor='gray', margin=0,fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'task'):
      taskScore = self.dbProxy.taskUsabilityScore(objtName,self.theEnvironmentName)
      self.theGraph.add_node(pydot.Node(objtName,shape='ellipse',margin=0,style='filled',color=usabilityColourCode(taskScore),pencolor='black',fontname=self.fontName,fontsize=self.fontSize,fontcolor=usabilityTextColourCode(taskScore),URL=objtUrl))

    else: 
      raise UnknownNodeType(dimName)

  def graph(self):
    self.nodeNameSet = set([])
    self.dimNameSet = set([])

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
      dirType = 'none'
      if (fromDimName == 'risk' and toDimName == 'vulnerability'):
        dirType = 'forward'
      edge = pydot.Edge(str(fromName),str(toName),dir=dirType)
      self.theGraph.add_edge(edge)

    if (self.isTagged == True):
      tags = self.dbProxy.riskModelTags(self.theEnvironmentName)
      if (len(tags) > 0):
        for tag in tags:
          cluster = pydot.Cluster(tag,label=tag)
          for objt,dimName in tags[tag]:
            if (objt not in self.nodeNameSet):
              self.buildNode(dimName,objt)
              self.nodeNameSet.add(objt) 
            cluster.add_node(pydot.Node(objt))
          self.theGraph.add_subgraph(cluster)
    return self.layout()

  def layout(self):
    self.theGraph.write_dot(self.theGraphName,prog=self.theRenderer)
    return open(self.theGraphName).read()
