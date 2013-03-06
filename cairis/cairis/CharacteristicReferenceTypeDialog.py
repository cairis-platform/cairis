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

class CharacteristicReferenceTypeDialog(wx.Dialog):
  def __init__(self,parent,currentValue):
    wx.Dialog.__init__(self,parent,armid.CHARACTERISTICREFERENCETYPE_ID,'Edit Characteristic Reference Type',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(300,150))

    self.theValue = currentValue
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Characteristic Reference Type',(87,30),armid.CHARACTERISTICREFERENCETYPE_COMBOVALUE_ID,['grounds','warrant','rebuttal']),0,wx.EXPAND)
    mainSizer.Add(wx.StaticText(self,-1,''),1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildCommitButtonSizer(self,armid.CHARACTERISTICREFERENCETYPE_BUTTONCOMMIT_ID,False),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.CHARACTERISTICREFERENCETYPE_BUTTONCOMMIT_ID,self.onCommit)
    self.valueCtrl = self.FindWindowById(armid.CHARACTERISTICREFERENCETYPE_COMBOVALUE_ID)
    self.valueCtrl.SetValue(currentValue)

  def onCommit(self,evt):
    self.theValue = self.valueCtrl.GetValue()
    self.EndModal(armid.CHARACTERISTICREFERENCETYPE_BUTTONCOMMIT_ID)

  def value(self): return self.theValue
