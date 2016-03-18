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
from ComponentViewPanel import ComponentViewPanel
from ComponentViewParameters import ComponentViewParameters
import DialogClassParameters

class ComponentViewDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,parameters.id(),parameters.label(),style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,500))
    self.theName = ''
    self.theSynopsis = ''
    self.theComponents = []
    self.theConnectors = []
    self.theComponentViewId = -1
    self.panel = 0
    self.buildControls(parameters)
    self.commitVerb = 'Add'
    
  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = ComponentViewPanel(self)
    self.panel.buildControls(parameters.createFlag())
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.COMPONENTVIEW_BUTTONCOMMIT_ID,self.onCommit)

  def load(self,cv):
    self.theComponentViewId = cv.id()
    self.panel.loadControls(cv)
    self.commitVerb = 'Edit'

  def onCommit(self,evt):
    commitLabel = self.commitVerb + ' component view'
    nameCtrl = self.FindWindowById(armid.COMPONENTVIEW_TEXTNAME_ID)
    synCtrl = self.FindWindowById(armid.COMPONENTVIEW_TEXTSYNOPSIS_ID)
    comCtrl = self.FindWindowById(armid.COMPONENTVIEW_LISTCOMPONENTS_ID)
    conCtrl = self.FindWindowById(armid.COMPONENTVIEW_LISTCONNECTORS_ID)
    self.theName = nameCtrl.GetValue()
    self.theSynopsis = synCtrl.GetValue()
    self.theComponents = comCtrl.dimensions()
    self.theConnectors = conCtrl.dimensions()

    if len(self.theName) == 0:
      dlg = wx.MessageDialog(self,'Name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theSynopsis) == 0:
      dlg = wx.MessageDialog(self,'Synopsis cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theComponents) == 0:
      dlg = wx.MessageDialog(self,'Components need to be defined for component views',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(armid.COMPONENTVIEW_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = ComponentViewParameters(self.theName,self.theSynopsis,[],[],[],[],[],self.theComponents,self.theConnectors)
    parameters.setId(self.theComponentViewId)
    return parameters
