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
from InternalDocumentPanel import InternalDocumentPanel
from cairis.core.InternalDocumentParameters import InternalDocumentParameters
import DialogClassParameters

__author__ = 'Shamal Faily'

class InternalDocumentDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,parameters.id(),parameters.label(),style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,300))
    self.theName = ''
    self.theDescription = ''
    self.theContent = ''
    self.theCodes = {}
    self.theMemos = {}
    self.theId = -1
    self.panel = 0
    self.buildControls(parameters)
    self.commitVerb = 'Add'
    
  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = InternalDocumentPanel(self)
    self.panel.buildControls(parameters.createFlag())
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,INTERNALDOCUMENT_BUTTONCOMMIT_ID,self.onCommit)

  def load(self,objt):
    self.theId = objt.id()
    self.panel.loadControls(objt)
    self.commitVerb = 'Edit'

  def onCommit(self,evt):
    commitLabel = self.commitVerb + ' internal document'
    nameCtrl = self.FindWindowById(INTERNALDOCUMENT_TEXTNAME_ID)
    descCtrl = self.FindWindowById(INTERNALDOCUMENT_TEXTDESCRIPTION_ID)
    contCtrl = self.FindWindowById(INTERNALDOCUMENT_TEXTCONTENT_ID)

    self.theName = nameCtrl.GetValue()
    self.theDescription = descCtrl.GetValue()
    self.theContent = contCtrl.GetValue()
    self.theCodes = contCtrl.codes()
    self.theMemos = contCtrl.memos()

    if len(self.theName) == 0:
      dlg = wx.MessageDialog(self,'Name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theDescription) == 0:
      dlg = wx.MessageDialog(self,'Description cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theContent) == 0):
      dlg = wx.MessageDialog(self,'Content cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(INTERNALDOCUMENT_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = InternalDocumentParameters(self.theName,self.theDescription,self.theContent,self.theCodes,self.theMemos)
    parameters.setId(self.theId)
    return parameters
