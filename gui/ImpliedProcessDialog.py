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
import os
from Borg import Borg
import ARM
from ImpliedProcessPanel import ImpliedProcessPanel
from ImpliedProcessParameters import ImpliedProcessParameters

class ImpliedProcessDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,parameters.id(),parameters.label(),style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(500,800))
    self.theParent = parent 
    self.theImpliedProcessId = -1
    self.theName = ''
    self.theDescription = ''
    self.thePersonaName = ''
    self.theCodeNetwork = []
    self.theSpecification = ''
    self.theChannels = []
    self.panel = 0
    self.buildControls(parameters)
    self.theCommitVerb = 'Create'

  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = ImpliedProcessPanel(self,parameters.createFlag())
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.IMPLIEDPROCESS_BUTTONCOMMIT_ID,self.onCommit)

  def load(self,implProc):
    self.theImpliedProcessId = implProc.id()
    self.panel.loadControls(implProc)
    self.theCommitVerb = 'Edit'

  def onCommit(self,evt):
    nameCtrl = self.FindWindowById(armid.IMPLIEDPROCESS_TEXTNAME_ID)
    descCtrl = self.FindWindowById(armid.IMPLIEDPROCESS_TEXTDESCRIPTION_ID)
    personaCtrl = self.FindWindowById(armid.IMPLIEDPROCESS_COMBOPERSONA_ID)
    specCtrl = self.FindWindowById(armid.IMPLIEDPROCESS_TEXTSPECIFICATION_ID)
    channelCtrl = self.FindWindowById(armid.IMPLIEDPROCESS_LISTCHANNELS_ID)
     
    self.theName = nameCtrl.GetValue()
    self.theDescription = descCtrl.GetValue()
    self.thePersonaName = personaCtrl.GetValue()
    self.theCodeNetwork = self.panel.dimensions()
    self.theSpecification = specCtrl.GetValue()
    self.theChannels = channelCtrl.channels()

    commitLabel = self.theCommitVerb + ' implied process'

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
    if len(self.thePersonaName) == 0:
      dlg = wx.MessageDialog(self,'Persona name cannot be empty',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theCodeNetwork) == 0:
      dlg = wx.MessageDialog(self,'Code relationships must be selected',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theSpecification) == 0:
      dlg = wx.MessageDialog(self,'Specification cannot be empty',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif len(self.theChannels) == 0:
      dlg = wx.MessageDialog(self,'Channel list cannot be empty',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return

    self.EndModal(armid.IMPLIEDPROCESS_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = ImpliedProcessParameters(self.theName,self.theDescription,self.thePersonaName,self.theCodeNetwork,self.theSpecification,self.theChannels)
    parameters.setId(self.theImpliedProcessId)
    return parameters



