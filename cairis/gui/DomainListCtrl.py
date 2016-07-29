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
from DomainEntryDialog import DomainEntryDialog

__author__ = 'Shamal Faily'

class DomainListCtrl(wx.ListCtrl):
  def __init__(self,parent,winId):
    wx.ListCtrl.__init__(self,parent,winId,size=wx.DefaultSize,style=wx.LC_REPORT | wx.LC_SORT_ASCENDING)
    self.InsertColumn(0,'Domain')
    self.SetColumnWidth(0,100)
    self.InsertColumn(1,'Phenomena')
    self.SetColumnWidth(1,300)
    self.InsertColumn(2,'Connection Domain')
    self.SetColumnWidth(2,100)
    self.theSelectedIdx = -1
    self.theMenu = wx.Menu()
    self.theMenu.Append(DOMAINLISTCTRL_MENUADD_ID,'Add')
    self.theMenu.Append(DOMAINLISTCTRL_MENUDELETE_ID,'Delete')
    self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK,self.OnRightDown)
    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    wx.EVT_MENU(self.theMenu,DOMAINLISTCTRL_MENUADD_ID,self.onAddEntry)
    wx.EVT_MENU(self.theMenu,DOMAINLISTCTRL_MENUDELETE_ID,self.onDeleteEntry)

  def OnItemSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()

  def OnItemDeselected(self,evt):
    self.theSelectedIdx = -1

  def OnRightDown(self,evt):
    self.PopupMenu(self.theMenu)

  def onAddEntry(self,evt):
    dlg = DomainEntryDialog(self)
    if (dlg.ShowModal() == DOMAINENTRY_BUTTONCOMMIT_ID):
      domainName = dlg.domain()
      domainPhenomena = dlg.phenomena()
      connectionDomain = dlg.connectionDomain()
      idx = self.GetItemCount()
      self.InsertStringItem(idx,domainName)
      self.SetStringItem(idx,1,domainPhenomena)
      self.SetStringItem(idx,2,connectionDomain)

  def onDeleteEntry(self,evt):
    if (self.theSelectedIdx == -1):
      errorText = 'No entry selected'
      errorLabel = 'Delete domain association'
      dlg = wx.MessageDialog(self,errorText,errorLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
    else:
      selectedValue = self.GetItemText(self.theSelectedIdx)
      self.DeleteItem(self.theSelectedIdx)


  def load(self,entries):
    for association in entries:
      idx = self.GetItemCount()
      self.InsertStringItem(idx,association.tailDomain())
      self.SetStringItem(idx,1,association.phenomena())
      self.SetStringItem(idx,2,association.connectionDomain())

  def dimensions(self):
    entries = []
    for x in range(self.GetItemCount()):
      domainName = self.GetItemText(x)
      domainPhenomena = self.GetItem(x,1)
      connectionDomain = self.GetItem(x,2)
      entries.append((domainName,domainPhenomena.GetText(),connectionDomain.GetText()))
    return entries
