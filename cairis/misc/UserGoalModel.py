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

from cairis.core.Borg import Borg
from cairis.core.ARM import *
from cairis.core.colourcodes import goalSatisfactionColourCode
from cairis.core.colourcodes import goalSatisfactionFontColourCode

def contLabel(contName):
  if contName == 'Make':
    return "*\n+\n(100)"
  elif contName == 'SomePositive':
    return "+\n*\n(50)"
  elif contName == 'Help':
    return "+\n(25)"
  elif contName == 'Hurt':
    return "-\n(-25)"
  elif contName == 'SomeNegative':
    return "-\n*\n(-50)"
  if contName == 'Break':
    return "*\n-\n(-100)"

  
class UserGoalModel:
  def __init__(self,contributions, envName,db_proxy=None,font_name=None, font_size=None):
    self.theContributions = contributions
    self.theEnvironmentName = envName
    self.fontName = font_name
    self.fontSize = font_size
    self.dbProxy = db_proxy

    b = Borg()

    if font_size is None or font_name is None:
      self.fontName = b.fontName
      self.fontSize = b.fontSize

    self.theGraph = pydot.Dot()
    self.theGraph.set_graph_defaults(rankdir='TB')
    self.theGraphName = b.tmpDir + '/' + 'ugm.dot'

  def size(self):
    return len(self.theContributions)

  def buildNode(self,dimName,objtName):
    objtUrl = dimName + '#' + objtName
    colourCode = '3'
    fontColourCode = 'black'
    objtLabel = objtName
    if (dimName == 'goal' or dimName == 'softgoal'):
      objtUrl = 'user_goal#' + objtName
      satScore = self.dbProxy.goalSatisfactionScore(objtName,self.theEnvironmentName)
      colourCode = goalSatisfactionColourCode(satScore)
      fontColourCode = goalSatisfactionFontColourCode(satScore)
      objtLabel += "\n(" + str(satScore) + ")"
    if (dimName == 'softgoal'):
      self.theGraph.add_node(pydot.Node(objtName,label=objtLabel,shape='septagon',margin=0,style='"rounded,filled"',pencolor='black',colorscheme='rdylgn5',fillcolor=colourCode,fontcolour=fontColourCode,fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'goal'):
      self.theGraph.add_node(pydot.Node(objtName,label=objtLabel,shape='box',margin=0,style='"rounded,filled"',pencolor='black',colorscheme='rdylgn5',fillcolor=colourCode,fontcolor=fontColourCode,fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'task'):
      self.theGraph.add_node(pydot.Node(objtName,shape='hexagon',margin=0,fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    else:
      raise UnknownNodeType(dimName)

  def layout(self,renderer = 'dot'):
    self.theGraph.write_xdot(self.theGraphName,prog=renderer)
    return open(self.theGraphName).read()

  def graph(self):
    try:
      nodeNameSet = set([])
      edgeSet = set([])

      for source, sourceType, sourceDim, target, targetType, targetDim, meName, contName in self.theContributions:

        if (source not in nodeNameSet):
          self.buildNode(sourceDim,source)
          nodeNameSet.add(source)

        if (target not in nodeNameSet):
          self.buildNode(targetDim,target)
          nodeNameSet.add(target)

        if ((source,target) not in edgeSet):
          fromName = source
          toName = target
          if meName == 'end':
            fromName = target
            toName = source 
          gc = pydot.Edge(fromName,toName,dir='forward',label=contLabel(contName),arrowhead='vee',fontname=self.fontName,fontsize=self.fontSize)
          self.theGraph.add_edge(gc)
      return self.layout()
    except DatabaseProxyException as errTxt:
      raise ARMException(errTxt)
