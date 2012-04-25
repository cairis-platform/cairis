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
from ConnectorDialog import ConnectorDialog
from ConnectorParameters import ConnectorParameters

class ConnectorListCtrl(wx.ListCtrl):
  def __init__(self,parent,winId = armid.COMPONENTVIEW_LISTCONNECTORS_ID):
    wx.ListCtrl.__init__(self,parent,winId,size=wx.DefaultSize,style=wx.LC_REPORT)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theViewName = ''
    self.InsertColumn(0,'Connector')
    self.SetColumnWidth(0,100)
    self.InsertColumn(1,'From')
    self.SetColumnWidth(1,100)
    self.InsertColumn(2,'Interface')
    self.SetColumnWidth(2,100)
    self.InsertColumn(3,'To')
    self.SetColumnWidth(3,100)
    self.InsertColumn(4,'Interface')
    self.SetColumnWidth(4,100)
    self.InsertColumn(5,'Asset')
    self.SetColumnWidth(5,100)
    self.InsertColumn(6,'Protocol')
    self.SetColumnWidth(6,100)
    self.InsertColumn(7,'Access Right')
    self.SetColumnWidth(7,100)
    self.theSelectedIdx = -1
    self.theDimMenu = wx.Menu()
    self.theDimMenu.Append(armid.AA_MENUADD_ID,'Add')
    self.theDimMenu.Append(armid.AA_MENUDELETE_ID,'Delete')
    self.Bind(wx.EVT_RIGHT_DOWN,self.OnRightDown)
    wx.EVT_MENU(self.theDimMenu,armid.AA_MENUADD_ID,self.onAddConnector)
    wx.EVT_MENU(self.theDimMenu,armid.AA_MENUDELETE_ID,self.onDeleteConnector)

    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.onConnectorActivated)

  def setView(self,cvName): self.theViewName = cvName

  def OnRightDown(self,evt):
    self.PopupMenu(self.theDimMenu)

  def onAddConnector(self,evt):
    dlg = ConnectorDialog(self)
    if (dlg.ShowModal() == armid.CONNECTOR_BUTTONCOMMIT_ID):
      self.theSelectedIdx = self.GetItemCount()
      self.InsertStringItem(self.theSelectedIdx,dlg.name())
      self.SetStringItem(self.theSelectedIdx,1,dlg.fromComponent())
      self.SetStringItem(self.theSelectedIdx,2,dlg.fromInterface())
      self.SetStringItem(self.theSelectedIdx,3,dlg.toComponent())
      self.SetStringItem(self.theSelectedIdx,4,dlg.toInterface())
      self.SetStringItem(self.theSelectedIdx,5,dlg.asset())
      self.SetStringItem(self.theSelectedIdx,6,dlg.protocol())
      self.SetStringItem(self.theSelectedIdx,7,dlg.accessRight())

  def onDeleteConnector(self,evt):
    if (self.theSelectedIdx == -1):
      errorText = 'No connector selected'
      errorLabel = 'Delete connector'
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

  def onConnectorActivated(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    conName = self.GetItemText(self.theSelectedIdx)
    fromComponent = self.GetItem(self.theSelectedIdx,1)
    fromInterface = self.GetItem(self.theSelectedIdx,2)
    toComponent = self.GetItem(self.theSelectedIdx,3)
    toInterface = self.GetItem(self.theSelectedIdx,4)
    assetName = self.GetItem(self.theSelectedIdx,5)
    pName = self.GetItem(self.theSelectedIdx,6)
    arName = self.GetItem(self.theSelectedIdx,7)
     
    dlg = ConnectorDialog(self,conName,fromComponent.GetText(),fromInterface.GetText(),toComponent.GetText(),toInterface.GetText(),assetName.GetText(),pName.GetText(),arName.GetText())
    if (dlg.ShowModal() == armid.CONNECTOR_BUTTONCOMMIT_ID):
      self.SetStringItem(self.theSelectedIdx,0,dlg.name())
      self.SetStringItem(self.theSelectedIdx,1,dlg.fromComponent())
      self.SetStringItem(self.theSelectedIdx,2,dlg.fromInterface())
      self.SetStringItem(self.theSelectedIdx,3,dlg.toComponent())
      self.SetStringItem(self.theSelectedIdx,4,dlg.toInterface())
      self.SetStringItem(self.theSelectedIdx,5,dlg.asset())
      self.SetStringItem(self.theSelectedIdx,6,dlg.protocol())
      self.SetStringItem(self.theSelectedIdx,7,dlg.accessRight())

  def load(self,cons):
    for conName,fromComponent,fromInterface,toComponent,toInterface,assetName,pName,arName in cons:
      idx = self.GetItemCount()
      self.InsertStringItem(idx,conName)
      self.SetStringItem(idx,1,fromComponent)
      self.SetStringItem(idx,2,fromInterface)
      self.SetStringItem(idx,3,toComponent)
      self.SetStringItem(idx,4,toInterface)
      self.SetStringItem(idx,5,assetName)
      self.SetStringItem(idx,6,pName)
      self.SetStringItem(idx,7,arName)

  def dimensions(self):
    cons = []
    for x in range(self.GetItemCount()):
      conName = self.GetItemText(x)
      fromComponent = self.GetItem(x,1)
      fromInterface = self.GetItem(x,2)
      toComponent = self.GetItem(x,3)
      toInterface = self.GetItem(x,4)
      assetName = self.GetItem(x,5)
      pName = self.GetItem(x,6)
      arName = self.GetItem(x,7)
      p = ConnectorParameters(conName,self.theViewName,fromComponent.GetText(),fromInterface.GetText(),toComponent.GetText(),toInterface.GetText(),assetName.GetText(),pName.GetText(),arName.GetText())
      cons.append(p)
    return cons
