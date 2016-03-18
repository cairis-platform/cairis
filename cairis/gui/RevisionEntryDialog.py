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

class RevisionEntryDialog(wx.Dialog):
  def __init__(self,parent):
    wx.Dialog.__init__(self,parent,armid.REVISIONENTRY_ID,'Add Revision',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(300,300))
    self.theRemarks = ''
    mainSizer = wx.BoxSizer(wx.VERTICAL)

    mainSizer.Add(WidgetFactory.buildMLTextSizer(self,'Remarks',(87,30),armid.REVISIONENTRY_TEXTREMARKS_ID),1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildAddCancelButtonSizer(self,armid.REVISIONENTRY_BUTTONCOMMIT_ID),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

    wx.EVT_BUTTON(self,armid.REVISIONENTRY_BUTTONCOMMIT_ID,self.onCommit)
    self.commitLabel = 'Add'

  def onCommit(self,evt):
    remarksCtrl = self.FindWindowById(armid.REVISIONENTRY_TEXTREMARKS_ID)
    self.theRemarks = remarksCtrl.GetValue()
    if (len(self.theRemarks) == 0):
      dlg = wx.MessageDialog(self,'No revision remarks','Add revision',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(armid.REVISIONENTRY_BUTTONCOMMIT_ID)

  def remarks(self): return self.theRemarks
