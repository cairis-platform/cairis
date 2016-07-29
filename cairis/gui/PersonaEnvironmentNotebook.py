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
from BVNarrativeTextCtrl import BVNarrativeTextCtrl

__author__ = 'Shamal Faily'

class SummaryPage(wx.Panel):
  def __init__(self,parent,dp):
    wx.Panel.__init__(self,parent)
    self.dbProxy = dp
    topSizer = wx.BoxSizer(wx.VERTICAL)

    directBox = wx.StaticBox(self,-1,'Direct/Indirect Persona')
    directSizer = wx.StaticBoxSizer(directBox,wx.HORIZONTAL)
    topSizer.Add(directSizer,0,wx.EXPAND)
    self.directCtrl = wx.CheckBox(self,PERSONA_CHECKDIRECT_ID)
    self.directCtrl.SetValue(True)
    directSizer.Add(self.directCtrl,0,wx.EXPAND)

    roleBox = wx.StaticBox(self)
    roleSizer = wx.StaticBoxSizer(roleBox,wx.HORIZONTAL)
    topSizer.Add(roleSizer,1,wx.EXPAND)
    self.roleList = DimensionListCtrl(self,PERSONA_LISTROLES_ID,wx.DefaultSize,'Role','role',self.dbProxy)
    roleSizer.Add(self.roleList,1,wx.EXPAND)

    self.SetSizer(topSizer)

class NarrativePage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    narrativeBox = wx.StaticBox(self,-1)
    narrativeBoxSizer = wx.StaticBoxSizer(narrativeBox,wx.HORIZONTAL)
    topSizer.Add(narrativeBoxSizer,1,wx.EXPAND)
    self.narrativeCtrl = BVNarrativeTextCtrl(self,PERSONA_TEXTNARRATIVE_ID)
    narrativeBoxSizer.Add(self.narrativeCtrl,1,wx.EXPAND)

    self.SetSizer(topSizer)

class PersonaEnvironmentNotebook(wx.Notebook):
  def __init__(self,parent,dp):
    wx.Notebook.__init__(self,parent,PERSONA_NOTEBOOKENVIRONMENT_ID)
    p1 = SummaryPage(self,dp)
    p2 = NarrativePage(self)
    self.AddPage(p1,'Summary')
    self.AddPage(p2,'Narrative')
