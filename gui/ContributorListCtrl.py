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
from ContributorEntryDialog import ContributorEntryDialog

class ContributorListCtrl(wx.ListCtrl):
  def __init__(self,parent):
    wx.ListCtrl.__init__(self,parent,armid.PROJECTSETTINGS_LISTCONTRIBUTORS_ID,size=wx.DefaultSize,style=wx.LC_REPORT | wx.LC_SORT_ASCENDING)
    self.InsertColumn(0,'Firstname')
    self.SetColumnWidth(0,100)
    self.InsertColumn(1,'Surname')
    self.SetColumnWidth(0,100)
    self.InsertColumn(2,'Affiliation')
    self.SetColumnWidth(2,100)
    self.InsertColumn(3,'Role')
    self.SetColumnWidth(3,100)
    self.theSelectedIdx = -1
    self.theMenu = wx.Menu()
    self.theMenu.Append(armid.CONTRIBUTORLISTCTRL_MENUADD_ID,'Add')
    self.theMenu.Append(armid.CONTRIBUTORLISTCTRL_MENUDELETE_ID,'Delete')
    self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK,self.OnRightDown)
    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.onEntryActivated)
    wx.EVT_MENU(self.theMenu,armid.CONTRIBUTORLISTCTRL_MENUADD_ID,self.onAddEntry)
    wx.EVT_MENU(self.theMenu,armid.CONTRIBUTORLISTCTRL_MENUDELETE_ID,self.onDeleteEntry)

  def OnItemSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()

  def OnItemDeselected(self,evt):
    self.theSelectedIdx = -1

  def OnRightDown(self,evt):
    self.PopupMenu(self.theMenu)

  def onAddEntry(self,evt):
    dlg = ContributorEntryDialog(self)
    if (dlg.ShowModal() == armid.CONTRIBUTORENTRY_BUTTONCOMMIT_ID):
      firstName = dlg.firstName()
      surname = dlg.surname()
      affiliation = dlg.affiliation()
      role = dlg.role()
      idx = self.GetItemCount()
      self.InsertStringItem(idx,firstName)
      self.SetStringItem(idx,1,surname)
      self.SetStringItem(idx,2,affiliation)
      self.SetStringItem(idx,3,role)

  def onDeleteEntry(self,evt):
    if (self.theSelectedIdx == -1):
      errorText = 'No entry selected'
      errorLabel = 'Delete definition'
      dlg = wx.MessageDialog(self,errorText,errorLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
    else:
      selectedValue = self.GetItemText(self.theSelectedIdx)
      self.DeleteItem(self.theSelectedIdx)

  def onEntryActivated(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    firstName = self.GetItemText(self.theSelectedIdx)
    surname = self.GetItem(self.theSelectedIdx,1)
    affiliation = self.GetItem(self.theSelectedIdx,2)
    role = self.GetItem(self.theSelectedIdx,3)
     
    dlg = ContributorEntryDialog(self,firstName,surname.GetText(),affiliation.GetText(),role.GetText())
    if (dlg.ShowModal() == armid.CONTRIBUTORENTRY_BUTTONCOMMIT_ID):
      self.SetStringItem(self.theSelectedIdx,0,dlg.firstName())
      self.SetStringItem(self.theSelectedIdx,1,dlg.surname())
      self.SetStringItem(self.theSelectedIdx,2,dlg.affiliation())
      self.SetStringItem(self.theSelectedIdx,3,dlg.role())

  def load(self,entries):
    for firstName,surname,affiliation,role in entries:
      idx = self.GetItemCount()
      self.InsertStringItem(idx,firstName)
      self.SetStringItem(idx,1,surname)
      self.SetStringItem(idx,2,affiliation)
      self.SetStringItem(idx,3,role)

  def dimensions(self):
    entries = []
    for x in range(self.GetItemCount()):
      firstName = self.GetItemText(x)
      surname = self.GetItem(x,1)
      affiliation = self.GetItem(x,2)
      role = self.GetItem(x,3)
      entries.append((firstName,surname.GetText(),affiliation.GetText(),role.GetText()))
    return entries
