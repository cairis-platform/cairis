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
import WidgetFactory
from EnvironmentPropertiesPanel import EnvironmentPropertiesPanel
from ValueTensionsGrid import ValueTensionsGrid

__author__ = 'Shamal Faily'

class SummaryPage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,GOAL_PANELSUMMARY_ID)
    topSizer = wx.BoxSizer(wx.VERTICAL)
    topSizer.Add(WidgetFactory.buildTextSizer(self,'Short Code',(87,30),ENVIRONMENT_TEXTSHORTCODE_ID,'Code which prefixes requirements which are specific to this environment'),0,wx.EXPAND)
    topSizer.Add(WidgetFactory.buildMLTextSizer(self,'Description',(87,30),ENVIRONMENT_TEXTDESCRIPTION_ID),1,wx.EXPAND)
    self.SetSizer(topSizer)

class CompositePage(wx.Panel):
  def __init__(self,parent,dp):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)
    cBox = wx.StaticBox(self,-1)
    cBoxSizer = wx.StaticBoxSizer(cBox,wx.HORIZONTAL)
    topSizer.Add(cBoxSizer,1,wx.EXPAND)
    self.compositeCtrl = EnvironmentPropertiesPanel(self,dp)
    cBoxSizer.Add(self.compositeCtrl,1,wx.EXPAND)
    self.SetSizer(topSizer)

class TensionsPage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent)
    self.thePrevRow = -1
    self.thePrevCol = -1
    topSizer = wx.BoxSizer(wx.VERTICAL)
    cBox = wx.StaticBox(self,-1)
    cBoxSizer = wx.StaticBoxSizer(cBox,wx.HORIZONTAL)
    topSizer.Add(cBoxSizer,1,wx.EXPAND)
    self.tensionsCtrl = ValueTensionsGrid(self)
    self.tensionsCtrl.Bind(wx.grid.EVT_GRID_SELECT_CELL,self.onSelectRationale)
    cBoxSizer.Add(self.tensionsCtrl,1,wx.EXPAND)

    rBox = wx.StaticBox(self,-1,'Rationale')
    rBoxSizer = wx.StaticBoxSizer(rBox,wx.VERTICAL)
    topSizer.Add(rBoxSizer,1,wx.EXPAND)
    self.rationaleCtrl = wx.TextCtrl(self,ENVIRONMENT_TEXTTENSIONRATIONALE_ID,"",size=(200,100),style=wx.TE_MULTILINE)
    rBoxSizer.Add(self.rationaleCtrl,0,wx.EXPAND)
    self.tensionsCtrl.setRationaleCtrl(self.rationaleCtrl)
    self.SetSizer(topSizer)

  def onSelectRationale(self,evt):
    if (self.thePrevRow != -1 or self.thePrevCol != -1):
      lastRationale = self.rationaleCtrl.GetValue()
      self.tensionsCtrl.setRationale(self.thePrevRow,self.thePrevCol,lastRationale)
    currentRow = evt.GetRow()
    currentCol = evt.GetCol()
    tRat = self.tensionsCtrl.rationale(currentRow,currentCol)
    self.rationaleCtrl.SetValue(tRat)
    self.thePrevRow = currentRow
    self.thePrevCol = currentCol
    evt.Skip()
    

class EnvironmentNotebook(wx.Notebook):
  def __init__(self,parent,dp):
    wx.Notebook.__init__(self,parent,ENVIRONMENT_NOTEBOOKENVIRONMENT_ID)
    p1 = SummaryPage(self)
    p2 = CompositePage(self,dp)
    p3 = TensionsPage(self)
    self.AddPage(p1,'Summary')
    self.AddPage(p2,'Composite')
    self.AddPage(p3,'Tensions')
