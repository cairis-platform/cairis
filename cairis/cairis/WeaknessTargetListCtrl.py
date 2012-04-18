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
import ARM
from Borg import Borg

class WeaknessTargetListCtrl(wx.ListCtrl):
  def __init__(self,parent,winId):
    wx.ListCtrl.__init__(self,parent,winId,size=wx.DefaultSize,style=wx.LC_REPORT)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theViewName = ''
    self.theComponents = []
    self.InsertColumn(0,'Target')
    self.SetColumnWidth(0,100)
    self.InsertColumn(1,'Components')
    self.SetColumnWidth(1,100)
    self.InsertColumn(2,'Assets')
    self.SetColumnWidth(2,100)
    self.theSelectedIdx = -1
    self.theDimMenu = wx.Menu()
    self.theDimMenu.Append(armid.AA_MENUADD_ID,'Add')
    self.theDimMenu.Append(armid.AA_MENUDELETE_ID,'Delete')
    self.Bind(wx.EVT_RIGHT_DOWN,self.OnRightDown)
    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.onTargetActivated)

  def OnRightDown(self,evt):
    self.PopupMenu(self.theDimMenu)

  def OnItemSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()

  def OnItemDeselected(self,evt):
    self.theSelectedIdx = -1

  def onTargetActivated(self,evt):
    self.theSelectedIdx = evt.GetIndex()
#    dlg = ComponentDialog(self)
#    inParameters = self.theComponents[self.theSelectedIdx]
#    dlg.load(inParameters)
#    if (dlg.ShowModal() == armid.COMPONENT_BUTTONCOMMIT_ID):
#      outParameters = dlg.parameters()
#      self.theComponents[self.theSelectedIdx] = outParameters
#      self.SetStringItem(self.theSelectedIdx,0,outParameters.name())
#      self.SetStringItem(self.theSelectedIdx,1,outParameters.description())

  def load(self,targets):
    for targetName,components,assets in self.theTargetss:
      idx = self.GetItemCount()
      self.InsertStringItem(idx,targetName)
      self.SetStringItem(idx,1,components)
      self.SetStringItem(idx,2,assets)

  def dimensions(self):
    return []
