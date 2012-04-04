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
from TaskPersonaListCtrl import TaskPersonaListCtrl
from ConcernAssociationListCtrl import ConcernAssociationListCtrl
from NarrativeCtrl import NarrativeCtrl
from DimensionListCtrl import DimensionListCtrl

class SummaryPage(wx.Panel):
  def __init__(self,parent,dp):
    wx.Panel.__init__(self,parent)
    self.dbProxy = dp
    topSizer = wx.BoxSizer(wx.VERTICAL)

    depsBox = wx.StaticBox(self,-1,'Dependencies')
    depsBoxSizer = wx.StaticBoxSizer(depsBox,wx.VERTICAL)
    topSizer.Add(depsBoxSizer,0,wx.EXPAND)
    self.dependenciesCtrl = wx.TextCtrl(self,armid.TASK_TEXTDEPENDENCIES_ID,'',size=(150,100),style= wx.TE_MULTILINE)
    depsBoxSizer.Add(self.dependenciesCtrl,1,wx.EXPAND)

    personaBox = wx.StaticBox(self)
    personaSizer = wx.StaticBoxSizer(personaBox,wx.HORIZONTAL)
    topSizer.Add(personaSizer,0,wx.EXPAND)
    self.personaList = TaskPersonaListCtrl(self,armid.TASK_LISTPERSONAS_ID,self.dbProxy)
    personaSizer.Add(self.personaList,1,wx.EXPAND)

    assetBox = wx.StaticBox(self)
    assetSizer = wx.StaticBoxSizer(assetBox,wx.HORIZONTAL)
    topSizer.Add(assetSizer,1,wx.EXPAND)
    self.assetList = DimensionListCtrl(self,armid.TASK_LISTASSETS_ID,wx.DefaultSize,'Concerns','asset',self.dbProxy)
    assetSizer.Add(self.assetList,1,wx.EXPAND)

    self.SetSizer(topSizer)

class NarrativePage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)
    narrativeBox = wx.StaticBox(self,-1)
    narrativeBoxSizer = wx.StaticBoxSizer(narrativeBox,wx.HORIZONTAL)
    topSizer.Add(narrativeBoxSizer,1,wx.EXPAND)
    self.narrativeCtrl = NarrativeCtrl(self,armid.TASK_TEXTNARRATIVE_ID)
    narrativeBoxSizer.Add(self.narrativeCtrl,1,wx.EXPAND)

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


class TaskEnvironmentNotebook(wx.Notebook):
  def __init__(self,parent,dp):
    wx.Notebook.__init__(self,parent,armid.TASK_NOTEBOOKENVIRONMENT_ID)
    p1 = SummaryPage(self,dp)
    p2 = NarrativePage(self)
    p3 = MLTextPage(self,armid.TASK_TEXTCONSEQUENCES_ID)
    p4 = MLTextPage(self,armid.TASK_TEXTBENEFITS_ID)
    p5 = ConcernAssociationPage(self,armid.TASK_LISTCONCERNASSOCIATIONS_ID,dp)
    self.AddPage(p1,'Summary')
    self.AddPage(p2,'Narrative')
    self.AddPage(p3,'Consequences')
    self.AddPage(p4,'Benefits')
    self.AddPage(p5,'Concern Associations')
