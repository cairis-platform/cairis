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
from cairis.core.ARM import *
import AssetPanel
from cairis.core.AssetParameters import AssetParameters
from cairis.core.Borg import Borg
import DialogClassParameters

class AssetDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,parameters.id(),parameters.label(),style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,500))
    self.theAssetName = ''
    self.theShortCode = ''
    self.theAssetDescription = ''
    self.theAssetSignificance = ''
    self.theType = ''
    self.theTags = []
    self.theInterfaces = []
    self.theCriticalIndicator = False
    self.theCriticalRationale = ''
    self.theEnvironmentProperties = []
    self.theAssetId = -1
    self.panel = 0
    self.buildControls(parameters)
    self.commitVerb = 'Add'
    
  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = AssetPanel.AssetPanel(self)
    self.panel.buildControls(parameters.createFlag())
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,ASSET_BUTTONCOMMIT_ID,self.onCommit)

  def load(self,asset):
    self.theAssetId = asset.id()
    self.panel.loadControls(asset)
    self.commitVerb = 'Edit'

  def onCommit(self,evt):
    commitLabel = self.commitVerb + ' asset'
    nameCtrl = self.FindWindowById(ASSET_TEXTNAME_ID)
    tagCtrl = self.FindWindowById(ASSET_TAGS_ID)
    shortCodeCtrl = self.FindWindowById(ASSET_TEXTSHORTCODE_ID)
    descriptionCtrl = self.FindWindowById(ASSET_TEXTDESCRIPTION_ID)
    sigCtrl = self.FindWindowById(ASSET_TEXTSIGNIFICANCE_ID)
    typeCtrl = self.FindWindowById(ASSET_COMBOTYPE_ID)
    criticalCtrl = self.FindWindowById(ASSET_CHECKCRITICAL_ID)
    criticalRationaleCtrl = self.FindWindowById(ASSET_TEXTCRITICALRATIONALE_ID)
    interfacesCtrl = self.FindWindowById(ASSET_PAGEINTERFACE_ID)
    environmentCtrl = self.FindWindowById(ASSET_PANELENVIRONMENT_ID)
    self.theAssetName = nameCtrl.GetValue()
    if (self.commitVerb == 'Add'):
      b = Borg()
      try:
        b.dbProxy.nameCheck(self.theAssetName,'asset')
      except ARMException,errorText:
        dlg = wx.MessageDialog(self,str(errorText),'Add asset',wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
        return
    self.theTags = tagCtrl.tags()
    self.theShortCode = shortCodeCtrl.GetValue()
    self.theAssetDescription = descriptionCtrl.GetValue()
    self.theAssetSignificance = sigCtrl.GetValue()
    self.theType = typeCtrl.GetValue()
    self.theCriticalIndicator = criticalCtrl.GetValue()
    self.theCriticalRationale = criticalRationaleCtrl.GetValue()
    self.theInterfaces = interfacesCtrl.dimensions()
    self.theEnvironmentProperties = environmentCtrl.environmentProperties()

    if len(self.theAssetName) == 0:
      dlg = wx.MessageDialog(self,'Asset name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theShortCode) == 0:
      dlg = wx.MessageDialog(self,'Short code cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theType) == 0:
      dlg = wx.MessageDialog(self,'Asset type cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theAssetDescription) == 0):
      dlg = wx.MessageDialog(self,'Asset description cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theAssetSignificance) == 0):
      dlg = wx.MessageDialog(self,'Asset significance cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      for environmentProperties in self.theEnvironmentProperties:
        if len(environmentProperties.properties()) == 0:
          errorTxt = 'No security properties associated with environment ' + environmentProperties.name()
          dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK)
          dlg.ShowModal()
          dlg.Destroy()
          return
      self.EndModal(ASSET_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = AssetParameters(self.theAssetName,self.theShortCode,self.theAssetDescription,self.theAssetSignificance,self.theType,self.theCriticalIndicator,self.theCriticalRationale,self.theTags,self.theInterfaces,self.theEnvironmentProperties)
    parameters.setId(self.theAssetId)
    return parameters
