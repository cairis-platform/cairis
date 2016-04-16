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

class CapabilityDialog(wx.Dialog):
  def __init__(self,parent,setCapabilities,dp):
    wx.Dialog.__init__(self,parent,CAPABILITY_ID,'Add Capability',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,150))
    self.theCapabilityName = ''
    self.theCapabilityValue = ''
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    defaultCapabilities = set(dp.getDimensionNames('capability'))
    capabilityList = list(defaultCapabilities.difference(setCapabilities))
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Capability',(87,30),CAPABILITY_COMBOCAPABILITY_ID,capabilityList),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Value',(87,30),CAPABILITY_COMBOVALUE_ID,['Low','Medium','High']),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildAddCancelButtonSizer(self,CAPABILITY_BUTTONADD_ID),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

    wx.EVT_BUTTON(self,CAPABILITY_BUTTONADD_ID,self.onAdd)

  def onAdd(self,evt):
    capCtrl = self.FindWindowById(CAPABILITY_COMBOCAPABILITY_ID)
    valueCtrl = self.FindWindowById(CAPABILITY_COMBOVALUE_ID)
    self.theCapabilityName = capCtrl.GetStringSelection()
    self.theCapabilityValue = valueCtrl.GetStringSelection()

    if len(self.theCapabilityName) == 0:
      dlg = wx.MessageDialog(self,'No capability selected','Add Capability',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theCapabilityValue) == 0):
      dlg = wx.MessageDialog(self,'No value selected','Add Capability',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(CAPABILITY_BUTTONADD_ID)

  def capability(self): return self.theCapabilityName

  def value(self): return self.theCapabilityValue
