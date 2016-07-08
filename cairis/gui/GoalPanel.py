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
import cairis.core.Goal
from cairis.core.Borg import Borg
from BasePanel import BasePanel
from GoalEnvironmentPanel import GoalEnvironmentPanel

class GoalPanel(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,GOAL_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
   
  def buildControls(self,isCreate,isUpdateable=True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(self.buildTextSizer('Name',(87,30),GOAL_TEXTNAME_ID),0,wx.EXPAND)
    mainSizer.Add(self.buildTagCtrlSizer((87,30),GOAL_TAGS_ID),0,wx.EXPAND)

    mainSizer.Add(self.buildTextSizer('Originator',(87,30),GOAL_TEXTORIGINATOR_ID),0,wx.EXPAND)
    self.environmentPanel = GoalEnvironmentPanel(self,self.dbProxy)
    mainSizer.Add(self.environmentPanel,1,wx.EXPAND)
    if (isUpdateable):
      mainSizer.Add(self.buildCommitButtonSizer(GOAL_BUTTONCOMMIT_ID,isCreate),0,wx.CENTER)
    self.SetSizer(mainSizer)

  def loadControls(self,goal,isReadOnly=False):
    self.theGoalId = goal.id()
    nameCtrl = self.FindWindowById(GOAL_TEXTNAME_ID)
    tagsCtrl = self.FindWindowById(GOAL_TAGS_ID)
    tagsCtrl.set(goal.tags())

    origCtrl = self.FindWindowById(GOAL_TEXTORIGINATOR_ID)
    environmentCtrl = self.FindWindowById(GOAL_PANELENVIRONMENT_ID)
    nameCtrl.SetValue(goal.name())
    origCtrl.SetValue(goal.originator())
    environmentCtrl.loadControls(goal)
