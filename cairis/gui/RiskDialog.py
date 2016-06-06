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
import WidgetFactory
from cairis.core.ARM import *
from cairis.core.Borg import Borg
import cairis.core.ObjectFactory
from DialogClassParameters import DialogClassParameters
from cairis.core.RiskParameters import RiskParameters
from RiskDialogParameters import RiskDialogParameters
from RiskPanel import RiskPanel
from MisuseCaseDialog import MisuseCaseDialog

class RiskDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,parameters.id(),parameters.label(),style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,550))

    self.theRiskId = -1
    self.theMisuseCase = None
    self.theThreatName = ''
    self.theVulnerabilityName = ''
    self.theTags = []
    self.panel = 0
    self.buildControls(parameters)
    self.commitVerb = 'Create'
 
  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = RiskPanel(self)
    self.panel.buildControls(parameters.createFlag())
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,RISK_BUTTONCOMMIT_ID,self.onCommit)
    wx.EVT_BUTTON(self,RISK_BUTTONMISUSECASE_ID,self.onMisuseCase)

  def load(self,risk):
    self.theRiskId = risk.id()
    self.theMisuseCase = risk.misuseCase()
    self.panel.loadControls(risk)
    self.commitVerb = 'Edit'
    if (self.theMisuseCase != None):
      mcButton = self.FindWindowById(RISK_BUTTONMISUSECASE_ID)
      mcButton.SetLabel('Edit Misuse Case')
    

  def onMisuseCase(self,evt):
    nameCtrl = self.FindWindowById(RISK_TEXTNAME_ID)
    threatCtrl = self.FindWindowById(RISK_COMBOTHREAT_ID)
    vulCtrl = self.FindWindowById(RISK_COMBOVULNERABILITY_ID)

    riskName = nameCtrl.GetValue() 
    if (self.commitVerb == 'Create'):
      b = Borg()
      try:
        b.dbProxy.nameCheck(riskName,'risk')
      except ARMException,errorText:
        dlg = wx.MessageDialog(self,str(errorText),'Add Misuse Case',wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
        return

    threatName = threatCtrl.GetStringSelection()
    vulnerabilityName = vulCtrl.GetStringSelection()

    commitLabel = self.commitVerb + ' risk'
    if len(riskName) == 0:
      dlg = wx.MessageDialog(self,'No risk name entered',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(threatName) == 0:
      dlg = wx.MessageDialog(self,'No threat selected',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(vulnerabilityName) == 0):
      dlg = wx.MessageDialog(self,'No vulnerability selected',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return

    isCreate = False
    if (self.theMisuseCase == None):
      isCreate = True
    dlg = MisuseCaseDialog(self,isCreate)
    if (self.theMisuseCase != None):
      self.theMisuseCase.theThreatName = threatName
      self.theMisuseCase.theVulnerabilityName = vulnerabilityName
      dlg.loadMisuseCase(self.theMisuseCase)
    else:
      dlg.loadRiskComponents(riskName,threatName,vulnerabilityName)
    if (dlg.ShowModal() == MISUSECASE_BUTTONCOMMIT_ID):
      if (self.theMisuseCase != None):
        self.theMisuseCase = cairis.core.ObjectFactory.build(self.theMisuseCase.id(),dlg.parameters())
      else:
        self.theMisuseCase = cairis.core.ObjectFactory.build(-1,dlg.parameters())
      mcButton = self.FindWindowById(RISK_BUTTONMISUSECASE_ID)
      mcButton.SetLabel('Edit Misuse Case')

  def onCommit(self,evt):
    nameCtrl = self.FindWindowById(RISK_TEXTNAME_ID)
    threatCtrl = self.FindWindowById(RISK_COMBOTHREAT_ID)
    vulCtrl = self.FindWindowById(RISK_COMBOVULNERABILITY_ID)
    tagCtrl = self.FindWindowById(RISK_TAGS_ID)

    commitLabel = self.commitVerb + ' risk'
    self.theRiskName = nameCtrl.GetValue() 
    self.theTags = tagCtrl.tags()

    b = Borg()
    if (self.commitVerb == 'Create'):
      try:
        b.dbProxy.nameCheck(self.theRiskName,'risk')
      except ARMException,errorText:
        dlg = wx.MessageDialog(self,str(errorText),commitLabel,wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
        return

    self.theThreatName = threatCtrl.GetStringSelection()
    self.theVulnerabilityName = vulCtrl.GetStringSelection()

    if len(self.theRiskName) == 0:
      dlg = wx.MessageDialog(self,'No risk name entered',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theThreatName) == 0:
      dlg = wx.MessageDialog(self,'No threat selected',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theVulnerabilityName) == 0):
      dlg = wx.MessageDialog(self,'No vulnerability selected',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (self.theMisuseCase == None):
      dlg = wx.MessageDialog(self,'No Misuse Case defined',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(RISK_BUTTONCOMMIT_ID)

  def parameters(self): 
    parameters = RiskParameters(self.theRiskName,self.theThreatName,self.theVulnerabilityName,self.theMisuseCase,self.theTags)
    parameters.setId(self.theRiskId)
    return parameters
