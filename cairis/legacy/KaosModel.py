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
import wx
import os
from cairis.core.ARM import *
import gtk
from cairis.core.colourcodes import usabilityColourCode
from cairis.core.colourcodes import usabilityTextColourCode
from cairis.core.colourcodes import threatColourCode
from cairis.core.colourcodes import obstacleColourCode

__author__ = 'Shamal Faily'

class KaosModel:
  def __init__(self,associations,envName,kaosModelType = 'goal',goalName = ''):
    self.theAssociations = associations
    self.theEnvironmentName = envName
    self.theGoalName = goalName
    b = Borg()
    self.dbProxy = b.dbProxy
    self.fontName = b.fontName
    self.fontSize = b.fontSize
    self.theGraph = pydot.Dot()
    self.theKaosModel = kaosModelType
    if (self.theKaosModel == 'task'):
      self.theGraph.set_graph_defaults(rankdir='LR')
    else:
      self.theGraph.set_graph_defaults(rankdir='BT')
    self.theGraphName = b.tmpDir + '/' + self.theKaosModel + '.dot'

  def size(self):
    return len(self.theAssociations)

  def buildNode(self,dimName,objtName):
    objtUrl = dimName + '#' + objtName
    if (dimName == 'goal'):
      self.theGraph.add_node(pydot.Node(objtName,shape='parallelogram',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
# soft-goal attributes      self.theGraph.add_node(pydot.Node(objtName,shape='polygon',style='rounded',sides='6',distortion='-0.537997',orientation='52',skew='-0.960726',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'obstacle'):
      obsId = self.dbProxy.getDimensionId(objtName,'obstacle')
      envId = self.dbProxy.getDimensionId(self.theEnvironmentName,'environment')
      self.theGraph.add_node(pydot.Node(objtName,shape='polygon',skew='-0.4',style='filled',pencolor='black',colorscheme='ylorrd9',fillcolor=obstacleColourCode(self.dbProxy.obstacleProbability(obsId,envId)),fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'domainproperty'):
      self.theGraph.add_node(pydot.Node(objtName,shape='house',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'requirement'):
      self.theGraph.add_node(pydot.Node(objtName,shape='parallelogram',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'countermeasure'):
      self.theGraph.add_node(pydot.Node(objtName,shape='hexagon',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif ((dimName == 'role') and (self.theKaosModel != 'task')):
      self.theGraph.add_node(pydot.Node(objtName,shape='hexagon',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif ((dimName == 'role') and (self.theKaosModel == 'task')):
      self.theGraph.add_node(pydot.Node(objtName,shape='ellipse',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'usecase'):
      self.theGraph.add_node(pydot.Node(objtName,shape='ellipse',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'task'):
      objt = self.dbProxy.dimensionObject(objtName,'task')
      if (objt.assumption() == True):
        objtLabel = "&lt;&lt;Assumption&gt;&gt;" + objtName 
      else:
        objtLabel = objtName
      taskScore = self.dbProxy.taskUsabilityScore(objtName,self.theEnvironmentName)
      self.theGraph.add_node(pydot.Node(objtName,label=objtLabel,shape='ellipse',style='filled',color=usabilityColourCode(taskScore),fontcolor=usabilityTextColourCode(taskScore),fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'misusecase'):
      ellipseColour = 'black'
      if (self.theKaosModel == 'task'):
        riskName = objtName[8:]
        riskObjt = self.dbProxy.dimensionObject(riskName,'risk')
        riskScores = self.dbProxy.riskScore(riskObjt.threat(),riskObjt.vulnerability(),self.theEnvironmentName,riskName)
        highestScore = 0
        for riskScore in riskScores:
          currentScore = riskScore[2]
          if (currentScore > highestScore):
            highestScore = currentScore
        ellipseColour = threatColourCode(highestScore)
        ellipseFontColour = 'white'
        if highestScore < 2:
          ellipseFontColour = 'black'
      self.theGraph.add_node(pydot.Node(objtName,shape='ellipse',style='filled',color=ellipseColour,fontcolor=ellipseFontColour,fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'persona'):
      objt = self.dbProxy.dimensionObject(objtName,'persona')
      if (objt.assumption() == True):
        objtLabel = "&lt;&lt;Assumption&gt;&gt;" + objtName 
        self.theGraph.add_node(pydot.Node(objtName,label=objtLabel,shape='circle',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
      else: 
        self.theGraph.add_node(pydot.Node(objtName,shape='circle',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'attacker'):
      self.theGraph.add_node(pydot.Node(objtName,shape='circle',style='filled',color='black',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'response'):
      self.theGraph.add_node(pydot.Node(objtName,shape='note',fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'asset'):
      fontColour = 'black'
      nodeColour = 'black'
      if (self.theKaosModel == 'task'):
        fontColour = 'blue'
        nodeColour = 'blue'
      self.theGraph.add_node(pydot.Node(objtName,shape='record',fontname=self.fontName,fontsize=self.fontSize,fontcolor=fontColour,color=nodeColour,URL=objtUrl))
    else:
      raise ARM.UnknownNodeType(dimName)


  def layout(self,renderer = ''):
    if (renderer == ''):
      if ((self.theKaosModel == 'goal') or (self.theKaosModel == 'template_goal') or (self.theKaosModel == 'obstacle')):
        renderer = 'dot'
      if (self.theKaosModel == 'responsibility'):
        renderer = 'twopi'
      elif (self.theKaosModel == 'task'):
        renderer = 'dot'
    self.theGraph.write_xdot(self.theGraphName,prog=renderer)
    return open(self.theGraphName).read()

  def buildGoalModel(self,isComponent=False):
    self.nodeNameSet = set([])
    refNodes = set([])
    # the Graph get_edge function doesn't appear to work, so we'll keep a set of edges ourselves.
    edgeSet = set([])

    for association in self.theAssociations:
      goalName = association.goal()
      associationType = association.type()
      subGoalName = association.subGoal()
      alternativeFlag = association.alternative()
      goalDimName = association.goalDimension()
      subGoalDimName = association.subGoalDimension()
      goalEnv = association.environment()

      if ((self.theGoalName != '' or isComponent == True) and goalName not in self.nodeNameSet):
        self.buildNode(goalDimName,goalName)
      if ((self.theGoalName != '' or isComponent == True) and subGoalName not in self.nodeNameSet):
        self.buildNode(subGoalDimName,subGoalName)

      if ((associationType == 'obstruct') or (associationType == 'resolve')):
        if ((subGoalName,goalName) not in edgeSet):
          goalEdge = pydot.Edge(subGoalName,goalName,dir='forward',arrowhead='veetee',weight='1')
          self.theGraph.add_edge(goalEdge)
          edgeSet.add((subGoalName,goalName))
      elif (associationType == 'depend'):
        if ((subGoalName,goalName) not in edgeSet):
          objtUrl = 'depend#' + goalEnv + '/' + goalName + '/' + subGoalName
#          self.theGraph.add_node(pydot.Node(objtUrl,shape='circle',label=' ',height='.2',width='.2',URL=objtUrl))
          self.theGraph.add_node(pydot.Node(objtUrl,shape='trapezium',style='rounded',orientation='270',label=' ',height='.2',width='.2',URL=objtUrl))
          edge1 = pydot.Edge(goalName,objtUrl,dir='forward',arrowhead='vee',weight='1')
          self.theGraph.add_edge(edge1)
          edge2 = pydot.Edge(objtUrl,subGoalName,dir='forward',arrowhead='vee',weight='1')
          self.theGraph.add_edge(edge2)
          edgeSet.add((subGoalName,goalName))
      else:
        refNodeName = goalName + '#' + associationType
        # This is probably a good time to see if there is already another goalassociation in the graph for another environment
        assocDirection = 'forward'
        arrowHead = 'vee'
        if ((subGoalName,refNodeName) not in edgeSet):
          objtUrl = 'link#' + goalEnv + '/' + goalName + '/' + subGoalName + '/' + goalDimName + '/' + subGoalDimName
          if (alternativeFlag == 1):
            refNodeName = goalName + '#' + subGoalName + '#' + associationType
          if (refNodeName not in refNodes):
            if (associationType == 'and'):
              objtUrl = 'linkand#' + goalEnv + '/' + goalName + '/' + subGoalName + '/' + goalDimName + '/' + subGoalDimName
              self.theGraph.add_node(pydot.Node(refNodeName,shape='circle',label=' ',height='.2',width='.2',URL=objtUrl))
            elif (associationType == 'or'):
              objtUrl = 'linkor#' + goalEnv + '/' + goalName + '/' + subGoalName + '/' + goalDimName + '/' + subGoalDimName
              self.theGraph.add_node(pydot.Node(refNodeName,shape='circle',style='filled',color='black',label=' ',height='.2',width='.2',URL=objtUrl))
            elif (associationType == 'responsible'):
              objtUrl = 'linkresponsible#' + goalEnv + '/' + goalName + '/' + subGoalName + '/' + goalDimName + '/' + subGoalDimName
              self.theGraph.add_node(pydot.Node(refNodeName,shape='circle',style='filled',color='red',label=' ',height='.2',width='.2',URL=objtUrl))
            elif (associationType == 'conflict'):
              objtUrl = 'linkconflict#' + goalEnv + '/' + goalName + '/' + subGoalName + '/' + goalDimName + '/' + subGoalDimName
              self.theGraph.add_node(pydot.Node(refNodeName,shape='circle',color='red',label=' ',height='.2',width='.2',URL=objtUrl))
              assocDirection = 'none'
              arrowHead = 'none'
            goalEdge = pydot.Edge(refNodeName,goalName,dir=assocDirection,arrowhead=arrowHead,weight='1')
            if ((refNodeName,goalName) not in edgeSet):
              self.theGraph.add_edge(goalEdge)
              edgeSet.add((refNodeName,goalName))
              refNodes.add(refNodeName)

          if ((subGoalName,refNodeName) not in edgeSet):
            self.theGraph.add_edge(pydot.Edge(subGoalName,refNodeName,dir='none',weight='1'))
            edgeSet.add((subGoalName,refNodeName))
        else:
          pass
          # Mark the node with a ? so we know the association properties might vary by environment
#          modifiedRefNodeName = '\"' + refNodeName + '\"'
#          refNode = self.theGraph.get_node(modifiedRefNodeName)
#          refNode.set('label','?')
     
        

  def buildTaskModel(self):
    self.nodeNameSet = set([])
    edgeSet = set([])
    fontSize = '7.5'
    for association in self.theAssociations:
      goalName = association.goal()
      subGoalName = association.subGoal()
      goalDimName = association.goalDimension()
      subGoalDimName = association.subGoalDimension()
      assocLabel = association.rationale()
      fontColour = 'black'
      edgeColour = 'black'
      edgeStyle = 'solid'
      assocDir = 'none'
      arrowHead = 'none'
      arrowTail = 'none'
      assocType = association.type()

      if (self.theGoalName != '' and goalName not in self.nodeNameSet):
        self.buildNode(goalDimName,goalName)
        self.nodeNameSet.add(goalName)
      if (self.theGoalName != '' and subGoalName not in self.nodeNameSet):
        self.buildNode(subGoalDimName,subGoalName)
        self.nodeNameSet.add(subGoalName)

      if (assocType in ('misusecasethreatasset_association','misusecasevulnerabilityasset_association','taskmisusecasethreat_association','taskmisusecasevulnerability_association')):
        fontColour = 'red'
        edgeColour = 'red'
        assocDir = 'forward'
        arrowHead = 'vee'
      elif (assocType in ('misusecasethreatmitigation_association','misusecasevulnerabilitymitigation_association','taskmisusecasemitigation_association')):
        fontColour = 'green'
        edgeColour = 'green'
        assocDir = 'forward'
        arrowHead = 'vee'
      elif (assocType == 'taskasset_association'):
        fontColour = 'blue'
        edgeColour = 'blue'
        arrowTail = 'vee'
      elif (assocType == 'rolepersona_association' or assocType == 'roleattacker_association'):
        arrowHead = 'empty'
        assocDir = 'forward'

      if (assocType in ('misusecasethreatasset_association','misusecasevulnerabilityasset_association','taskasset_association')):
        arrowHead = 'none'
        arrowTail = 'vee'
      if (assocType == 'taskmisusecasemitigation_association'):
        arrowHead = 'none'
        arrowTail = 'vee'

      if (assocType == 'usecasetask_association'):
        arrowTail = 'vee'
        edgeStyle = 'dashed'



      objtUrl = goalDimName + '#' + subGoalDimName + '#' + assocType
      if ((subGoalName,goalName,assocLabel) not in edgeSet):
	if assocLabel == '':
	    assocLabel = ' '
        self.theGraph.add_edge(pydot.Edge(subGoalName,goalName,style=edgeStyle,dir=assocDir,arrowhead=arrowHead,arrowtail=arrowTail,label=assocLabel,fontsize=fontSize,weight='1',fontcolor=fontColour,color=edgeColour,URL=objtUrl))
        edgeSet.add((subGoalName,goalName,assocLabel))

  def graph(self):
    try:
      elements = []
      if (self.theKaosModel == 'goal' and self.theGoalName == ''):
        elements = self.dbProxy.goalModelElements(self.theEnvironmentName)
      elif (self.theKaosModel == 'obstacle' and self.theGoalName == ''):
        elements = self.dbProxy.obstacleModelElements(self.theEnvironmentName)
      elif (self.theKaosModel == 'responsibility' and self.theGoalName == ''):
        elements = self.dbProxy.responsibilityModelElements(self.theEnvironmentName)
      elif (self.theKaosModel == 'task' and self.theGoalName == ''):
        elements = self.dbProxy.taskModelElements(self.theEnvironmentName)

      for element in elements:
        self.buildNode(element[0],element[1])

      if ((self.theKaosModel == 'goal') or (self.theKaosModel == 'responsibility') or (self.theKaosModel == 'obstacle')):
        self.buildGoalModel()
      elif (self.theKaosModel == 'template_goal'):
        self.buildGoalModel(True)
      else:
        self.buildTaskModel()

      return self.layout()
    except DatabaseProxyException, errTxt:
      raise ARMException(errTxt)

