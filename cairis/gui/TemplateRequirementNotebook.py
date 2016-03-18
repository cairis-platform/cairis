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
from Borg import Borg

class MLTextPage(wx.Panel):
  def __init__(self,parent,winId):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    narrativeBox = wx.StaticBox(self,-1)
    narrativeBoxSizer = wx.StaticBoxSizer(narrativeBox,wx.HORIZONTAL)
    topSizer.Add(narrativeBoxSizer,1,wx.EXPAND)
    self.narrativeCtrl = wx.TextCtrl(self,winId,'None',style=wx.TE_MULTILINE)
    narrativeBoxSizer.Add(self.narrativeCtrl,1,wx.EXPAND)
    self.SetSizer(topSizer)

class SummaryPage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    nameBox = wx.StaticBox(self,-1,'Name')
    nameBoxSizer = wx.StaticBoxSizer(nameBox,wx.HORIZONTAL)
    topSizer.Add(nameBoxSizer,0,wx.EXPAND)
    self.nameCtrl = wx.TextCtrl(self,armid.TEMPLATEREQUIREMENT_TEXTNAME_ID,'')
    nameBoxSizer.Add(self.nameCtrl,1,wx.EXPAND)

    assetBox = wx.StaticBox(self,-1,'Asset')
    assetBoxSizer = wx.StaticBoxSizer(assetBox,wx.HORIZONTAL)
    topSizer.Add(assetBoxSizer,0,wx.EXPAND)

    b = Borg()
    assets = b.dbProxy.getDimensionNames('template_asset')
    self.assetCtrl = wx.ComboBox(self,armid.TEMPLATEREQUIREMENT_COMBOASSET_ID,choices=assets,size=wx.DefaultSize,style=wx.CB_READONLY)
    assetBoxSizer.Add(self.assetCtrl,1,wx.EXPAND)

    typeBox = wx.StaticBox(self,-1,'Type')
    typeBoxSizer = wx.StaticBoxSizer(typeBox,wx.HORIZONTAL)
    topSizer.Add(typeBoxSizer,0,wx.EXPAND)
    typeChoices = ['Functional','Data','Look and Feel','Usability','Performance','Operational','Maintainability','Portability','Security','Cultural and Political','Legal','Privacy']
    self.typeCtrl = wx.ComboBox(self,armid.TEMPLATEREQUIREMENT_COMBOTYPE_ID,choices=typeChoices,size=wx.DefaultSize,style=wx.CB_READONLY)
    typeBoxSizer.Add(self.typeCtrl,1,wx.EXPAND)

    descBox = wx.StaticBox(self,-1,'Description')
    descBoxSizer = wx.StaticBoxSizer(descBox,wx.HORIZONTAL)
    topSizer.Add(descBoxSizer,1,wx.EXPAND)
    self.descriptionCtrl = wx.TextCtrl(self,armid.TEMPLATEREQUIREMENT_TEXTDESCRIPTION_ID,'',style=wx.TE_MULTILINE)
    descBoxSizer.Add(self.descriptionCtrl,1,wx.EXPAND)

    self.SetSizer(topSizer)

class TemplateRequirementNotebook(wx.Notebook):
  def __init__(self,parent):
    wx.Notebook.__init__(self,parent,armid.TEMPLATEREQUIREMENT_NOTEBOOKREQUIREMENT_ID)
    p1 = SummaryPage(self)
    p2 = MLTextPage(self,armid.TEMPLATEREQUIREMENT_TEXTRATIONALE_ID)
    p3 = MLTextPage(self,armid.TEMPLATEREQUIREMENT_TEXTFITCRITERION_ID)
    self.AddPage(p1,'Summary')
    self.AddPage(p2,'Rationale')
    self.AddPage(p3,'Fit Criterion')
