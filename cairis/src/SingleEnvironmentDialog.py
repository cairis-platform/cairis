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
from SingleEnvironmentPanel import SingleEnvironmentPanel
from EnvironmentParameters import EnvironmentParameters

class SingleEnvironmentDialog(wx.Dialog):
  def __init__(self,parent,preText = 'New'):
    wx.Dialog.__init__(self,parent,armid.SINGLEENVIRONMENT_ID,preText + ' Environment',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(500,400))
    self.theEnvironmentId = -1
    self.environmentName = ''
    self.environmentShortCode = ''
    self.environmentDescription = ''
    self.buildControls()
    self.theCommitVerb = 'Create'

  def buildControls(self):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = SingleEnvironmentPanel(self)
    self.panel.buildControls()
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.ENVIRONMENT_BUTTONCOMMIT_ID,self.onCommit)

  def load(self,environment):
    self.theEnvironmentId = environment.id()
    self.panel.loadControls(environment)
    self.theCommitVerb = 'Edit'

  def onCommit(self,evt):
    nameCtrl = self.FindWindowById(armid.ENVIRONMENT_TEXTNAME_ID)
    valueCtrl = self.FindWindowById(armid.ENVIRONMENT_TEXTDESCRIPTION_ID)
    shortCodeCtrl = self.FindWindowById(armid.ENVIRONMENT_TEXTSHORTCODE_ID)

    self.environmentName = nameCtrl.GetValue()
    self.environmentDescription = valueCtrl.GetValue()
    self.environmentShortCode = shortCodeCtrl.GetValue()

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
    
    self.EndModal(armid.ENVIRONMENT_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = EnvironmentParameters(self.environmentName,self.environmentShortCode,self.environmentDescription)
    parameters.setId(self.theEnvironmentId)
    return parameters

  def name(self):
    return self.environmentName
