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
from InterfacePage import InterfacePage

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

class CriticalPage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    crBoxSizer = wx.BoxSizer(wx.VERTICAL)
    topSizer.Add(crBoxSizer,0,wx.EXPAND)
    self.criticalCheckCtrl = wx.CheckBox(self,ASSET_CHECKCRITICAL_ID,'Critical Asset')
    self.criticalCheckCtrl.SetValue(False)
    crBoxSizer.Add(self.criticalCheckCtrl,0,wx.EXPAND)
    self.criticalRationaleCtrl = wx.TextCtrl(self,ASSET_TEXTCRITICALRATIONALE_ID,'',style=wx.TE_MULTILINE)
    self.criticalRationaleCtrl.Disable()
    crBoxSizer.Add(self.criticalRationaleCtrl,1,wx.EXPAND)
    self.SetSizer(topSizer)
    wx.EVT_CHECKBOX(self,ASSET_CHECKCRITICAL_ID,self.onCheckCritical)

  def onCheckCritical(self,evt):
    if (self.criticalCheckCtrl.GetValue() == True):
      self.criticalRationaleCtrl.Enable()
    else:
      self.criticalRationaleCtrl.Disable()
      self.criticalRationaleCtrl.Clear()

class AssetSummaryNotebook(wx.Notebook):
  def __init__(self,parent,isTemplateAsset = False):
    wx.Notebook.__init__(self,parent,ASSET_NOTEBOOKSUMMARY_ID)
    p1 = MLTextPage(self,ASSET_TEXTDESCRIPTION_ID)
    p2 = MLTextPage(self,ASSET_TEXTSIGNIFICANCE_ID)
    p4 = InterfacePage(self,ASSET_PAGEINTERFACE_ID)
    self.AddPage(p1,'Description')
    self.AddPage(p2,'Significance')
    if (isTemplateAsset == False):
      p3 = CriticalPage(self)
      self.AddPage(p3,'Criticality')
    self.AddPage(p4,'Interfaces')
