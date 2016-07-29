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

__author__ = 'Shamal Faily'

class DependentsDialog(wx.Dialog):
  def __init__(self,parent,dependents,dimName):
    wx.Dialog.__init__(self,parent,DEPENDENTS_ID,'Delete ' + dimName,style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,300))
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    labelTxt = 'The following artifacts are dependent on this ' + dimName + ', and removing it also removes them.\n  Do you want to continue?'
    mainSizer.Add(wx.StaticText(self,-1,labelTxt),0,wx.EXPAND)
    dependentsListCtrl = wx.ListCtrl(self,-1,style=wx.LC_REPORT)
    dependentsListCtrl.InsertColumn(0,"Artifact")
    dependentsListCtrl.InsertColumn(1,"Name")
    
    for idx,artifact in enumerate(dependents):
      dimName = artifact[0]
      objtName = artifact[2]
      dependentsListCtrl.InsertStringItem(idx,dimName)
      dependentsListCtrl.SetStringItem(idx,1,objtName)
    dependentsListCtrl.SetColumnWidth(0,75)
    dependentsListCtrl.SetColumnWidth(1,200)
    mainSizer.Add(dependentsListCtrl,1,wx.EXPAND)
    buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(buttonSizer,0,wx.CENTER)
    yesButton = wx.Button(self,DEPENDENTS_BUTTONCONFIRM_ID,"Yes")
    buttonSizer.Add(yesButton)
    cancelButton = wx.Button(self,wx.ID_CANCEL,"Cancel")
    buttonSizer.Add(cancelButton)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,DEPENDENTS_BUTTONCONFIRM_ID,self.onConfirm)

  def onConfirm(self,evt):
    self.EndModal(DEPENDENTS_BUTTONCONFIRM_ID)
