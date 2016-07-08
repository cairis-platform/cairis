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
from InterfaceListPanel import InterfaceListPanel

class InterfaceListDialog(wx.Dialog):
  def __init__(self,parent,ifName = '',ifType = '',arName = '',pName = ''):
    wx.Dialog.__init__(self,parent,INTERFACELISTDIALOG_ID,'Add Interface',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(300,200))
    self.theInterfaceName = ifName
    self.theInterfaceType = ifType
    self.theAccessRight = arName
    self.thePrivilege = pName
    self.buildControls()
    self.load(ifName,ifType,arName,pName)

  def buildControls(self):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = InterfaceListPanel(self)
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,wx.ID_OK,self.onCommit)

  def load(self,ifName,ifType,arName,pName):
    self.panel.load(ifName,ifType,arName,pName)


  def onCommit(self,evt):
    nameCtrl = self.FindWindowById(INTERFACELISTDIALOG_COMBONAME_ID)
    typeCtrl = self.FindWindowById(INTERFACELISTDIALOG_COMBOTYPE_ID)
    arCtrl = self.FindWindowById(INTERFACELISTDIALOG_COMBOACCESSRIGHT_ID)
    pCtrl = self.FindWindowById(INTERFACELISTDIALOG_COMBOPRIVILEGE_ID)

    self.theInterfaceName = nameCtrl.GetValue()
    self.theInterfaceType = typeCtrl.GetValue()
    self.theAccessRight = arCtrl.GetValue()
    self.thePrivilege = pCtrl.GetValue()
    self.EndModal(wx.ID_OK)

  def interface(self): return self.theInterfaceName
  def interfaceType(self): return self.theInterfaceType
  def accessRight(self): return self.theAccessRight
  def privilege(self): return self.thePrivilege
