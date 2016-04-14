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
import WidgetFactory
from Borg import Borg

class ResponseCostDialog(wx.Dialog):
  def __init__(self,parent):
    wx.Dialog.__init__(self,parent,armid.RESPONSECOST_ID,'Add Response Cost',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,100))
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theResponseName = ''
    self.theResponseCost = ''
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    responseList = self.dbProxy.getDimensionNames('response')
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Response',(87,30),armid.RESPONSECOST_COMBORESPONSE_ID,responseList),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Cost',(87,30),armid.RESPONSECOST_COMBOCOST_ID,['Low','Medium','High']),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildAddCancelButtonSizer(self,armid.RESPONSECOST_BUTTONADD_ID),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

    wx.EVT_BUTTON(self,armid.RESPONSECOST_BUTTONADD_ID,self.onAdd)

  def onAdd(self,evt):
    responseCtrl = self.FindWindowById(armid.RESPONSECOST_COMBORESPONSE_ID)
    costCtrl = self.FindWindowById(armid.RESPONSECOST_COMBOCOST_ID)
    self.theResponseName = responseCtrl.GetStringSelection()
    self.theResponseCost = costCtrl.GetStringSelection()

    if len(self.theResponseName) == 0:
      dlg = wx.MessageDialog(self,'No response selected','Add Response Cost',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theResponseCost) == 0):
      dlg = wx.MessageDialog(self,'No cost selected','Add Response Cost',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(armid.RESPONSECOST_BUTTONADD_ID)

  def response(self): return self.theResponseName

  def cost(self): return self.theResponseCost
