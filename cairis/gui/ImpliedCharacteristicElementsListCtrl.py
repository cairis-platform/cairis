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
from cairis.core.Borg import Borg
from CharacteristicReferenceTypeDialog import CharacteristicReferenceTypeDialog

class ImpliedCharacteristicElementsListCtrl(wx.ListCtrl):
  def __init__(self,parent,winId,elements):
    wx.ListCtrl.__init__(self,parent,winId,size=wx.DefaultSize,style=wx.LC_REPORT | wx.LC_SORT_ASCENDING)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theParentDialog = parent

    self.InsertColumn(0,'Element')
    self.SetColumnWidth(0,200)
    self.InsertColumn(1,'Type')
    self.SetColumnWidth(1,100)
    self.theSelectedIdx = -1
    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.onItemActivated)

    for elName,elType in elements:
      idx = self.GetItemCount()
      self.InsertStringItem(idx,elName)
      self.SetStringItem(idx,1,elType)

  def OnItemSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()

  def OnItemDeselected(self,evt):
    self.theSelectedIdx = -1

  def onItemActivated(self,evt):
    elName = self.GetItem(self.theSelectedIdx,0)
    elType = self.GetItem(self.theSelectedIdx,1)
    intCtrl = self.theParentDialog.FindWindowById(IMPLIEDCHARACTERISTIC_TEXTINTENTION_ID)
    intName = intCtrl.GetValue()
    dlg = CharacteristicReferenceTypeDialog(self,intName,elName.GetText(),elType.GetText())
    if (dlg.ShowModal() == CHARACTERISTICREFERENCETYPE_BUTTONCOMMIT_ID):
      modElType = dlg.value()
      self.SetStringItem(self.theSelectedIdx,1,modElType)


  def dimensions(self):
    entries = []
    for x in range(self.GetItemCount()):
      elName = self.GetItemText(x)
      elType = self.GetItem(x,1)
      entries.append((elName,elType.GetText()))
    return entries
