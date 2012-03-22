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
import armid
from BasePanel import BasePanel
from TaskEnvironmentPanel import TaskEnvironmentPanel
from TCNarrativeTextCtrl import TCNarrativeTextCtrl

class TaskPanel(BasePanel):
  def __init__(self,parent,dp):
    BasePanel.__init__(self,parent,armid.TASK_ID)
    self.dbProxy = dp
 
  def buildControls(self,isCreate,isUpdateable = True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)

    summBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(summBoxSizer,0,wx.EXPAND)
    summBoxSizer.Add(self.buildTextSizer('Name',(87,30),armid.TASK_TEXTNAME_ID),1,wx.EXPAND)
    summBoxSizer.Add(self.buildTextSizer('Code',(87,30),armid.TASK_TEXTSHORTCODE_ID),1,wx.EXPAND)
    mainSizer.Add(self.buildTextSizer('Author',(87,30),armid.TASK_TEXTAUTHOR_ID),0,wx.EXPAND)
    mainSizer.Add(self.buildCheckSizer('Assumption Task',armid.TASK_CHECKASSUMPTION_ID,False),0,wx.EXPAND)

    oBox = wx.StaticBox(self,-1,'Objective')
    oSizer = wx.StaticBoxSizer(oBox,wx.HORIZONTAL)
    oSizer.Add(TCNarrativeTextCtrl(self,armid.TASK_TEXTOBJECTIVE_ID),1,wx.EXPAND)
    mainSizer.Add(oSizer,0,wx.EXPAND)

    self.environmentPanel = TaskEnvironmentPanel(self,self.dbProxy)
    mainSizer.Add(self.environmentPanel,1,wx.EXPAND)
    mainSizer.Add(self.buildCommitButtonSizer(armid.TASK_BUTTONCOMMIT_ID,isCreate),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

  def loadControls(self,task,isReadOnly=False):
    nameCtrl = self.FindWindowById(armid.TASK_TEXTNAME_ID)
    nameCtrl.SetValue(task.name())
    shortCodeCtrl = self.FindWindowById(armid.TASK_TEXTSHORTCODE_ID)
    shortCodeCtrl.SetValue(task.shortCode())
    authorCtrl = self.FindWindowById(armid.TASK_TEXTAUTHOR_ID)
    authorCtrl.SetValue(task.author())
    assumptionCtrl = self.FindWindowById(armid.TASK_CHECKASSUMPTION_ID)
    assumptionCtrl.SetValue(task.assumption())
    objectiveCtrl = self.FindWindowById(armid.TASK_TEXTOBJECTIVE_ID)
    objectiveCtrl.Set(task.name(),task.objective())
    self.environmentPanel.loadControls(task)
