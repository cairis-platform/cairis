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
from BasePanel import BasePanel
from Borg import Borg

class InterfaceListPanel(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,armid.INTERFACELISTDIALOG_ID)
    b = Borg()
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    ifList = b.dbProxy.getDimensionNames('interface')
    mainSizer.Add(self.buildComboSizerList('Name',(87,30),armid.INTERFACELISTDIALOG_COMBONAME_ID,ifList),0,wx.EXPAND)
    mainSizer.Add(self.buildComboSizerList('Type',(87,30),armid.INTERFACELISTDIALOG_COMBOTYPE_ID,['provided','required']),0,wx.EXPAND)
    mainSizer.Add(wx.StaticText(self,-1,''),1,wx.EXPAND)
    mainSizer.Add(self.buildCommitButtonSizer(wx.ID_OK,True),0,wx.CENTER)
    self.SetSizer(mainSizer)

  def load(self,ifName,ifType):
    nameCtrl = self.FindWindowById(armid.INTERFACELISTDIALOG_COMBONAME_ID)
    nameCtrl.SetValue(ifName)
    typeCtrl = self.FindWindowById(armid.INTERFACELISTDIALOG_COMBOTYPE_ID)
    typeCtrl.SetValue(ifType)
