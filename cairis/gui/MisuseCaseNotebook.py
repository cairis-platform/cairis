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

__author__ = 'Shamal Faily'

class SummaryPage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    objectiveBox = wx.StaticBox(self,-1,'Objective')
    objectiveBoxSizer = wx.StaticBoxSizer(objectiveBox,wx.VERTICAL)
    topSizer.Add(objectiveBoxSizer,0,wx.EXPAND)
    self.objectiveCtrl = wx.TextCtrl(self,MISUSECASE_TEXTOBJECTIVE_ID,'',style=wx.TE_READONLY | wx.TE_MULTILINE)
    objectiveBoxSizer.Add(self.objectiveCtrl,1,wx.EXPAND)

    aaSizer = wx.BoxSizer(wx.HORIZONTAL)
    topSizer.Add(aaSizer,0,wx.EXPAND)
    attackerBox = wx.StaticBox(self)
    attackerBoxSizer = wx.StaticBoxSizer(attackerBox,wx.HORIZONTAL)
    self.attackerList = wx.ListCtrl(self,MISUSECASE_LISTATTACKERS_ID,style=wx.LC_REPORT)
    self.attackerList.InsertColumn(0,'Attacker')
    self.attackerList.SetColumnWidth(0,200)
    attackerBoxSizer.Add(self.attackerList,1,wx.EXPAND)
    aaSizer.Add(attackerBoxSizer,1,wx.EXPAND)
    assetBox = wx.StaticBox(self)
    assetBoxSizer = wx.StaticBoxSizer(assetBox,wx.HORIZONTAL)
    self.assetList = wx.ListCtrl(self,MISUSECASE_LISTASSETS_ID,style=wx.LC_REPORT)
    self.assetList.InsertColumn(0,'Asset')
    self.assetList.SetColumnWidth(0,200)
    assetBoxSizer.Add(self.assetList,1,wx.EXPAND)
    aaSizer.Add(assetBoxSizer,1,wx.EXPAND)

    thrSizer = wx.BoxSizer(wx.HORIZONTAL)
    topSizer.Add(thrSizer,0,wx.EXPAND)
    threatBox = wx.StaticBox(self,-1,'Threat')
    threatBoxSizer = wx.StaticBoxSizer(threatBox,wx.HORIZONTAL)
    self.threatCtrl = wx.TextCtrl(self,MISUSECASE_TEXTTHREAT_ID,'',style=wx.TE_READONLY)
    threatBoxSizer.Add(self.threatCtrl,1,wx.EXPAND)
    thrSizer.Add(threatBoxSizer,1,wx.EXPAND)
    lhoodBox = wx.StaticBox(self,-1,'Likelihood')
    lhoodBoxSizer = wx.StaticBoxSizer(lhoodBox,wx.HORIZONTAL)
    self.lhoodCtrl = wx.TextCtrl(self,MISUSECASE_TEXTLIKELIHOOD_ID,'',style=wx.TE_READONLY)
    lhoodBoxSizer.Add(self.lhoodCtrl,1,wx.EXPAND)
    thrSizer.Add(lhoodBoxSizer,1,wx.EXPAND)

    vulSizer = wx.BoxSizer(wx.HORIZONTAL)
    topSizer.Add(vulSizer,0,wx.EXPAND)
    vulBox = wx.StaticBox(self,-1,'Vulnerability')
    vulBoxSizer = wx.StaticBoxSizer(vulBox,wx.HORIZONTAL)
    self.vulCtrl = wx.TextCtrl(self,MISUSECASE_TEXTVULNERABILITY_ID,'',style=wx.TE_READONLY)
    vulBoxSizer.Add(self.vulCtrl,1,wx.EXPAND)
    vulSizer.Add(vulBoxSizer,1,wx.EXPAND)
    sevBox = wx.StaticBox(self,-1,'Severity')
    sevBoxSizer = wx.StaticBoxSizer(sevBox,wx.HORIZONTAL)
    self.sevCtrl = wx.TextCtrl(self,MISUSECASE_TEXTSEVERITY_ID,'',style=wx.TE_READONLY)
    sevBoxSizer.Add(self.sevCtrl,1,wx.EXPAND)
    vulSizer.Add(sevBoxSizer,1,wx.EXPAND)

    ratingBox = wx.StaticBox(self,-1,'Risk Rating')
    ratingBoxSizer = wx.StaticBoxSizer(ratingBox,wx.HORIZONTAL)
    topSizer.Add(ratingBoxSizer,0,wx.EXPAND)
    self.ratingCtrl = wx.TextCtrl(self,MISUSECASE_TEXTSCORE_ID,'',style=wx.TE_READONLY)
    ratingBoxSizer.Add(self.ratingCtrl,1,wx.EXPAND)

    self.SetSizer(topSizer)

class NarrativePage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    narrativeBox = wx.StaticBox(self,-1,'Narrative')
    narrativeBoxSizer = wx.StaticBoxSizer(narrativeBox,wx.HORIZONTAL)
    topSizer.Add(narrativeBoxSizer,1,wx.EXPAND)
    self.narrativeCtrl = wx.TextCtrl(self,MISUSECASE_TEXTNARRATIVE_ID,'',style=wx.TE_MULTILINE)
    narrativeBoxSizer.Add(self.narrativeCtrl,1,wx.EXPAND)

    self.SetSizer(topSizer)

class MisuseCaseNotebook(wx.Notebook):
  def __init__(self,parent):
    wx.Notebook.__init__(self,parent,MISUSECASE_NOTEBOOK_ID)
    p1 = SummaryPage(self)
    p2 = NarrativePage(self)
    self.AddPage(p1,'Summary')
    self.AddPage(p2,'Narrative')
