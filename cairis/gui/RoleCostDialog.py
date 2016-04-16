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
from cairis.core.Borg import Borg

class RoleCostDialog(wx.Dialog):
  def __init__(self,parent):
    wx.Dialog.__init__(self,parent,ROLECOST_ID,'Add Role Cost',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,140))
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theRoleName = ''
    self.theRoleCost = ''
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    roleList = self.dbProxy.getDimensionNames('role')
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Role',(87,30),ROLECOST_COMBOROLE_ID,roleList),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Cost',(87,30),ROLECOST_COMBOCOST_ID,['Low','Medium','High']),0,wx.EXPAND)
    mainSizer.Add(wx.StaticText(self,-1),1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildAddCancelButtonSizer(self,ROLECOST_BUTTONADD_ID),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

    wx.EVT_BUTTON(self,ROLECOST_BUTTONADD_ID,self.onAdd)

  def onAdd(self,evt):
    roleCtrl = self.FindWindowById(ROLECOST_COMBOROLE_ID)
    costCtrl = self.FindWindowById(ROLECOST_COMBOCOST_ID)
    self.theRoleName = roleCtrl.GetStringSelection()
    self.theRoleCost = costCtrl.GetStringSelection()

    if len(self.theRoleName) == 0:
      dlg = wx.MessageDialog(self,'No role selected','Add Role Cost',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theRoleCost) == 0):
      dlg = wx.MessageDialog(self,'No cost selected','Add Role Cost',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(ROLECOST_BUTTONADD_ID)

  def role(self): return self.theRoleName

  def cost(self): return self.theRoleCost
