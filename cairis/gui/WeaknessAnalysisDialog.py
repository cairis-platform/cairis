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


import wx
from cairis.core.armid import *
from cairis.core.ARM import *
from WeaknessAnalysisPanel import WeaknessAnalysisPanel
from cairis.core.Borg import Borg

__author__ = 'Shamal Faily'

class WeaknessAnalysisDialog(wx.Dialog):
  def __init__(self,parent,cvName,envName):
    wx.Dialog.__init__(self,parent,-1,'Weakness analysis for ' + cvName,style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(600,350))
    self.panel = 0
    self.theThreatTargets = []
    self.theVulnerabilityTargets = []
    self.theGoalObstacles = []
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = WeaknessAnalysisPanel(self,cvName,envName)
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,WEAKNESSANALYSIS_BUTTONCOMMIT_ID,self.onCommit)

  def onCommit(self,evt):
    thrList = self.FindWindowById(WEAKNESSANALYSIS_LISTTHREATS_ID)
    vulList = self.FindWindowById(WEAKNESSANALYSIS_LISTVULNERABILITIES_ID)
    goList = self.FindWindowById(WEAKNESSANALYSIS_LISTGOALOBSTACLE_ID)

    thrDict = thrList.dimensions() 
    for thrName in thrDict:
      target = thrDict[thrName]
      if target.requirement() != '':
        self.theThreatTargets.append(target) 
    vulDict = vulList.dimensions() 
    for vulName in vulDict:
      target = vulDict[vulName]
      if target.requirement() != '':
        self.theVulnerabilityTargets.append(target) 

    self.theGoalObstacles = goList.dimensions()
    self.EndModal(WEAKNESSANALYSIS_BUTTONCOMMIT_ID)
  def targets(self):
    return self.theThreatTargets + self.theVulnerabilityTargets

  def goalObstacles(self):
    return self.theGoalObstacles
