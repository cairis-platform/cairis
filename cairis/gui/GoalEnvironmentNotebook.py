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
from GoalPage import GoalPage
from ConcernAssociationListCtrl import ConcernAssociationListCtrl

__author__ = 'Shamal Faily'

class SummaryPage(wx.Panel):
  def __init__(self,parent,refiningGoal):
    wx.Panel.__init__(self,parent,GOAL_PANELSUMMARY_ID)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    topRowSizer = wx.BoxSizer(wx.HORIZONTAL)
    topSizer.Add(topRowSizer,0,wx.EXPAND)

    lblBox = wx.StaticBox(self,-1,'Label')
    lblBoxSizer = wx.StaticBoxSizer(lblBox,wx.VERTICAL)
    topRowSizer.Add(lblBoxSizer,0,wx.EXPAND)
    self.labelCtrl = wx.TextCtrl(self,GOAL_TEXTLABEL_ID,"",pos=wx.DefaultPosition,size=wx.Size(150,30),style=wx.TE_READONLY)
    self.labelCtrl.Disable()
    lblBoxSizer.Add(self.labelCtrl,1,wx.EXPAND)

    catBox = wx.StaticBox(self,-1,'Category')
    catBoxSizer = wx.StaticBoxSizer(catBox,wx.VERTICAL)
    topRowSizer.Add(catBoxSizer,1,wx.EXPAND)


    catList = ['Achieve','Maintain','Avoid','Improve','Increase','Maximise','Minimise']
    self.categoryCtrl = wx.ComboBox(self,GOAL_COMBOCATEGORY_ID,choices=catList,size=wx.DefaultSize,style= wx.CB_READONLY)
    catBoxSizer.Add(self.categoryCtrl,1,wx.EXPAND)

    priBox = wx.StaticBox(self,-1,'Priority')
    priBoxSizer = wx.StaticBoxSizer(priBox,wx.VERTICAL)
    topSizer.Add(priBoxSizer,0,wx.EXPAND)
    priList = ['Low','Medium','High']
    self.priorityCtrl = wx.ComboBox(self,GOAL_COMBOPRIORITY_ID,choices=priList,size=wx.DefaultSize,style= wx.CB_READONLY)
    priBoxSizer.Add(self.priorityCtrl,1,wx.EXPAND)

    defBox = wx.StaticBox(self,-1,'Definition')
    defBoxSizer = wx.StaticBoxSizer(defBox,wx.VERTICAL)
    topSizer.Add(defBoxSizer,1,wx.EXPAND)
    self.definitionCtrl = wx.TextCtrl(self,GOAL_TEXTDEFINITION_ID,'',style= wx.TE_MULTILINE)
    defBoxSizer.Add(self.definitionCtrl,1,wx.EXPAND)

    if (refiningGoal == True):
      ctBox = wx.StaticBox(self,-1,'Contribution Type')
      ctBoxSizer = wx.StaticBoxSizer(ctBox,wx.HORIZONTAL)
      topSizer.Add(ctBoxSizer,0,wx.EXPAND)
      self.ctCtrl = wx.ComboBox(self,GOAL_COMBOCONTRIBUTIONTYPE_ID,choices=['Operationalises','Obstructs'],size=wx.DefaultSize,style=wx.CB_READONLY)
      self.ctCtrl.SetSelection(0)
      ctBoxSizer.Add(self.ctCtrl,1,wx.EXPAND)

    self.SetSizer(topSizer)

class MLTextPage(wx.Panel):
  def __init__(self,parent,winId):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    narrativeBox = wx.StaticBox(self,-1)
    narrativeBoxSizer = wx.StaticBoxSizer(narrativeBox,wx.HORIZONTAL)
    topSizer.Add(narrativeBoxSizer,1,wx.EXPAND)
    self.narrativeCtrl = wx.TextCtrl(self,winId,'',style=wx.TE_MULTILINE)
    narrativeBoxSizer.Add(self.narrativeCtrl,1,wx.EXPAND)
    self.SetSizer(topSizer)

class ConcernAssociationPage(wx.Panel):
  def __init__(self,parent,winId,dp):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    caBox = wx.StaticBox(self,-1)
    caBoxSizer = wx.StaticBoxSizer(caBox,wx.HORIZONTAL)
    topSizer.Add(caBoxSizer,1,wx.EXPAND)
    self.caList = ConcernAssociationListCtrl(self,winId,dp)
    caBoxSizer.Add(self.caList,1,wx.EXPAND)
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


class GoalEnvironmentNotebook(wx.Notebook):
  def __init__(self,parent,dp,refiningGoal=False):
    wx.Notebook.__init__(self,parent,GOAL_NOTEBOOKENVIRONMENT_ID)
    p1 = SummaryPage(self,refiningGoal)
    p2 = MLTextPage(self,GOAL_TEXTFITCRITERION_ID)
    p3 = MLTextPage(self,GOAL_TEXTISSUE_ID)
    p4 = GoalPage(self,GOAL_LISTGOALREFINEMENTS_ID,True,dp)
    p5 = GoalPage(self,GOAL_LISTSUBGOALREFINEMENTS_ID,False,dp)
    p6 = ConcernPage(self,GOAL_LISTCONCERNS_ID,dp)
    p7 = ConcernAssociationPage(self,GOAL_LISTCONCERNASSOCIATIONS_ID,dp)
    self.AddPage(p1,'Definition')
    self.AddPage(p2,'Fit Criterion')
    self.AddPage(p3,'Issue')
    self.AddPage(p4,'Goals')
    self.AddPage(p5,'Sub-Goals')
    self.AddPage(p6,'Concerns')
    self.AddPage(p7,'Concern Associations')
