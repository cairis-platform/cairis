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
from CapabilityDialog import CapabilityDialog

class CapabilitiesListCtrl(wx.ListCtrl):
  def __init__(self,parent,winId,dp,boxSize=wx.DefaultSize):
    wx.ListCtrl.__init__(self,parent,winId,size=boxSize,style=wx.LC_REPORT)
    self.dbProxy = dp
    self.theCurrentEnvironment = ''
    self.InsertColumn(0,'Capability')
    self.SetColumnWidth(0,150)
    self.InsertColumn(1,'Value')
    self.SetColumnWidth(1,300)
    self.theDimMenu = wx.Menu()
    self.theDimMenu.Append(CAPABILITIESLISTCTRL_MENUADD_ID,'Add')
    self.theDimMenu.Append(CAPABILITIESLISTCTRL_MENUDELETE_ID,'Delete')
    self.theSelectedValue = ''
    self.theSelectedIdx = -1
    self.setCapabilities = {}
    self.Bind(wx.EVT_RIGHT_DOWN,self.OnRightDown)
    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    wx.EVT_MENU(self.theDimMenu,CAPABILITIESLISTCTRL_MENUADD_ID,self.onAddCapability)
    wx.EVT_MENU(self.theDimMenu,CAPABILITIESLISTCTRL_MENUDELETE_ID,self.onDeleteCapability)

  def setEnvironment(self,environmentName):
    self.theCurrentEnvironment = environmentName
    if ((self.theCurrentEnvironment in self.setCapabilities) == False):
      self.setCapabilities[self.theCurrentEnvironment] = set([])

  def OnItemSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()

  def OnItemDeselected(self,evt):
    self.theSelectedIdx = -1

  def OnRightDown(self,evt):
    self.PopupMenu(self.theDimMenu)

  def onAddCapability(self,evt):
    dlg = CapabilityDialog(self,self.setCapabilities[self.theCurrentEnvironment],self.dbProxy)
    if (dlg.ShowModal() == CAPABILITY_BUTTONADD_ID):
      capName = dlg.capability()
      capValue = dlg.value()
      idx = self.GetItemCount()
      self.InsertStringItem(idx,capName)
      self.SetStringItem(idx,1,capValue)
      self.theSelectedValue = capName
      (self.setCapabilities[self.theCurrentEnvironment]).add(capName)

  def onDeleteCapability(self,evt):
    if (self.theSelectedIdx == -1):
      errorText = 'No capability selected'
      errorLabel = 'Delete Capability'
      dlg = wx.MessageDialog(self,errorText,errorLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
    else:
      selectedValue = self.GetItemText(self.theSelectedIdx)
      self.DeleteItem(self.theSelectedIdx)
      (self.setCapabilities[self.theCurrentEnvironment]).remove(selectedValue)

  def load(self,capabilities):
    for name,value in capabilities:
      idx = self.GetItemCount()
      self.InsertStringItem(idx,name)
      self.SetStringItem(idx,1,value)
      (self.setCapabilities[self.theCurrentEnvironment]).add(name)

  def capabilities(self):
    capabilities = []
    for x in range(self.GetItemCount()):
      capName = self.GetItemText(x)
      capValue = self.GetItem(x,1)
      capabilities.append((capName,capValue.GetText()))
    return capabilities
