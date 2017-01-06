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
from cairis.core.ARM import *
from cairis.core.Borg import Borg
from PatternStructureDialog import PatternStructureDialog

__author__ = 'Shamal Faily'

class PatternStructureListCtrl(wx.ListCtrl):
  def __init__(self,parent,winId = SECURITYPATTERN_LISTPATTERNSTRUCTURE_ID):
    wx.ListCtrl.__init__(self,parent,winId,size=wx.DefaultSize,style=wx.LC_REPORT)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.InsertColumn(0,'Head Asset')
    self.SetColumnWidth(0,100)
    self.InsertColumn(1,'Type')
    self.SetColumnWidth(1,75)
    self.InsertColumn(2,'Nav')
    self.SetColumnWidth(2,75)
    self.InsertColumn(3,'Nry')
    self.SetColumnWidth(3,50)
    self.InsertColumn(4,'Role')
    self.SetColumnWidth(4,50)
    self.InsertColumn(5,'Tail Role')
    self.SetColumnWidth(5,50)
    self.InsertColumn(6,'Tail Nry')
    self.SetColumnWidth(6,50)
    self.InsertColumn(7,'Tail Nav')
    self.SetColumnWidth(7,75)
    self.InsertColumn(8,'Tail Type')
    self.SetColumnWidth(8,75)
    self.InsertColumn(9,'Tail Asset')
    self.SetColumnWidth(9,100)
    self.theSelectedIdx = -1
    self.theDimMenu = wx.Menu()
    self.theDimMenu.Append(AA_MENUADD_ID,'Add')
    self.theDimMenu.Append(AA_MENUDELETE_ID,'Delete')
    self.Bind(wx.EVT_RIGHT_DOWN,self.OnRightDown)
    wx.EVT_MENU(self.theDimMenu,AA_MENUADD_ID,self.onAddAssociation)
    wx.EVT_MENU(self.theDimMenu,AA_MENUDELETE_ID,self.onDeleteAssociation)

    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.onAssetActivated)

  def OnRightDown(self,evt):
    self.PopupMenu(self.theDimMenu)

  def onAddAssociation(self,evt):
    dlg = PatternStructureDialog(self)
    if (dlg.ShowModal() == PATTERNSTRUCTURE_BUTTONCOMMIT_ID):
      self.theSelectedIdx = self.GetItemCount()
      self.InsertStringItem(self.theSelectedIdx,dlg.headAsset())
      self.SetStringItem(self.theSelectedIdx,1,dlg.headAdornment())
      self.SetStringItem(self.theSelectedIdx,2,dlg.headNavigation())
      self.SetStringItem(self.theSelectedIdx,3,dlg.headMultiplicity())
      self.SetStringItem(self.theSelectedIdx,4,dlg.headRole())
      self.SetStringItem(self.theSelectedIdx,5,dlg.tailRole())
      self.SetStringItem(self.theSelectedIdx,6,dlg.tailMultiplicity())
      self.SetStringItem(self.theSelectedIdx,7,dlg.tailNavigation())
      self.SetStringItem(self.theSelectedIdx,8,dlg.tailAdornment())
      self.SetStringItem(self.theSelectedIdx,9,dlg.tailAsset())

  def onDeleteAssociation(self,evt):
    if (self.theSelectedIdx == -1):
      errorText = 'No association selected'
      errorLabel = 'Delete asset association'
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

  def onAssetActivated(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    headAsset = self.GetItemText(self.theSelectedIdx)
    headAdornment = self.GetItem(self.theSelectedIdx,1)
    headNav = self.GetItem(self.theSelectedIdx,2)
    headNry = self.GetItem(self.theSelectedIdx,3)
    headRole = self.GetItem(self.theSelectedIdx,4)
    tailRole = self.GetItem(self.theSelectedIdx,5)
    tailNry = self.GetItem(self.theSelectedIdx,6)
    tailNav = self.GetItem(self.theSelectedIdx,7)
    tailAdornment = self.GetItem(self.theSelectedIdx,8)
    tailAsset = self.GetItem(self.theSelectedIdx,9)
     
    dlg = PatternStructureDialog(self,headAsset,headAdornment.GetText(),headNav.GetText(),headNry.GetText(),headRole.GetText(),tailRole.GetText(),tailNry.GetText(),tailNav.GetText(),tailAdornment.GetText(),tailAsset.GetText())
    if (dlg.ShowModal() == PATTERNSTRUCTURE_BUTTONCOMMIT_ID):
      self.SetStringItem(self.theSelectedIdx,0,dlg.headAsset())
      self.SetStringItem(self.theSelectedIdx,1,dlg.headAdornment())
      self.SetStringItem(self.theSelectedIdx,2,dlg.headNavigation())
      self.SetStringItem(self.theSelectedIdx,3,dlg.headMultiplicity())
      self.SetStringItem(self.theSelectedIdx,4,dlg.headRole())
      self.SetStringItem(self.theSelectedIdx,5,dlg.tailRole())
      self.SetStringItem(self.theSelectedIdx,6,dlg.tailMultiplicity())
      self.SetStringItem(self.theSelectedIdx,7,dlg.tailNavigation())
      self.SetStringItem(self.theSelectedIdx,8,dlg.tailAdornment())
      self.SetStringItem(self.theSelectedIdx,9,dlg.tailAsset())

  def load(self,assocs):
    import pytest
    pytest.set_trace()
    for headAsset,headAdornment,headNry,headRole,tailRole,tailNry,tailAdornment,tailAsset in assocs:
      headNav = 0
      tailNav = 0
      idx = self.GetItemCount()
      self.InsertStringItem(idx,headAsset)
      self.SetStringItem(idx,1,headAdornment)
      self.SetStringItem(idx,2,str(headNav))
      self.SetStringItem(idx,3,headNry)
      self.SetStringItem(idx,4,headRole)
      self.SetStringItem(idx,5,tailRole)
      self.SetStringItem(idx,6,tailNry)
      self.SetStringItem(idx,7,str(tailNav))
      self.SetStringItem(idx,8,tailAdornment)
      self.SetStringItem(idx,9,tailAsset)

  def associations(self):
    assocs = []
    for x in range(self.GetItemCount()):
      headAsset = self.GetItemText(x)
      headAdornment = self.GetItem(x,1)
      headNav = self.GetItem(x,2)
      headNry = self.GetItem(x,3)
      headRole = self.GetItem(x,4)
      tailRole = self.GetItem(x,5)
      tailNry = self.GetItem(x,6)
      tailNav = self.GetItem(x,7)
      tailAdornment = self.GetItem(x,8)
      tailAsset = self.GetItem(x,9)
      assocs.append((headAsset,headAdornment.GetText(),int(headNav.GetText()),headNry.GetText(),headRole.GetText(),tailRole.GetText(),tailNry.GetText(),int(tailNav.GetText()),tailAdornment.GetText(),tailAsset.GetText()))
    return assocs

  def assets(self):
    assets = set([])
    for x in range(self.GetItemCount()):
      assets.add(self.GetItemText(x))
      assets.add(((self.GetItem(x,7))).GetText())
    return list(assets)

