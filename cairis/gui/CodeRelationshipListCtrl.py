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
from CodeRelationshipDialog import CodeRelationshipDialog
from ImpliedCharacteristicDialog import ImpliedCharacteristicDialog
from cairis.core.Borg import Borg

class CodeRelationshipListCtrl(wx.ListCtrl):
  def __init__(self,parent,personaName):
    wx.ListCtrl.__init__(self,parent,CODERELATIONSHIP_LISTRELATIONSHIPS_ID,size=wx.DefaultSize,style=wx.LC_REPORT | wx.LC_SORT_ASCENDING)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.rtLookup = {'associated':'==','implies':'=>','conflict':'<>','part-of':'[]'}
    self.thePersonaName = personaName

    self.InsertColumn(0,'From')
    self.SetColumnWidth(0,150)
    self.InsertColumn(1,'Relationship')
    self.SetColumnWidth(1,75)
    self.InsertColumn(2,'To')
    self.SetColumnWidth(2,150)
    self.theSelectedIdx = -1
    self.theLastRevision = 0
    self.theMenu = wx.Menu()
    self.theMenu.Append(CODERELATIONSHIPLISTCTRL_MENUADD_ID,'Add')
    self.deleteMenu = self.theMenu.Append(CODERELATIONSHIPLISTCTRL_MENUDELETE_ID,'Delete')
    self.deleteMenu.Enable(False)
    self.charMenu = self.theMenu.Append(CODERELATIONSHIPLISTCTRL_MENUCHARACTERISTICS_ID,'Set Implied Characteristic')
    self.charMenu.Enable(False)
    self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK,self.OnRightDown)
    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.onItemActivated)

    wx.EVT_MENU(self.theMenu,CODERELATIONSHIPLISTCTRL_MENUADD_ID,self.onAddRelationship)
    wx.EVT_MENU(self.theMenu,CODERELATIONSHIPLISTCTRL_MENUDELETE_ID,self.onDeleteRelationship)
    wx.EVT_MENU(self.theMenu,CODERELATIONSHIPLISTCTRL_MENUCHARACTERISTICS_ID,self.onEditCharacteristics)

    for fromName,fromType,toName,toType,rType in self.dbProxy.personaCodeNetwork(personaName):
      idx = self.GetItemCount()
      self.InsertStringItem(idx,fromName)
      self.SetStringItem(idx,1,rType)
      self.SetStringItem(idx,2,toName)

  def OnItemSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    self.charMenu.Enable(True)
    self.deleteMenu.Enable(True)

  def OnItemDeselected(self,evt):
    self.theSelectedIdx = -1
    self.charMenu.Enable(False)
    self.deleteMenu.Enable(False)

  def OnRightDown(self,evt):
    self.PopupMenu(self.theMenu)

  def onAddRelationship(self,evt):
    dlg = CodeRelationshipDialog(self)
    if (dlg.ShowModal() == CODERELATIONSHIP_BUTTONADD_ID):
      idx = self.GetItemCount()
      fromName = dlg.fromName()
      toName = dlg.toName()
      rshipType = dlg.relationship()
      self.InsertStringItem(idx,fromName)
      self.SetStringItem(idx,1,rshipType)
      self.SetStringItem(idx,2,toName)

  def onItemActivated(self,evt):
    fromName = self.GetItemText(self.theSelectedIdx)
    rType = self.GetItem(self.theSelectedIdx,1)
    toName = self.GetItem(self.theSelectedIdx,2)
    dlg = CodeRelationshipDialog(self,fromName,toName.GetText(),rType.GetText())
    if (dlg.ShowModal() == CODERELATIONSHIP_BUTTONADD_ID):
      fromName = dlg.fromName()
      toName = dlg.toName()
      rshipType = dlg.relationship()
      self.SetStringItem(self.theSelectedIdx,0,fromName)
      self.SetStringItem(self.theSelectedIdx,1,rshipType)
      self.SetStringItem(self.theSelectedIdx,2,toName)


  def onDeleteRelationship(self,evt):
    if (self.theSelectedIdx == -1):
      errorText = 'No relatioship selected'
      errorLabel = 'Delete Code Relationship'
      dlg = wx.MessageDialog(self,errorText,errorLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
    else:
      self.DeleteItem(self.theSelectedIdx)

  def onEditCharacteristics(self,evt):
    fromName = self.GetItemText(self.theSelectedIdx)
    rType = self.GetItem(self.theSelectedIdx,1)
    toName = self.GetItem(self.theSelectedIdx,2)
    dlg = ImpliedCharacteristicDialog(self,self.thePersonaName,fromName,toName.GetText(),rType.GetText())
    dlg.ShowModal()

  def dimensions(self):
    entries = []
    for x in range(self.GetItemCount()):
      fromName = self.GetItemText(x)
      rType = self.GetItem(x,1)
      toName = self.GetItem(x,2)
      entries.append((fromName,toName.GetText(),rType.GetText()))
    return entries
