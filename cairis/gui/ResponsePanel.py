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
import ARM
import armid
from Borg import Borg
from BasePanel import BasePanel
from ResponseParameters import ResponseParameters
from AcceptEnvironmentPanel import AcceptEnvironmentPanel
from TransferEnvironmentPanel import TransferEnvironmentPanel
from MitigateEnvironmentPanel import MitigateEnvironmentPanel

class ResponsePanel(BasePanel):
  def __init__(self,parent,responseType,panel):
    BasePanel.__init__(self,parent,armid.RESPONSE_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theResponseName = ''
    self.theRiskName = ''
    self.theTags = []
    self.theCommitVerb = 'Create'
    self.environmentPanel = panel(self,self.dbProxy)
    self.environmentPanel.Disable()
    self.theEnvironmentProperties = []
    self.theResponseVerb = responseType

  def buildControls(self,isCreate,isUpdateable = True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(self.buildTextSizer('Name',(87,60),armid.RESPONSE_TEXTNAME_ID,isReadOnly=True),0,wx.EXPAND)
    mainSizer.Add(self.buildTagCtrlSizer((87,30),armid.RESPONSE_TAGS_ID),0,wx.EXPAND)
    mainSizer.Add(self.buildComboSizerList('Risk',(87,30),armid.RESPONSE_COMBORISK_ID,self.dbProxy.getDimensionNames('risk')),0,wx.EXPAND)
    mainSizer.Add(self.environmentPanel,1,wx.EXPAND)
    if (isUpdateable):
      mainSizer.Add(self.buildCommitButtonSizer(armid.RESPONSE_BUTTONCOMMIT_ID,isCreate),0,wx.ALIGN_CENTRE)
    self.SetSizer(mainSizer)
    self.nameCtrl = self.FindWindowById(armid.RESPONSE_TEXTNAME_ID)
    self.nameCtrl.Disable()
    self.riskCtrl = self.FindWindowById(armid.RESPONSE_COMBORISK_ID)
    self.riskCtrl.Bind(wx.EVT_COMBOBOX,self.onRiskChange)

  def onRiskChange(self,evt):
    riskName = self.riskCtrl.GetValue()
    if (riskName != ''):
      self.environmentPanel.Enable()
      self.environmentPanel.setRisk(riskName)
      if (self.environmentPanel.__class__.__name__ != 'MitigateEnvironmentPanel'):
        nameLabel = self.theResponseVerb + ' ' + riskName
        self.nameCtrl.SetValue(nameLabel)
      else:
        mitTypeCombo = self.environmentPanel.FindWindowById(armid.MITIGATE_COMBOTYPE_ID)
        mitType = mitTypeCombo.GetValue()
        if (mitType != ''):
          nameLabel = 'Mitigate' + ' ' + riskName 
          self.nameCtrl.SetValue(nameLabel)
    else:
      self.environmentPanel.Disable()
      self.nameCtrl.SetValue('')


  def loadControls(self,response,isReadOnly = False):
    self.nameCtrl.SetValue(response.name())
    tagsCtrl = self.FindWindowById(armid.RESPONSE_TAGS_ID)
    tagsCtrl.set(response.tags())

    self.riskCtrl.SetStringSelection(response.risk())
    self.environmentPanel.loadControls(response)
    self.theCommitVerb = 'Edit'

  def commit(self):
    self.theResponseName = self.nameCtrl.GetValue()
    commitLabel = self.theCommitVerb + ' response'
    if (self.theCommitVerb == 'Create'):
      b = Borg()
      try:
        b.dbProxy.nameCheck(self.theResponseName,'response')
      except ARM.ARMException,errorText:
        dlg = wx.MessageDialog(self,str(errorText),commitLabel,wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
        return

    self.theRiskName = self.riskCtrl.GetStringSelection()
    tagsCtrl = self.FindWindowById(armid.RESPONSE_TAGS_ID)
    self.theTags = tagsCtrl.tags()
    try:
      self.theEnvironmentProperties = self.environmentPanel.environmentProperties()
    except ARM.EnvironmentValidationError, errorText:
      dlg = wx.MessageDialog(self,str(errorText),commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return -1
    
    commitLabel = self.theCommitVerb + ' response'

    if (len(self.theResponseName) == 0):
      dlg = wx.MessageDialog(self,'No risk selected',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return -1
    elif (len(self.theRiskName) == 0):
      dlg = wx.MessageDialog(self,'No risk selected',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return -1
    elif (len(self.theEnvironmentProperties) == 0):
      dlg = wx.MessageDialog(self,'No environment specific properties set',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return -1
    else:
      return 0

  def parameters(self):
    return ResponseParameters(self.theResponseName,self.theRiskName,self.theTags,self.theEnvironmentProperties,self.theResponseVerb)
