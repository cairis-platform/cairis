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
from PatternStructureDialog import PatternStructureDialog

class PatternStructureListCtrl(wx.ListCtrl):
  def __init__(self,parent):
    wx.ListCtrl.__init__(self,parent,armid.SECURITYPATTERN_LISTPATTERNSTRUCTURE_ID,size=wx.DefaultSize,style=wx.LC_REPORT)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.InsertColumn(0,'Head Asset')
    self.SetColumnWidth(0,100)
    self.InsertColumn(1,'Type')
    self.SetColumnWidth(1,75)
    self.InsertColumn(2,'Nry')
    self.SetColumnWidth(2,50)
    self.InsertColumn(3,'Role')
    self.SetColumnWidth(3,50)
    self.InsertColumn(4,'Tail Role')
    self.SetColumnWidth(4,50)
    self.InsertColumn(5,'Tail Nry')
    self.SetColumnWidth(5,50)
    self.InsertColumn(6,'Tail Type')
    self.SetColumnWidth(6,75)
    self.InsertColumn(7,'Tail Asset')
    self.SetColumnWidth(7,100)
    self.theSelectedIdx = -1
    self.theDimMenu = wx.Menu()
    self.theDimMenu.Append(armid.AA_MENUADD_ID,'Add')
    self.theDimMenu.Append(armid.AA_MENUDELETE_ID,'Delete')
    self.Bind(wx.EVT_RIGHT_DOWN,self.OnRightDown)
    wx.EVT_MENU(self.theDimMenu,armid.AA_MENUADD_ID,self.onAddAssociation)
    wx.EVT_MENU(self.theDimMenu,armid.AA_MENUDELETE_ID,self.onDeleteAssociation)

    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.onAssetActivated)

  def OnRightDown(self,evt):
    self.PopupMenu(self.theDimMenu)

  def onAddAssociation(self,evt):
    dlg = PatternStructureDialog(self)
    if (dlg.ShowModal() == armid.PATTERNSTRUCTURE_BUTTONCOMMIT_ID):
      self.theSelectedIdx = self.GetItemCount()
      self.InsertStringItem(self.theSelectedIdx,dlg.headAsset())
      self.SetStringItem(self.theSelectedIdx,1,dlg.headAdornment())
      self.SetStringItem(self.theSelectedIdx,2,dlg.headMultiplicity())
      self.SetStringItem(self.theSelectedIdx,3,dlg.headRole())
      self.SetStringItem(self.theSelectedIdx,4,dlg.tailRole())
      self.SetStringItem(self.theSelectedIdx,5,dlg.tailMultiplicity())
      self.SetStringItem(self.theSelectedIdx,6,dlg.tailAdornment())
      self.SetStringItem(self.theSelectedIdx,7,dlg.tailAsset())

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
    headNry = self.GetItem(self.theSelectedIdx,2)
    headRole = self.GetItem(self.theSelectedIdx,3)
    tailRole = self.GetItem(self.theSelectedIdx,4)
    tailNry = self.GetItem(self.theSelectedIdx,5)
    tailAdornment = self.GetItem(self.theSelectedIdx,6)
    tailAsset = self.GetItem(self.theSelectedIdx,7)
     
    dlg = PatternStructureDialog(self,headAsset,headAdornment.GetText(),headNry.GetText(),headRole.GetText(),tailRole.GetText(),tailNry.GetText(),tailAdornment.GetText(),tailAsset.GetText())
    if (dlg.ShowModal() == armid.PATTERNSTRUCTURE_BUTTONCOMMIT_ID):
      self.SetStringItem(self.theSelectedIdx,0,dlg.headAsset())
      self.SetStringItem(self.theSelectedIdx,1,dlg.headAdornment())
      self.SetStringItem(self.theSelectedIdx,2,dlg.headMultiplicity())
      self.SetStringItem(self.theSelectedIdx,3,dlg.headRole())
      self.SetStringItem(self.theSelectedIdx,4,dlg.tailRole())
      self.SetStringItem(self.theSelectedIdx,5,dlg.tailMultiplicity())
      self.SetStringItem(self.theSelectedIdx,6,dlg.tailAdornment())
      self.SetStringItem(self.theSelectedIdx,7,dlg.tailAsset())

  def load(self,assets):
    for headAsset,headAdornment,headNry,headRole,tailRole,tailNry,tailAdornment,tailAsset in assets:
      idx = self.GetItemCount()
      self.InsertStringItem(idx,headAsset)
      self.SetStringItem(idx,1,headAdornment)
      self.SetStringItem(idx,2,headNry)
      self.SetStringItem(idx,3,headRole)
      self.SetStringItem(idx,4,tailRole)
      self.SetStringItem(idx,5,tailNry)
      self.SetStringItem(idx,6,tailAdornment)
      self.SetStringItem(idx,7,tailAsset)

  def associations(self):
    assocs = []
    for x in range(self.GetItemCount()):
      headAsset = self.GetItemText(x)
      headAdornment = self.GetItem(x,1)
      headNry = self.GetItem(x,2)
      headRole = self.GetItem(x,3)
      tailRole = self.GetItem(x,4)
      tailNry = self.GetItem(x,5)
      tailAdornment = self.GetItem(x,6)
      tailAsset = self.GetItem(x,7)
      assocs.append((headAsset,headAdornment.GetText(),headNry.GetText(),headRole.GetText(),tailRole.GetText(),tailNry.GetText(),tailAdornment.GetText(),tailAsset.GetText()))
    return assocs

  def assets(self):
    assets = set([])
    for x in range(self.GetItemCount()):
      assets.add(self.GetItemText(x))
      assets.add(((self.GetItem(x,7))).GetText())
    return list(assets)

