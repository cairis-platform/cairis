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
from DimensionListCtrl import DimensionListCtrl
from GoalAssociationListCtrl import GoalAssociationListCtrl

class SummaryPage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    topRowSizer = wx.BoxSizer(wx.HORIZONTAL)
    topSizer.Add(topRowSizer,0,wx.EXPAND)

    lblBox = wx.StaticBox(self,-1,'Label')
    lblBoxSizer = wx.StaticBoxSizer(lblBox,wx.VERTICAL)
    topRowSizer.Add(lblBoxSizer,0,wx.EXPAND)
    self.labelCtrl = wx.TextCtrl(self,OBSTACLE_TEXTLABEL_ID,"",pos=wx.DefaultPosition,size=wx.Size(150,30),style=wx.TE_READONLY)
    self.labelCtrl.Disable()
    lblBoxSizer.Add(self.labelCtrl,1,wx.EXPAND)
    
    catBox = wx.StaticBox(self,-1,'Category')
    catBoxSizer = wx.StaticBoxSizer(catBox,wx.VERTICAL)
    topRowSizer.Add(catBoxSizer,0,wx.EXPAND)
    catList = ['Confidentiality Threat','Integrity Threat','Availability Threat','Accountability Threat','Anonymity Threat','Pseudonymity Threat','Unlinkability Threat','Unobservability Threat','Vulnerability','Duration','Frequency','Demands','Goal Support']
    self.categoryCtrl = wx.ComboBox(self,OBSTACLE_COMBOCATEGORY_ID,choices=catList,size=wx.DefaultSize,style= wx.CB_READONLY)
    catBoxSizer.Add(self.categoryCtrl,1,wx.EXPAND)

    defBox = wx.StaticBox(self,-1,'Definition')
    defBoxSizer = wx.StaticBoxSizer(defBox,wx.VERTICAL)
    topSizer.Add(defBoxSizer,1,wx.EXPAND)
    self.definitionCtrl = wx.TextCtrl(self,OBSTACLE_TEXTDEFINITION_ID,'',style= wx.TE_MULTILINE)
    defBoxSizer.Add(self.definitionCtrl,1,wx.EXPAND)

    probBox = wx.StaticBox(self,-1,'Probability')
    probBoxSizer = wx.StaticBoxSizer(probBox,wx.VERTICAL)
    topRowSizer.Add(probBoxSizer,0,wx.EXPAND)
    self.probCtrl = wx.TextCtrl(self,OBSTACLE_TEXTPROBABILITY_ID,"",pos=wx.DefaultPosition,size=wx.Size(150,30),style=wx.TE_READONLY)
    self.probCtrl.Disable()
    probBoxSizer.Add(self.probCtrl,1,wx.EXPAND)

    self.SetSizer(topSizer)

class GoalPage(wx.Panel):
  def __init__(self,parent,winId,isGoal,dp):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    sgBox = wx.StaticBox(self,-1)
    sgBoxSizer = wx.StaticBoxSizer(sgBox,wx.HORIZONTAL)
    topSizer.Add(sgBoxSizer,1,wx.EXPAND)
    self.goalList = GoalAssociationListCtrl(self,winId,dp,isGoal)
    sgBoxSizer.Add(self.goalList,1,wx.EXPAND)
    self.SetSizer(topSizer)

class ConcernPage(wx.Panel):
  def __init__(self,parent,winId,dp):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    sgBox = wx.StaticBox(self,-1)
    sgBoxSizer = wx.StaticBoxSizer(sgBox,wx.HORIZONTAL)
    topSizer.Add(sgBoxSizer,1,wx.EXPAND)
    self.concernList = DimensionListCtrl(self,winId,wx.DefaultSize,'Concern','asset',dp)
    sgBoxSizer.Add(self.concernList,1,wx.EXPAND)
    self.SetSizer(topSizer)

class ObstacleEnvironmentNotebook(wx.Notebook):
  def __init__(self,parent,dp):
    wx.Notebook.__init__(self,parent,OBSTACLE_NOTEBOOKENVIRONMENT_ID)
    p1 = SummaryPage(self)
    p2 = GoalPage(self,OBSTACLE_LISTGOALS_ID,True,dp)
    p3 = GoalPage(self,OBSTACLE_LISTSUBGOALS_ID,False,dp)
    p4 = ConcernPage(self,OBSTACLE_LISTCONCERNS_ID,dp)
    self.AddPage(p1,'Definition')
    self.AddPage(p2,'Goals')
    self.AddPage(p3,'Sub-Goals')
    self.AddPage(p4,'Concerns')
