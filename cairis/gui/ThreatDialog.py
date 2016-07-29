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
from cairis.core.ThreatParameters import ThreatParameters
from ThreatPanel import ThreatPanel

__author__ = 'Shamal Faily'

class ThreatDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,parameters.id(),parameters.label(),style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(600,600))
    self.theThreatId = -1
    self.theThreatName = ''
    self.theThreatType = ''
    self.theThreatMethod = ''
    self.theTags = []
    self.theEnvironmentProperties = []
    self.panel = 0
    self.buildControls(parameters)
    self.theCommitVerb = 'Add'
    
  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = ThreatPanel(self)
    self.panel.buildControls(parameters.createFlag())
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,THREAT_BUTTONCOMMIT_ID,self.onCommit)


  def load(self,threat):
    self.theThreatId = threat.id() 
    self.panel.loadControls(threat)
    self.theCommitVerb = 'Edit'

  def onCommit(self,evt):
    nameCtrl = self.FindWindowById(THREAT_TEXTNAME_ID)
    tagCtrl = self.FindWindowById(THREAT_TAGS_ID)
    typeCtrl = self.FindWindowById(THREAT_THREATTYPE_ID)
    methodCtrl = self.FindWindowById(THREAT_TEXTMETHOD_ID)
    environmentCtrl = self.FindWindowById(THREAT_PANELENVIRONMENT_ID)

    self.theThreatName = nameCtrl.GetValue()
    if (self.theCommitVerb == 'Add'):
      b = Borg()
      try:
        b.dbProxy.nameCheck(self.theThreatName,'threat')
      except ARMException,errorText:
        dlg = wx.MessageDialog(self,str(errorText),'Add threat',wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
        return

    self.theThreatType = typeCtrl.GetValue()
    self.theThreatMethod = methodCtrl.GetValue()
    self.theTags = tagCtrl.tags()
    self.theEnvironmentProperties = environmentCtrl.environmentProperties()

    commitLabel = self.theCommitVerb + ' threat'

    if len(self.theThreatName) == 0:
      dlg = wx.MessageDialog(self,'Threat name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theThreatType) == 0:
      dlg = wx.MessageDialog(self,'Threat type cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif len(self.theThreatMethod) == 0:
      dlg = wx.MessageDialog(self,'Method cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      for environmentProperties in self.theEnvironmentProperties:
        if len(environmentProperties.likelihood()) == 0:
          errorTxt = 'No likelihood associated with environment ' + environmentProperties.name()
          dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK)
          dlg.ShowModal()
          dlg.Destroy()
          return
        if len(environmentProperties.attackers()) == 0:
          errorTxt = 'No attackers associated with environment ' + environmentProperties.name()
          dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK)
          dlg.ShowModal()
          dlg.Destroy()
          return
        if len(environmentProperties.assets()) == 0:
          errorTxt = 'No assets associated with environment ' + environmentProperties.name()
          dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK)
          dlg.ShowModal()
          dlg.Destroy()
          return
        if len(environmentProperties.properties()) == 0:
          errorTxt = 'No security properties associated with environment ' + environmentProperties.name()
          dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK)
          dlg.ShowModal()
          dlg.Destroy()
          return
      self.EndModal(THREAT_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = ThreatParameters(self.theThreatName,self.theThreatType,self.theThreatMethod,self.theTags,self.theEnvironmentProperties)
    parameters.setId(self.theThreatId)
    return parameters
