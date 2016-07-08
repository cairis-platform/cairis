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
from PatternStructureListCtrl import PatternStructureListCtrl
from DimensionListCtrl import DimensionListCtrl
from InterfacePage import InterfacePage
from cairis.core.Borg import Borg

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

class StructurePage(wx.Panel):
  def __init__(self,parent,winId):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)
    asBox = wx.StaticBox(self,-1)
    asBoxSizer = wx.StaticBoxSizer(asBox,wx.HORIZONTAL)
    topSizer.Add(asBoxSizer,1,wx.EXPAND)
    self.associationList = PatternStructureListCtrl(self,winId)
    asBoxSizer.Add(self.associationList,1,wx.EXPAND)
    self.SetSizer(topSizer)

class RequirementsPage(wx.Panel):
  def __init__(self,parent,structPage):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)
    asBox = wx.StaticBox(self,-1)
    asBoxSizer = wx.StaticBoxSizer(asBox,wx.HORIZONTAL)
    topSizer.Add(asBoxSizer,1,wx.EXPAND)
    b = Borg()
    self.requirementList = DimensionListCtrl(self,COMPONENT_LISTREQUIREMENTS_ID,wx.DefaultSize,'Requirement','template_requirement',b.dbProxy)
    asBoxSizer.Add(self.requirementList,1,wx.EXPAND)
    self.SetSizer(topSizer)

class GoalsPage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)
    asBox = wx.StaticBox(self,-1)
    asBoxSizer = wx.StaticBoxSizer(asBox,wx.HORIZONTAL)
    topSizer.Add(asBoxSizer,1,wx.EXPAND)
    b = Borg()
    self.goalList = DimensionListCtrl(self,COMPONENT_LISTGOALS_ID,wx.DefaultSize,'Goal','template_goal',b.dbProxy)
    asBoxSizer.Add(self.goalList,1,wx.EXPAND)
    self.SetSizer(topSizer)

class ComponentNotebook(wx.Notebook):
  def __init__(self,parent):
    wx.Notebook.__init__(self,parent,SECURITYPATTERN_NOTEBOOKPATTERN_ID)
    p1 = MLTextPage(self,COMPONENT_TEXTDESCRIPTION_ID)
    p2 = InterfacePage(self,COMPONENT_LISTINTERFACES_ID)
    p3 = StructurePage(self,COMPONENT_LISTSTRUCTURE_ID)
    p4 = RequirementsPage(self,p3)
    p5 = GoalsPage(self)
    self.AddPage(p1,'Description')
    self.AddPage(p2,'Interfaces')
    self.AddPage(p3,'Structure')
    self.AddPage(p4,'Requirements')
    self.AddPage(p5,'Goals')
