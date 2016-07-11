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
from cairis.core.Borg import Borg

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
    b = Borg()
    self.dbProxy = b.dbProxy
    topSizer = wx.BoxSizer(wx.VERTICAL)

    typeBox = wx.StaticBox(self,-1,'Type')
    typeBoxSizer = wx.StaticBoxSizer(typeBox,wx.HORIZONTAL)
    topSizer.Add(typeBoxSizer,0,wx.EXPAND)
    typeChoices = ['Functional','Data','Look and Feel','Usability','Performance','Operational','Maintainability','Portability','Security','Cultural and Political','Legal','Privacy']
    self.typeCtrl = wx.ComboBox(self,SINGLEREQUIREMENT_COMBOTYPE_ID,choices=typeChoices,size=wx.DefaultSize,style=wx.CB_READONLY)
    typeBoxSizer.Add(self.typeCtrl,1,wx.EXPAND)

    radioBox = wx.StaticBox(self,-1,'Referrer')
    radioSizer = wx.StaticBoxSizer(radioBox,wx.HORIZONTAL)
    topSizer.Add(radioSizer,0,wx.EXPAND)
    radioSizer.Add(wx.RadioButton(self,SINGLEREQUIREMENT_RADIOASSET_ID,'Asset',style=wx.RB_GROUP))
    radioSizer.Add(wx.RadioButton(self,SINGLEREQUIREMENT_RADIOENVIRONMENT_ID,'Environment',style=0))
    self.refCtrl = wx.ComboBox(self,SINGLEREQUIREMENT_COMBOREFERRER_ID,choices=self.dbProxy.getDimensionNames('asset'),size=wx.DefaultSize,style=wx.CB_READONLY)
    radioSizer.Add(self.refCtrl,1,wx.EXPAND)
    wx.EVT_RADIOBUTTON(self,SINGLEREQUIREMENT_RADIOASSET_ID,self.onAssetSelected)
    wx.EVT_RADIOBUTTON(self,SINGLEREQUIREMENT_RADIOENVIRONMENT_ID,self.onEnvironmentSelected)
    

    priBox = wx.StaticBox(self,-1,'Priority')
    priBoxSizer = wx.StaticBoxSizer(priBox,wx.HORIZONTAL)
    topSizer.Add(priBoxSizer,0,wx.EXPAND)
    self.priorityCtrl = wx.ComboBox(self,SINGLEREQUIREMENT_COMBOPRIORITY_ID,choices=['1','2','3'],size=wx.DefaultSize,style=wx.CB_READONLY)
    priBoxSizer.Add(self.priorityCtrl,1,wx.EXPAND)
   
    descBox = wx.StaticBox(self,-1,'Description')
    descBoxSizer = wx.StaticBoxSizer(descBox,wx.HORIZONTAL)
    topSizer.Add(descBoxSizer,1,wx.EXPAND)
    self.descriptionCtrl = wx.TextCtrl(self,SINGLEREQUIREMENT_TEXTDESCRIPTION_ID,'',style=wx.TE_MULTILINE)
    descBoxSizer.Add(self.descriptionCtrl,1,wx.EXPAND)

    ctBox = wx.StaticBox(self,-1,'Contribution Type')
    ctBoxSizer = wx.StaticBoxSizer(ctBox,wx.HORIZONTAL)
    topSizer.Add(ctBoxSizer,0,wx.EXPAND)
    self.ctCtrl = wx.ComboBox(self,SINGLEREQUIREMENT_COMBOCONTRIBUTIONTYPE_ID,choices=['Operationalises','Obstructs'],size=wx.DefaultSize,style=wx.CB_READONLY)
    self.ctCtrl.SetSelection(0)
    ctBoxSizer.Add(self.ctCtrl,1,wx.EXPAND)

    self.SetSizer(topSizer)

  def onAssetSelected(self,evt):
    self.refCtrl.SetItems(self.dbProxy.getDimensionNames('asset'))
    self.refCtrl.SetValue('')

  def onEnvironmentSelected(self,evt):
    self.refCtrl.SetItems(self.dbProxy.getDimensionNames('environment'))
    self.refCtrl.SetValue('')

class SingleRequirementNotebook(wx.Notebook):
  def __init__(self,parent):
    wx.Notebook.__init__(self,parent,SINGLEREQUIREMENT_NOTEBOOKREQUIREMENT_ID)
    p1 = SummaryPage(self)
    p2 = MLTextPage(self,SINGLEREQUIREMENT_TEXTRATIONALE_ID)
    p3 = MLTextPage(self,SINGLEREQUIREMENT_TEXTFITCRITERION_ID)
    p4 = MLTextPage(self,SINGLEREQUIREMENT_TEXTORIGINATOR_ID)
    self.AddPage(p1,'Definition')
    self.AddPage(p2,'Rationale')
    self.AddPage(p3,'Fit Criterion')
    self.AddPage(p4,'Originator')
