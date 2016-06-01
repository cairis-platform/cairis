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
from BasePanel import BasePanel
from cairis.core.Borg import Borg

class InterfaceListPanel(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,INTERFACELISTDIALOG_ID)
    b = Borg()
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    ifList = b.dbProxy.getDimensionNames('interface')
    mainSizer.Add(self.buildEditableComboSizerList('Name',(87,30),INTERFACELISTDIALOG_COMBONAME_ID,ifList),0,wx.EXPAND)
    mainSizer.Add(self.buildComboSizerList('Type',(87,30),INTERFACELISTDIALOG_COMBOTYPE_ID,['provided','required']),0,wx.EXPAND)
    metricsSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(metricsSizer,0,wx.EXPAND)
    arList = b.dbProxy.getDimensionNames('access_right')
    pList = b.dbProxy.getDimensionNames('privilege')
    metricsSizer.Add(self.buildComboSizerList('Access Right',(87,30),INTERFACELISTDIALOG_COMBOACCESSRIGHT_ID,arList),1,wx.EXPAND)
    metricsSizer.Add(self.buildComboSizerList('Privilege',(87,30),INTERFACELISTDIALOG_COMBOPRIVILEGE_ID,pList),1,wx.EXPAND)

    mainSizer.Add(wx.StaticText(self,-1,''),1,wx.EXPAND)
    mainSizer.Add(self.buildCommitButtonSizer(wx.ID_OK,True),0,wx.CENTER)
    self.SetSizer(mainSizer)

  def load(self,ifName,ifType,arName,pName):
    nameCtrl = self.FindWindowById(INTERFACELISTDIALOG_COMBONAME_ID)
    nameCtrl.SetValue(ifName)
    typeCtrl = self.FindWindowById(INTERFACELISTDIALOG_COMBOTYPE_ID)
    typeCtrl.SetValue(ifType)
    arCtrl = self.FindWindowById(INTERFACELISTDIALOG_COMBOACCESSRIGHT_ID)
    arCtrl.SetValue(arName)
    pCtrl = self.FindWindowById(INTERFACELISTDIALOG_COMBOPRIVILEGE_ID)
    pCtrl.SetValue(pName)
