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
from ChannelDialog import ChannelDialog

__author__ = 'Shamal Faily'

class ChannelListCtrl(wx.ListCtrl):
  def __init__(self,parent,winId,boxSize=wx.DefaultSize):
    wx.ListCtrl.__init__(self,parent,winId,size=boxSize,style=wx.LC_REPORT)
    self.InsertColumn(0,'Channel')
    self.SetColumnWidth(0,150)
    self.InsertColumn(1,'Data Type')
    self.SetColumnWidth(1,300)
    self.theDimMenu = wx.Menu()
    self.theDimMenu.Append(CHANNELLISTCTRL_MENUADD_ID,'Add')
    self.theDimMenu.Append(CHANNELLISTCTRL_MENUDELETE_ID,'Delete')
    self.theSelectedValue = ''
    self.theSelectedIdx = -1
    self.Bind(wx.EVT_RIGHT_DOWN,self.OnRightDown)
    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    wx.EVT_MENU(self.theDimMenu,CHANNELLISTCTRL_MENUADD_ID,self.onAddChannel)
    wx.EVT_MENU(self.theDimMenu,CHANNELLISTCTRL_MENUDELETE_ID,self.onDeleteChannel)

  def OnItemSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()

  def OnItemDeselected(self,evt):
    self.theSelectedIdx = -1

  def OnRightDown(self,evt):
    self.PopupMenu(self.theDimMenu)

  def onAddChannel(self,evt):
    dlg = ChannelDialog(self)
    if (dlg.ShowModal() == CHANNEL_BUTTONADD_ID):
      channelName = dlg.channel()
      dType = dlg.dataType()
      idx = self.GetItemCount()
      self.InsertStringItem(idx,channelName)
      self.SetStringItem(idx,1,dType)
      self.theSelectedValue = channelName

  def onDeleteChannel(self,evt):
    if (self.theSelectedIdx == -1):
      errorText = 'No channel selected'
      errorLabel = 'Delete Channel'
      dlg = wx.MessageDialog(self,errorText,errorLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
    else:
      selectedValue = self.GetItemText(self.theSelectedIdx)
      self.DeleteItem(self.theSelectedIdx)

  def load(self,channels):
    for name,dType in channels:
      idx = self.GetItemCount()
      self.InsertStringItem(idx,name)
      self.SetStringItem(idx,1,dType)

  def channels(self):
    channels = []
    for x in range(self.GetItemCount()):
      channelName = self.GetItemText(x)
      dType = self.GetItem(x,1)
      channels.append((channelName,dType.GetText()))
    return channels
