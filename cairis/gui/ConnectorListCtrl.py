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
from ConnectorDialog import ConnectorDialog
from cairis.core.ConnectorParameters import ConnectorParameters

class ConnectorListCtrl(wx.ListCtrl):
  def __init__(self,parent,winId = COMPONENTVIEW_LISTCONNECTORS_ID):
    wx.ListCtrl.__init__(self,parent,winId,size=wx.DefaultSize,style=wx.LC_REPORT)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theViewName = ''
    self.InsertColumn(0,'Connector')
    self.SetColumnWidth(0,100)
    self.InsertColumn(1,'From')
    self.SetColumnWidth(1,100)
    self.InsertColumn(2,'Role')
    self.SetColumnWidth(2,100)
    self.InsertColumn(3,'Interface')
    self.SetColumnWidth(3,100)
    self.InsertColumn(4,'To')
    self.SetColumnWidth(4,100)
    self.InsertColumn(5,'Interface')
    self.SetColumnWidth(5,100)
    self.InsertColumn(6,'Role')
    self.SetColumnWidth(6,100)
    self.InsertColumn(7,'Asset')
    self.SetColumnWidth(7,100)
    self.InsertColumn(8,'Protocol')
    self.SetColumnWidth(8,100)
    self.InsertColumn(9,'Access Right')
    self.SetColumnWidth(9,100)
    self.theSelectedIdx = -1
    self.theDimMenu = wx.Menu()
    self.theDimMenu.Append(AA_MENUADD_ID,'Add')
    self.theDimMenu.Append(AA_MENUDELETE_ID,'Delete')
    self.Bind(wx.EVT_RIGHT_DOWN,self.OnRightDown)
    wx.EVT_MENU(self.theDimMenu,AA_MENUADD_ID,self.onAddConnector)
    wx.EVT_MENU(self.theDimMenu,AA_MENUDELETE_ID,self.onDeleteConnector)

    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.onConnectorActivated)

  def setView(self,cvName): self.theViewName = cvName

  def OnRightDown(self,evt):
    self.PopupMenu(self.theDimMenu)

  def onAddConnector(self,evt):
    dlg = ConnectorDialog(self)
    if (dlg.ShowModal() == CONNECTOR_BUTTONCOMMIT_ID):
      self.theSelectedIdx = self.GetItemCount()
      self.InsertStringItem(self.theSelectedIdx,dlg.name())
      self.SetStringItem(self.theSelectedIdx,1,dlg.fromComponent())
      self.SetStringItem(self.theSelectedIdx,2,dlg.fromRole())
      self.SetStringItem(self.theSelectedIdx,3,dlg.fromInterface())
      self.SetStringItem(self.theSelectedIdx,4,dlg.toComponent())
      self.SetStringItem(self.theSelectedIdx,5,dlg.toInterface())
      self.SetStringItem(self.theSelectedIdx,6,dlg.toRole())
      self.SetStringItem(self.theSelectedIdx,7,dlg.asset())
      self.SetStringItem(self.theSelectedIdx,8,dlg.protocol())
      self.SetStringItem(self.theSelectedIdx,9,dlg.accessRight())

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
    fromRole = self.GetItem(self.theSelectedIdx,2)
    fromInterface = self.GetItem(self.theSelectedIdx,3)
    toComponent = self.GetItem(self.theSelectedIdx,4)
    toInterface = self.GetItem(self.theSelectedIdx,5)
    toRole = self.GetItem(self.theSelectedIdx,6)
    assetName = self.GetItem(self.theSelectedIdx,7)
    pName = self.GetItem(self.theSelectedIdx,8)
    arName = self.GetItem(self.theSelectedIdx,9)
     
    dlg = ConnectorDialog(self,conName,fromComponent.GetText(),fromRole.GetText(),fromInterface.GetText(),toComponent.GetText(),toInterface.GetText(),toRole.GetText(),assetName.GetText(),pName.GetText(),arName.GetText())
    if (dlg.ShowModal() == CONNECTOR_BUTTONCOMMIT_ID):
      self.SetStringItem(self.theSelectedIdx,0,dlg.name())
      self.SetStringItem(self.theSelectedIdx,1,dlg.fromComponent())
      self.SetStringItem(self.theSelectedIdx,2,dlg.fromRole())
      self.SetStringItem(self.theSelectedIdx,3,dlg.fromInterface())
      self.SetStringItem(self.theSelectedIdx,4,dlg.toComponent())
      self.SetStringItem(self.theSelectedIdx,5,dlg.toInterface())
      self.SetStringItem(self.theSelectedIdx,6,dlg.toRole())
      self.SetStringItem(self.theSelectedIdx,7,dlg.asset())
      self.SetStringItem(self.theSelectedIdx,8,dlg.protocol())
      self.SetStringItem(self.theSelectedIdx,9,dlg.accessRight())

  def load(self,cons):
    for conName,fromComponent,fromRole,fromInterface,toComponent,toInterface,toRole,assetName,pName,arName in cons:
      idx = self.GetItemCount()
      self.InsertStringItem(idx,conName)
      self.SetStringItem(idx,1,fromComponent)
      self.SetStringItem(idx,2,fromRole)
      self.SetStringItem(idx,3,fromInterface)
      self.SetStringItem(idx,4,toComponent)
      self.SetStringItem(idx,5,toInterface)
      self.SetStringItem(idx,6,toRole)
      self.SetStringItem(idx,7,assetName)
      self.SetStringItem(idx,8,pName)
      self.SetStringItem(idx,9,arName)

  def dimensions(self):
    cons = []
    for x in range(self.GetItemCount()):
      conName = self.GetItemText(x)
      fromComponent = self.GetItem(x,1)
      fromRole = self.GetItem(x,2)
      fromInterface = self.GetItem(x,3)
      toComponent = self.GetItem(x,4)
      toInterface = self.GetItem(x,5)
      toRole = self.GetItem(x,6)
      assetName = self.GetItem(x,7)
      pName = self.GetItem(x,8)
      arName = self.GetItem(x,9)
      p = ConnectorParameters(conName,self.theViewName,fromComponent.GetText(),fromRole.GetText(),fromInterface.GetText(),toComponent.GetText(),toInterface.GetText(),toRole.GetText(),assetName.GetText(),pName.GetText(),arName.GetText())
      cons.append(p)
    return cons
