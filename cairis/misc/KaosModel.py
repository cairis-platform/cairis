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
from cairis.core.colourcodes import usabilityColourCode
from cairis.core.colourcodes import usabilityTextColourCode
from cairis.core.colourcodes import probabilityTextColourCode
from cairis.core.colourcodes import threatColourCode
from cairis.core.colourcodes import riskTextColourCode
from cairis.core.colourcodes import obstacleColourCode


class KaosModel:
  def __init__(self,associations,envName,kaosModelType = 'goal',goalName = '', db_proxy=None, font_name=None, font_size=None):
    self.theAssociations = associations
    self.theEnvironmentName = envName
    self.theGoalName = goalName
    self.dbProxy = db_proxy
    self.fontName = font_name
    self.fontSize = font_size

    b = Borg()
    if db_proxy is None: 
      self.dbProxy = b.dbProxy

    if font_size is None or font_name is None:
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
    if ((self.theKaosModel == 'template_goal') and (dimName == 'goal')):
      dimName = 'template_goal'
    objtUrl = dimName + '#' + objtName
    b = Borg()
    actorFile = b.assetDir + '/modelActor.png'
    attackerFile = b.assetDir + '/modelAttacker.png'
      
    if ((dimName == 'goal') or (dimName == 'template_goal')):
      self.theGraph.add_node(pydot.Node(objtName,shape='parallelogram',margin=0,fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'obstacle'):
      obsId = self.dbProxy.getDimensionId(objtName,'obstacle')
      envId = self.dbProxy.getDimensionId(self.theEnvironmentName,'environment')
      obsProb,obsRationale = self.dbProxy.obstacleProbability(obsId,envId)
      self.theGraph.add_node(pydot.Node(objtName,shape='polygon',margin=0,skew='-0.4',style='filled',pencolor='black',colorscheme='ylorrd9',fillcolor=obstacleColourCode(obsProb),fontname=self.fontName,fontsize=self.fontSize,fontcolor=probabilityTextColourCode(obsProb),URL=objtUrl))
    elif (dimName == 'domainproperty'):
      self.theGraph.add_node(pydot.Node(objtName,shape='house',margin=0,fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'requirement'):
      self.theGraph.add_node(pydot.Node(objtName,shape='parallelogram',margin=0,fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'countermeasure'):
      self.theGraph.add_node(pydot.Node(objtName,shape='hexagon',margin=0,fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif ((dimName == 'role') and (self.theKaosModel != 'task')):
      self.theGraph.add_node(pydot.Node(objtName,shape='hexagon',margin=0,fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif ((dimName == 'role') and (self.theKaosModel == 'task')):
      self.theGraph.add_node(pydot.Node(objtName,label='',xlabel=objtName,shapefile=actorFile,fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl,peripheries='0'))
    elif (dimName == 'usecase'):
      self.theGraph.add_node(pydot.Node(objtName,shape='ellipse',margin=0,fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'task'):
      objt = self.dbProxy.dimensionObject(objtName,'task')
      if (objt.assumption() == True):
        objtLabel = "&lt;&lt;Assumption&gt;&gt;" + objtName 
      else:
        objtLabel = objtName
      taskScore = self.dbProxy.taskUsabilityScore(objtName,self.theEnvironmentName)
      self.theGraph.add_node(pydot.Node(objtName,label=objtLabel,shape='ellipse',margin=0,style='filled',color=usabilityColourCode(taskScore),fontname=self.fontName,fontsize=self.fontSize,fontcolor=usabilityTextColourCode(taskScore),URL=objtUrl))
    elif (dimName == 'misusecase'):
      ellipseColour = 'black'
      if (self.theKaosModel == 'task'):
        try:
          riskName = objtName[8:]
          riskObjt = self.dbProxy.dimensionObject(riskName,'risk')
          riskScores = self.dbProxy.riskScore(riskObjt.threat(),riskObjt.vulnerability(),self.theEnvironmentName,riskName)
          highestScore = 0
          for riskScore in riskScores:
            currentScore = riskScore[2]
            if (currentScore > highestScore):
              highestScore = currentScore
          ellipseColour = threatColourCode(highestScore)
        except TypeError as ex:
          raise ARMException("Error processing risk " + riskName + " in task model" + format(ex))
      self.theGraph.add_node(pydot.Node(objtName,shape='ellipse',margin=0,style='filled',color=ellipseColour,fontcolor=riskTextColourCode(highestScore),fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'persona'):
      objt = self.dbProxy.dimensionObject(objtName,'persona')
      if (objt.assumption() == True):
        objtLabel = "&lt;&lt;Assumption&gt;&gt;" + objtName 
        self.theGraph.add_node(pydot.Node(objtName,label='',xlabel=objtLabel,shapefile=actorFile,fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl,peripheries='0'))
      else: 
        self.theGraph.add_node(pydot.Node(objtName,label='',xlabel=objtName,shapefile=actorFile,fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl,peripheries='0'))
    elif (dimName == 'attacker'):
      self.theGraph.add_node(pydot.Node(objtName,label='',xlabel=objtName,shapefile=attackerFile,fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl,peripheries='0'))
    elif (dimName == 'response'):
      self.theGraph.add_node(pydot.Node(objtName,shape='note',margin=0,fontname=self.fontName,fontsize=self.fontSize,URL=objtUrl))
    elif (dimName == 'asset'):
      fontColour = 'black'
      nodeColour = 'black'
      if (self.theKaosModel == 'task'):
        fontColour = 'blue'
        nodeColour = 'blue'
      self.theGraph.add_node(pydot.Node(objtName,shape='record',margin=0,fontname=self.fontName,fontsize=self.fontSize,fontcolor=fontColour,color=nodeColour,URL=objtUrl))
    else:
      raise UnknownNodeType(dimName)


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
    b = Borg()
    conflictFile = b.assetDir + '/modelConflict.png'
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
      elif (associationType == 'depender'):
        if ((subGoalName,goalName) not in edgeSet):
          goalEdge = pydot.Edge(goalName,subGoalName,dir='forward',arrowhead='curve',weight='1')
          self.theGraph.add_edge(goalEdge)
          edgeSet.add((goalName,subGoalName))
      elif (associationType == 'dependee'):
        if ((subGoalName,goalName) not in edgeSet):
          goalEdge = pydot.Edge(goalName,subGoalName,dir='forward',arrowhead='curve',weight='1')
          self.theGraph.add_edge(goalEdge)
          edgeSet.add((goalName,subGoalName))
      else:
        refNodeName = goalName + '#' + associationType
        # This is probably a good time to see if there is already another goalassociation in the graph for another environment
        assocDirection = 'forward'
        arrowHead = 'vee'
        if ((subGoalName,refNodeName) not in edgeSet):
          objtUrl = 'goalassociation#' + goalEnv + '/' + goalName + '/' + subGoalName 
          if (alternativeFlag == 1):
            refNodeName = goalName + '#' + subGoalName + '#' + associationType
          if (refNodeName not in refNodes):
            if (subGoalDimName in ['task','usecase']):
              self.theGraph.add_node(pydot.Node(refNodeName,shape='circle',style='filled',color='blue',label=' ',height='.2',width='.2'))
            elif ((subGoalDimName == 'countermeasure') and (associationType == 'and')):
              self.theGraph.add_node(pydot.Node(refNodeName,shape='circle',style='filled',color='blue',label=' ',height='.2',width='.2'))
            elif (associationType == 'and'):
              self.theGraph.add_node(pydot.Node(refNodeName,shape='circle',label=' ',height='.2',width='.2'))
            elif (associationType == 'or'):
              self.theGraph.add_node(pydot.Node(refNodeName,shape='circle',style='filled',color='black',label=' ',height='.2',width='.2'))
            elif (associationType == 'responsible'):
              self.theGraph.add_node(pydot.Node(refNodeName,shape='circle',style='filled',color='red',label=' ',height='.2',width='.2'))
            elif ((associationType == 'conflict') or (associationType == 'obstruct')):
              b = Borg()
              self.theGraph.add_node(pydot.Node(refNodeName,shapefile=conflictFile,margin=0,label='',height='.1',width='.1',peripheries='0'))
              assocDirection = 'none'
              arrowHead = 'none'
            elif((goalDimName == 'requirement') and (subGoalDimName == 'usecase')):
              self.theGraph.add_node(pydot.Node(refNodeName,shape='circle',label=' ',height='.2',width='.2'))
            goalEdge = pydot.Edge(refNodeName,goalName,dir=assocDirection,arrowhead=arrowHead,weight='1')
            if ((refNodeName,goalName) not in edgeSet):
              self.theGraph.add_edge(goalEdge)
              edgeSet.add((refNodeName,goalName))
              refNodes.add(refNodeName)

          if ((subGoalName,refNodeName) not in edgeSet):
            self.theGraph.add_edge(pydot.Edge(subGoalName,refNodeName,dir='none',weight='1',URL=objtUrl))
            edgeSet.add((subGoalName,refNodeName))
        else:
          pass
     
        

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
      elif (assocType == 'rolepersona_association'):
        arrowHead = 'empty'
        assocDir = 'forward'
      elif (assocType == 'roleattacker_association'):
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
        if (assocLabel == ''):
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
    except DatabaseProxyException as errTxt:
      raise ARMException(errTxt)

