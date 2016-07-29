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
from TemplateRequirementPanel import TemplateRequirementPanel
from cairis.core.TemplateRequirementParameters import TemplateRequirementParameters
import DialogClassParameters

__author__ = 'Shamal Faily'

class TemplateRequirementDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,parameters.id(),parameters.label(),style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,500))
    self.theRequirementId = -1
    self.theName = ''
    self.theAssetName = ''
    self.theDescription = ''
    self.theType = ''
    self.theRationale = ''
    self.theFitCriterion = ''
    self.panel = 0
    self.buildControls(parameters)
    self.commitVerb = 'Add'
    
  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = TemplateRequirementPanel(self)
    self.panel.buildControls(parameters.createFlag())
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,TEMPLATEREQUIREMENT_BUTTONCOMMIT_ID,self.onCommit)

  def load(self,req):
    self.theRequirementId = req.id()
    self.panel.loadControls(req)
    self.commitVerb = 'Edit'

  def onCommit(self,evt):
    commitLabel = self.commitVerb + ' template requirement'
    nameCtrl = self.FindWindowById(TEMPLATEREQUIREMENT_TEXTNAME_ID)
    assetCtrl = self.FindWindowById(TEMPLATEREQUIREMENT_COMBOASSET_ID)
    descCtrl = self.FindWindowById(TEMPLATEREQUIREMENT_TEXTDESCRIPTION_ID)
    typeCtrl = self.FindWindowById(TEMPLATEREQUIREMENT_COMBOTYPE_ID)
    ratCtrl = self.FindWindowById(TEMPLATEREQUIREMENT_TEXTRATIONALE_ID)
    fcCtrl = self.FindWindowById(TEMPLATEREQUIREMENT_TEXTFITCRITERION_ID)

    self.theName = nameCtrl.GetValue()
    self.theAssetName = assetCtrl.GetValue()
    self.theDescription = descCtrl.GetValue()
    self.theType = typeCtrl.GetValue()
    self.theRationale = ratCtrl.GetValue()
    self.theFitCriterion = fcCtrl.GetValue()

    if len(self.theName) == 0:
      dlg = wx.MessageDialog(self,'Requirement name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theAssetName) == 0:
      dlg = wx.MessageDialog(self,'Asset name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theDescription) == 0:
      dlg = wx.MessageDialog(self,'Description cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theType) == 0):
      dlg = wx.MessageDialog(self,'Requirement type cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theRationale) == 0):
      dlg = wx.MessageDialog(self,'Rationale cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theFitCriterion) == 0):
      dlg = wx.MessageDialog(self,'Fit Criterion cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(TEMPLATEREQUIREMENT_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = TemplateRequirementParameters(self.theName,self.theAssetName,self.theType,self.theDescription,self.theRationale,self.theFitCriterion)
    parameters.setId(self.theRequirementId)
    return parameters
