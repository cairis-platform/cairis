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
from ConcernAssociationDialog import ConcernAssociationDialog

class ConcernAssociationListCtrl(wx.ListCtrl):
  def __init__(self,parent,winId,dp,boxSize=wx.DefaultSize):
    wx.ListCtrl.__init__(self,parent,winId,size=boxSize,style=wx.LC_REPORT)
    self.dbProxy = dp
    self.theCurrentEnvironment = ''
    self.InsertColumn(0,'Source')
    self.SetColumnWidth(0,100)
    self.InsertColumn(1,'n')
    self.SetColumnWidth(1,50)
    self.InsertColumn(2,'Link Verb')
    self.SetColumnWidth(2,75)
    self.InsertColumn(3,'n')
    self.SetColumnWidth(3,50)
    self.InsertColumn(4,'Target')
    self.SetColumnWidth(4,100)
    self.theSelectedIdx = -1
    self.theDimMenu = wx.Menu()
    self.theDimMenu.Append(armid.CONCA_MENUADD_ID,'Add')
    self.theDimMenu.Append(armid.CONCA_MENUDELETE_ID,'Delete')
    self.Bind(wx.EVT_RIGHT_DOWN,self.OnRightDown)
    wx.EVT_MENU(self.theDimMenu,armid.CONCA_MENUADD_ID,self.onAddAssociation)
    wx.EVT_MENU(self.theDimMenu,armid.CONCA_MENUDELETE_ID,self.onDeleteAssociation)

    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.onAssociationActivated)

  def setEnvironment(self,environmentName):
    self.theCurrentEnvironment = environmentName

  def OnRightDown(self,evt):
    self.PopupMenu(self.theDimMenu)

  def onAddAssociation(self,evt):
    dlg = ConcernAssociationDialog(self,self.dbProxy,self.theCurrentEnvironment)
    if (dlg.ShowModal() == armid.CONCERNASSOCIATION_BUTTONCOMMIT_ID):
      self.theSelectedIdx = self.GetItemCount()
      self.InsertStringItem(self.theSelectedIdx,dlg.source())
      self.SetStringItem(self.theSelectedIdx,1,dlg.sourceMultiplicity())
      self.SetStringItem(self.theSelectedIdx,2,dlg.link())
      self.SetStringItem(self.theSelectedIdx,3,dlg.targetMultiplicity())
      self.SetStringItem(self.theSelectedIdx,4,dlg.target())

  def onDeleteAssociation(self,evt):
    if (self.theSelectedIdx == -1):
      errorText = 'No association selected'
      errorLabel = 'Delete concern'
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

  def onAssociationActivated(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    source = self.GetItemText(self.theSelectedIdx)
    sourceMultiplicity = self.GetItem(self.theSelectedIdx,1)
    link = self.GetItem(self.theSelectedIdx,2)
    targetMultiplicity = self.GetItem(self.theSelectedIdx,3)
    target = self.GetItem(self.theSelectedIdx,4)
     
    dlg = ConcernAssociationDialog(self,self.dbProxy,self.theCurrentEnvironment,source,sourceMultiplicity.GetText(),link.GetText(),target.GetText(),targetMultiplicity.GetText())
    if (dlg.ShowModal() == armid.CONCERNASSOCIATION_BUTTONCOMMIT_ID):
      self.SetStringItem(self.theSelectedIdx,0,dlg.source())
      self.SetStringItem(self.theSelectedIdx,1,dlg.sourceMultiplicity())
      self.SetStringItem(self.theSelectedIdx,2,dlg.link())
      self.SetStringItem(self.theSelectedIdx,3,dlg.targetMultiplicity())
      self.SetStringItem(self.theSelectedIdx,4,dlg.target())

  def load(self,assocs):
    for source,sourceMultiplicity,link,target,targetMultiplicity in assocs:
      idx = self.GetItemCount()
      self.InsertStringItem(idx,source)
      self.SetStringItem(idx,1,sourceMultiplicity)
      self.SetStringItem(idx,2,link)
      self.SetStringItem(idx,3,targetMultiplicity)
      self.SetStringItem(idx,4,target)

  def dimensions(self):
    assocs = []
    for x in range(self.GetItemCount()):
      source = self.GetItemText(x)
      sourceMultiplicity = self.GetItem(x,1)
      link = self.GetItem(x,2)
      targetMultiplicity = self.GetItem(x,3)
      target = self.GetItem(x,4)
      assocs.append((source,sourceMultiplicity.GetText(),link.GetText(),target.GetText(),targetMultiplicity.GetText()))
    return assocs
