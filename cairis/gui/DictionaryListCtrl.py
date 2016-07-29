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
from DictionaryEntryDialog import DictionaryEntryDialog

__author__ = 'Shamal Faily'

class DictionaryListCtrl(wx.ListCtrl):
  def __init__(self,parent):
    wx.ListCtrl.__init__(self,parent,PROJECTSETTINGS_LISTDICTIONARY_ID,size=wx.DefaultSize,style=wx.LC_REPORT | wx.LC_SORT_ASCENDING)
    self.keys = []
    self.InsertColumn(0,'Name')
    self.SetColumnWidth(0,150)
    self.InsertColumn(1,'Definition')
    self.SetColumnWidth(1,300)
    self.theSelectedIdx = -1
    self.theMenu = wx.Menu()
    self.theMenu.Append(DICTIONARYLISTCTRL_MENUADD_ID,'Add')
    self.theMenu.Append(DICTIONARYLISTCTRL_MENUDELETE_ID,'Delete')
    self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK,self.OnRightDown)
    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.onEntryActivated)
    wx.EVT_MENU(self.theMenu,DICTIONARYLISTCTRL_MENUADD_ID,self.onAddEntry)
    wx.EVT_MENU(self.theMenu,DICTIONARYLISTCTRL_MENUDELETE_ID,self.onDeleteEntry)

  def OnItemSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()

  def OnItemDeselected(self,evt):
    self.theSelectedIdx = -1

  def OnRightDown(self,evt):
    self.PopupMenu(self.theMenu)

  def onAddEntry(self,evt):
    dlg = DictionaryEntryDialog(self)
    if (dlg.ShowModal() == DICTIONARYENTRY_BUTTONCOMMIT_ID):
      name = dlg.name()
      definition = dlg.definition()
      idx = self.GetItemCount()
      self.InsertStringItem(idx,name)
      self.SetStringItem(idx,1,definition)

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
    name = self.GetItemText(self.theSelectedIdx)
    definition = self.GetItem(self.theSelectedIdx,1)
     
    dlg = DictionaryEntryDialog(self,name,definition.GetText())
    if (dlg.ShowModal() == DICTIONARYENTRY_BUTTONCOMMIT_ID):
      self.SetStringItem(self.theSelectedIdx,0,dlg.name())
      self.SetStringItem(self.theSelectedIdx,1,dlg.definition())

  def load(self,entries):
    self.keys = entries.keys()
    self.keys.sort()
    
    for name in self.keys:
      idx = self.GetItemCount()
      self.InsertStringItem(idx,name)
      self.SetStringItem(idx,1,entries[name])

  def dimensions(self):
    entries = []
    for x in range(self.GetItemCount()):
      name = self.GetItemText(x)
      definition = self.GetItem(x,1)
      entries.append((name,definition.GetText()))
    return entries
