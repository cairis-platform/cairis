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
from InterfaceListDialog import InterfaceListDialog

class InterfaceListCtrl(wx.ListCtrl):
  def __init__(self,parent,winId):
    wx.ListCtrl.__init__(self,parent,winId,size=wx.DefaultSize,style=wx.LC_REPORT)
    self.InsertColumn(0,'Interface')
    self.SetColumnWidth(0,200)
    self.InsertColumn(1,'Type')
    self.SetColumnWidth(1,100)
    self.theSelectedIdx = -1
    self.theDimMenu = wx.Menu()
    self.theDimMenu.Append(armid.INTERFACELIST_MENUADD_ID,'Add')
    self.theDimMenu.Append(armid.INTERFACELIST_MENUDELETE_ID,'Delete')
    self.Bind(wx.EVT_RIGHT_DOWN,self.OnRightDown)
    wx.EVT_MENU(self.theDimMenu,armid.INTERFACELIST_MENUADD_ID,self.onAddInterface)
    wx.EVT_MENU(self.theDimMenu,armid.INTERFACELIST_MENUDELETE_ID,self.onDeleteInterface)

    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.onInterfaceActivated)

  def OnRightDown(self,evt):
    self.PopupMenu(self.theDimMenu)

  def onAddInterface(self,evt):
    dlg = InterfaceListDialog(self)
    if (dlg.ShowModal() == wx.ID_OK):
      self.theSelectedIdx = self.GetItemCount()
      self.InsertStringItem(self.theSelectedIdx,dlg.interface())
      self.SetStringItem(self.theSelectedIdx,1,dlg.interfaceType())

  def onDeleteInterface(self,evt):
    if (self.theSelectedIdx == -1):
      errorText = 'No interface selected'
      errorLabel = 'Delete interface'
      dlg = wx.MessageDialog(self,errorText,errorLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
    else:
      selectedValue = self.GetItemText(self.theSelectedIdx)
      self.DeleteItem(self.theSelectedIdx)

  
  def OnItemSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()

  def OnItemDeselected(self,evt):
    self.theSelectedIdx = -1

  def onInterfaceActivated(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    ifName = self.GetItemText(self.theSelectedIdx)
    ifType = self.GetItem(self.theSelectedIdx,1)
     
    dlg = InterfaceListDialog(self,ifName,ifType.GetText())
    if (dlg.ShowModal() == wx.ID_OK):
      self.SetStringItem(self.theSelectedIdx,0,dlg.interface())
      self.SetStringItem(self.theSelectedIdx,1,dlg.interfaceType())

  def load(self,ifs):
    print ifs
    for ifName,ifType in ifs:
      idx = self.GetItemCount()
      self.InsertStringItem(idx,ifName)
      self.SetStringItem(idx,1,ifType)

  def dimensions(self):
    ifs = []
    for x in range(self.GetItemCount()):
      ifName = self.GetItemText(x)
      ifType = self.GetItem(x,1)
      ifs.append((ifName,ifType.GetText()))
    return ifs
