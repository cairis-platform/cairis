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

__author__ = 'Shamal Faily'

class DirectoryEntryDialog(wx.Dialog):
  def __init__(self,parent,dLabel,dName,dType,dDesc):
    wx.Dialog.__init__(self,parent,DIRECTORYENTRY_ID,'Directory Entry',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(500,300))
    mainSizer = wx.BoxSizer(wx.VERTICAL)

    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Label',(87,30),DIRECTORYENTRY_TEXTLABEL_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Name',(87,30),DIRECTORYENTRY_TEXTNAME_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Type',(87,30),DIRECTORYENTRY_TEXTTYPE_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildMLTextSizer(self,'Description',(87,30),DIRECTORYENTRY_TEXTDESCRIPTION_ID),1,wx.EXPAND)

    buttonSizer = wx.BoxSizer(wx.ALIGN_CENTER)
    okButton = wx.Button(self,wx.ID_OK,'Ok')
    buttonSizer.Add(okButton)
    mainSizer.Add(buttonSizer,0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

    labelCtrl = self.FindWindowById(DIRECTORYENTRY_TEXTLABEL_ID)
    labelCtrl.SetValue(dLabel)
    labelCtrl.Disable()
    nameCtrl = self.FindWindowById(DIRECTORYENTRY_TEXTNAME_ID)
    nameCtrl.SetValue(dName)
    nameCtrl.Disable()
    typeCtrl = self.FindWindowById(DIRECTORYENTRY_TEXTTYPE_ID)
    typeCtrl.SetValue(dType)
    typeCtrl.Disable()
    descCtrl = self.FindWindowById(DIRECTORYENTRY_TEXTDESCRIPTION_ID)
    descCtrl.SetValue(dDesc)
    descCtrl.Disable()

  def onOk(self,evt):
    self.EndModal(wx.ID_OK)
