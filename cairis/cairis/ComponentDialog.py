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
from ComponentPanel import ComponentPanel
from ComponentParameters import ComponentParameters
import DialogClassParameters

class ComponentDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,parameters.id(),parameters.label(),style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,500))
    self.theName = ''
    self.theDescription = ''
    self.theInterfaces = []
    self.theStructure = []
    self.theRequirements = []
    self.theComponentId = -1
    self.panel = 0
    self.buildControls(parameters)
    self.commitVerb = 'Add'
    
  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = ComponentPanel(self)
    self.panel.buildControls(parameters.createFlag())
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.COMPONENT_BUTTONCOMMIT_ID,self.onCommit)

  def load(self,component):
    self.theComponentId = component.id()
    self.panel.loadControls(component)
    self.commitVerb = 'Edit'

  def onCommit(self,evt):
    commitLabel = self.commitVerb + ' component'
    nameCtrl = self.FindWindowById(armid.COMPONENT_TEXTNAME_ID)
    descCtrl = self.FindWindowById(armid.COMPONENT_TEXTDESCRIPTION_ID)
    ifCtrl = self.FindWindowById(armid.COMPONENT_LISTINTERFACES_ID)
    structCtrl = self.FindWindowById(armid.COMPONENT_LISTSTRUCTURE_ID)
    reqsCtrl = self.FindWindowById(armid.COMPONENT_LISTREQUIREMENTS_ID)
    self.theName = nameCtrl.GetValue()
    self.theDescription = descCtrl.GetValue()
    self.theInterfaces = ifCtrl.dimensions()
    self.theStructure = structCtrl.associations()
    self.theRequirements = reqsCtrl.requirements()

    if len(self.theName) == 0:
      dlg = wx.MessageDialog(self,'Component name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theDescription) == 0:
      dlg = wx.MessageDialog(self,'Description cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theInterfaces) == 0:
      dlg = wx.MessageDialog(self,'Interfaces need to be defined for components',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(armid.COMPONENT_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = ComponentParameters(self.theName,self.theDescription,self.theInterfaces,self.theStructure,self.theRequirements)
    parameters.setId(self.theComponentId)
    return parameters
