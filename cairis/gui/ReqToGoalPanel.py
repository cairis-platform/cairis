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
from BasePanel import BasePanel
import cairis.core.Goal
from cairis.core.Borg import Borg
from ReqToGoalEnvironmentPanel import ReqToGoalEnvironmentPanel

__author__ = 'Shamal Faily'

class ReqToGoalPanel(BasePanel):
  def __init__(self,parent,goalName,goalDef,goalCat,goalPri,goalFc,goalIssue,goalOrig,goalAssets,envName):
    BasePanel.__init__(self,parent,GOAL_ID)
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(self.buildTextSizer('Name',(87,30),GOAL_TEXTNAME_ID),0,wx.EXPAND)
    mainSizer.Add(self.buildTextSizer('Originator',(87,30),GOAL_TEXTORIGINATOR_ID),0,wx.EXPAND)
    self.environmentPanel = ReqToGoalEnvironmentPanel(self,goalDef,goalCat,goalPri,goalFc,goalIssue,goalAssets,envName)
    mainSizer.Add(self.environmentPanel,1,wx.EXPAND)
    mainSizer.Add(self.buildCommitButtonSizer(GOAL_BUTTONCOMMIT_ID,True),0,wx.CENTER)
    origCtrl = self.FindWindowById(GOAL_TEXTORIGINATOR_ID)
    origCtrl.SetValue(goalOrig)
    self.SetSizer(mainSizer)
