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
from EnvironmentPanel import EnvironmentPanel
from EnvironmentParameters import EnvironmentParameters

class EnvironmentDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,parameters.id(),parameters.label(),style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(750,400))
    self.theEnvironmentId = -1
    self.environmentName = ''
    self.environmentShortCode = ''
    self.environmentDescription = ''
    self.theEnvironments = []
    self.theDuplicateProperty = ''
    self.theOverridingEnvironment = ''
    self.theTensions = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    self.buildControls(parameters)
    self.theCommitVerb = 'Create'

  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = EnvironmentPanel(self)
    self.panel.buildControls(parameters.createFlag())
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.ENVIRONMENT_BUTTONCOMMIT_ID,self.onCommit)

  def load(self,environment):
    self.theEnvironmentId = environment.id()
    self.panel.loadControls(environment)
    self.theCommitVerb = 'Edit'

  def onCommit(self,evt):
    nameCtrl = self.FindWindowById(armid.ENVIRONMENT_TEXTNAME_ID)
    shortCodeCtrl = self.FindWindowById(armid.ENVIRONMENT_TEXTSHORTCODE_ID)
    valueCtrl = self.FindWindowById(armid.ENVIRONMENT_TEXTDESCRIPTION_ID)
    environmentCtrl = self.FindWindowById(armid.ENVIRONMENT_PANELENVIRONMENTPROPERTIES_ID)
    tensionsCtrl = self.FindWindowById(armid.ENVIRONMENT_GRIDVALUETENSIONS_ID)

    self.environmentName = nameCtrl.GetValue()
    self.environmentShortCode = shortCodeCtrl.GetValue()
    self.environmentDescription = valueCtrl.GetValue()
    self.theEnvironments = environmentCtrl.environments()
    self.theTensions = tensionsCtrl.tensions()
    commitLabel = self.theCommitVerb + ' environment'

    if len(self.environmentName) == 0:
      dlg = wx.MessageDialog(self,'Environment name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.environmentShortCode) == 0):
      dlg = wx.MessageDialog(self,'Environment short code cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.environmentDescription) == 0):
      dlg = wx.MessageDialog(self,'Environment description cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theEnvironments) > 0):
      self.theDuplicateProperty = environmentCtrl.duplicateProperty()
      self.theOverridingEnvironment = environmentCtrl.overridingEnvironment()
      if (self.theDuplicateProperty == 'Override') and (len(self.theOverridingEnvironment) == 0):
        dlg = wx.MessageDialog(self,'An overriding environment has not been selected',commitLabel,wx.OK) 
        dlg.ShowModal()
        dlg.Destroy()
        return 
    
    self.EndModal(armid.ENVIRONMENT_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = EnvironmentParameters(self.environmentName,self.environmentShortCode,self.environmentDescription,self.theEnvironments,self.theDuplicateProperty,self.theOverridingEnvironment,self.theTensions)
    parameters.setId(self.theEnvironmentId)
    return parameters

