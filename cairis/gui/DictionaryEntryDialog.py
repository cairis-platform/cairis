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

class DictionaryEntryDialog(wx.Dialog):
  def __init__(self,parent,name = '',definition = ''):
    wx.Dialog.__init__(self,parent,DICTIONARYENTRY_ID,'Add Dictionary Entry',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(500,300))
    self.theName = name
    self.theDefinition = definition
    mainSizer = wx.BoxSizer(wx.VERTICAL)

    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Name',(87,30),DICTIONARYENTRY_TEXTNAME_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildMLTextSizer(self,'Definition',(87,30),DICTIONARYENTRY_TEXTDEFINITION_ID),1,wx.EXPAND)

    mainSizer.Add(WidgetFactory.buildAddCancelButtonSizer(self,DICTIONARYENTRY_BUTTONCOMMIT_ID),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

    wx.EVT_BUTTON(self,DICTIONARYENTRY_BUTTONCOMMIT_ID,self.onCommit)
    self.commitLabel = 'Add'
    if (len(self.theName) > 0):
      self.commitLabel = 'Edit'
      self.SetLabel('Edit Dictionary Entry')
      nameCtrl = self.FindWindowById(DICTIONARYENTRY_TEXTNAME_ID)
      nameCtrl.SetValue(self.theName)
      defCtrl = self.FindWindowById(DICTIONARYENTRY_TEXTDEFINITION_ID)
      defCtrl.SetValue(self.theDefinition)
      buttonCtrl = self.FindWindowById(DICTIONARYENTRY_BUTTONCOMMIT_ID)
      buttonCtrl.SetLabel('Edit')
      

  def onCommit(self,evt):
    nameCtrl = self.FindWindowById(DICTIONARYENTRY_TEXTNAME_ID)
    defCtrl = self.FindWindowById(DICTIONARYENTRY_TEXTDEFINITION_ID)

    self.theName = nameCtrl.GetValue()
    self.theDefinition = defCtrl.GetValue()

    if (len(self.theName) == 0):
      dlg = wx.MessageDialog(self,'No name entry',self.commitLabel + ' Dictionary Entry',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theDefinition) == 0):
      dlg = wx.MessageDialog(self,'No definition entry',self.commitLabel + ' Dictionary Entry',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(DICTIONARYENTRY_BUTTONCOMMIT_ID)

  def name(self): return self.theName
  def definition(self): return self.theDefinition
