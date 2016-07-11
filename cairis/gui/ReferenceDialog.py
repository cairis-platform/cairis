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
from ReferencePanel import ReferencePanel
import DialogClassParameters

class ReferenceDialog(wx.Dialog):
  def __init__(self,parent,crTypeName,refName = '',desc = '',dimName = ''):
    wx.Dialog.__init__(self,parent,CHARACTERISTICREFERENCE_ID,'Add Characteristic Reference',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,300))
    self.theCharacteristicReferenceType = crTypeName
    self.theReferenceName = refName
    self.theDescription = desc
    self.theDimensionName = dimName
    self.commitVerb = 'Add'

    if refName != '':
      self.commitVerb = 'Edit'
      self.SetTitle('Edit Characteristic Reference')

    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = ReferencePanel(self,self.theReferenceName,self.theDescription, self.theDimensionName)


    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,CHARACTERISTICREFERENCE_BUTTONCOMMIT_ID,self.onCommit)

  def onCommit(self,evt):
    commitLabel = self.commitVerb + ' Characteristic Reference'

    refCtrl = self.FindWindowById(CHARACTERISTICREFERENCE_COMBOREFERENCE_ID)
    descCtrl = self.FindWindowById(CHARACTERISTICREFERENCE_TEXTDESCRIPTION_ID)
    dimCtrl = self.FindWindowById(CHARACTERISTICREFERENCE_COMBODIMENSION_ID)

    self.theReferenceName = refCtrl.GetValue()
    self.theDescription = descCtrl.GetValue()
    self.theDimensionName = dimCtrl.GetValue()


    if len(self.theReferenceName) == 0:
      dlg = wx.MessageDialog(self,'Reference name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theDimensionName) == 0:
      dlg = wx.MessageDialog(self,'Dimension name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theDescription) == 0:
      dlg = wx.MessageDialog(self,'Description cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(CHARACTERISTICREFERENCE_BUTTONCOMMIT_ID)

  def reference(self):
    return self.theReferenceName

  def dimension(self):
    return self.theDimensionName

  def description(self):
    return self.theDescription
