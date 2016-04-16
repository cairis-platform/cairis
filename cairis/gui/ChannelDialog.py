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
import WidgetFactory

class ChannelDialog(wx.Dialog):
  def __init__(self,parent):
    wx.Dialog.__init__(self,parent,CHANNEL_ID,'Add Channel',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,150))
    self.theChannelName = ''
    self.theDataType = ''
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Channel',(87,30),CHANNEL_TEXTCHANNEL_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Data Type',(87,30),CHANNEL_TEXTDATATYPE_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildAddCancelButtonSizer(self,CHANNEL_BUTTONADD_ID),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

    wx.EVT_BUTTON(self,CHANNEL_BUTTONADD_ID,self.onAdd)

  def onAdd(self,evt):
    cCtrl = self.FindWindowById(CHANNEL_TEXTCHANNEL_ID)
    dtCtrl = self.FindWindowById(CHANNEL_TEXTDATATYPE_ID)
    self.theChannelName = cCtrl.GetValue()
    self.theDataType = dtCtrl.GetValue()

    if len(self.theChannelName) == 0:
      dlg = wx.MessageDialog(self,'No channel entered','Add Channel',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theDataType) == 0):
      dlg = wx.MessageDialog(self,'No data type','Add Channel',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(CHANNEL_BUTTONADD_ID)

  def channel(self): return self.theChannelName
  def dataType(self): return self.theDataType
