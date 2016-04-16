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
from RoleCostDialog import RoleCostDialog

class RoleCostListCtrl(wx.ListCtrl):
  def __init__(self,parent,winId,boxSize=wx.DefaultSize):
    wx.ListCtrl.__init__(self,parent,winId,size=boxSize,style=wx.LC_REPORT)
    self.InsertColumn(0,'Role')
    self.SetColumnWidth(0,150)
    self.InsertColumn(1,'Cost')
    self.SetColumnWidth(1,300)
    self.theDimMenu = wx.Menu()
    self.theDimMenu.Append(COSTLISTCTRL_MENUADD_ID,'Add')
    self.theDimMenu.Append(COSTLISTCTRL_MENUDELETE_ID,'Delete')
    self.theSelectedIdx = -1
    self.Bind(wx.EVT_RIGHT_DOWN,self.OnRightDown)
    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    wx.EVT_MENU(self.theDimMenu,COSTLISTCTRL_MENUADD_ID,self.onAddProperty)
    wx.EVT_MENU(self.theDimMenu,COSTLISTCTRL_MENUDELETE_ID,self.onDeleteProperty)

  def setEnvironment(self,environmentName):
    pass

  def OnItemSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()

  def OnItemDeselected(self,evt):
    self.theSelectedIdx = -1

  def OnRightDown(self,evt):
    self.PopupMenu(self.theDimMenu)

  def onAddProperty(self,evt):
    dlg = RoleCostDialog(self)
    if (dlg.ShowModal() == ROLECOST_BUTTONADD_ID):
      roleName = dlg.role()
      roleCost = dlg.cost()
      idx = self.GetItemCount()
      self.InsertStringItem(idx,roleName)
      self.SetStringItem(idx,1,roleCost)

  def onDeleteProperty(self,evt):
    if (self.theSelectedIdx == -1):
      errorText = 'No property selected'
      errorLabel = 'Delete Role Cost'
      dlg = wx.MessageDialog(self,errorText,errorLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
    else:
      selectedValue = self.GetItemText(self.theSelectedIdx)
      self.DeleteItem(self.theSelectedIdx)

  def load(self,roleCosts):
    for idx,roleCost in enumerate(roleCosts):
      role = roleCost[0]
      cost = roleCost[1]
      self.InsertStringItem(idx,role)
      self.SetStringItem(idx,1,cost)

  def roles(self):
    roleCosts = []
    for x in range(self.GetItemCount()):
      roleName = self.GetItemText(x)
      cost = (self.GetItem(x,1)).GetText()
      roleCosts.append( (roleName,cost) )
    return roleCosts
