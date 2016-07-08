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
from DomainPropertyPanel import DomainPropertyPanel
from cairis.core.DomainPropertyParameters import DomainPropertyParameters
import DialogClassParameters

class DomainPropertyDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,parameters.id(),parameters.label(),style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(600,400))
    self.theId = -1
    self.theName = ''
    self.theTags = []
    self.theType = ''
    self.theOriginator = ''
    self.theDescription = ''
    self.panel = 0
    self.buildControls(parameters)
    self.commitVerb = 'Add'
    
  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = DomainPropertyPanel(self)
    self.panel.buildControls(parameters.createFlag())
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,DOMAINPROPERTY_BUTTONCOMMIT_ID,self.onCommit)

  def load(self,dp):
    self.theId = dp.id()
    self.panel.loadControls(dp)
    self.commitVerb = 'Edit'

  def onCommit(self,evt):
    nameCtrl = self.FindWindowById(DOMAINPROPERTY_TEXTNAME_ID)
    tagsCtrl = self.FindWindowById(DOMAINPROPERTY_TAGS_ID)
    typeCtrl = self.FindWindowById(DOMAINPROPERTY_COMBOTYPE_ID)
    origCtrl = self.FindWindowById(DOMAINPROPERTY_TEXTORIGINATOR_ID)
    descCtrl = self.FindWindowById(DOMAINPROPERTY_TEXTDESCRIPTION_ID)

    self.theName = nameCtrl.GetValue()
    self.theTags = tagsCtrl.tags()
    self.theType = typeCtrl.GetValue()
    self.theOriginator = origCtrl.GetValue()
    self.theDescription = descCtrl.GetValue()

    commitLabel = self.commitVerb + ' Domain Property'
    if len(self.theName) == 0:
      dlg = wx.MessageDialog(self,'Property name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theType) == 0:
      dlg = wx.MessageDialog(self,'Domain Property type cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theOriginator) == 0:
      dlg = wx.MessageDialog(self,'Originator cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theDescription) == 0:
      dlg = wx.MessageDialog(self,'Domain Property description cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(DOMAINPROPERTY_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = DomainPropertyParameters(self.theName,self.theDescription,self.theType,self.theOriginator,self.theTags)
    parameters.setId(self.theId)
    return parameters
