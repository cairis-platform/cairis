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
from ComponentListCtrl import ComponentListCtrl
from ConnectorListCtrl import ConnectorListCtrl

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

class ComponentPage(wx.Panel):
  def __init__(self,parent,winId):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)
    asBox = wx.StaticBox(self,-1)
    asBoxSizer = wx.StaticBoxSizer(asBox,wx.HORIZONTAL)
    topSizer.Add(asBoxSizer,1,wx.EXPAND)
    self.componentList = ComponentListCtrl(self,winId)
    asBoxSizer.Add(self.componentList,1,wx.EXPAND)
    self.SetSizer(topSizer)

class ConnectorPage(wx.Panel):
  def __init__(self,parent,winId):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)
    asBox = wx.StaticBox(self,-1)
    asBoxSizer = wx.StaticBoxSizer(asBox,wx.HORIZONTAL)
    topSizer.Add(asBoxSizer,1,wx.EXPAND)
    self.connectorList = ConnectorListCtrl(self,winId)
    asBoxSizer.Add(self.connectorList,1,wx.EXPAND)
    self.SetSizer(topSizer)

class ComponentViewNotebook(wx.Notebook):
  def __init__(self,parent):
    wx.Notebook.__init__(self,parent,COMPONENTVIEW_NOTEBOOKCOMPONENTVIEW_ID)
    p1 = MLTextPage(self,COMPONENTVIEW_TEXTSYNOPSIS_ID)
    p2 = ComponentPage(self,COMPONENTVIEW_LISTCOMPONENTS_ID)
    p3 = ConnectorPage(self,COMPONENTVIEW_LISTCONNECTORS_ID)
    self.AddPage(p1,'Synopsis')
    self.AddPage(p2,'Components')
    self.AddPage(p3,'Connectors')

  def setView(self,cvName):
    componentList = self.FindWindowById(COMPONENTVIEW_LISTCOMPONENTS_ID)
    connectorList = self.FindWindowById(COMPONENTVIEW_LISTCONNECTORS_ID)
    componentList.setView(cvName)
    connectorList.setView(cvName)
