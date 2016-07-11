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
from BasePanel import BasePanel
import cairis.core.Asset
from cairis.core.Borg import Borg
from AssetSummaryNotebook import AssetSummaryNotebook
from AssetEnvironmentPanel import AssetEnvironmentPanel

class AssetPanel(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,ASSET_ID)
    self.theAssetId = None
    b = Borg()
    self.dbProxy = b.dbProxy
    
  def buildControls(self,isCreate,isUpdateable=True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(self.buildTextSizer('Name',(87,30),ASSET_TEXTNAME_ID),0,wx.EXPAND)
    mainSizer.Add(self.buildTagCtrlSizer((87,30),ASSET_TAGS_ID),0,wx.EXPAND)
    mainSizer.Add(self.buildTextSizer('Short Code',(87,30),ASSET_TEXTSHORTCODE_ID),0,wx.EXPAND)
    typeList = self.dbProxy.getDimensionNames('asset_type')
    mainSizer.Add(self.buildComboSizerList('Type',(87,30),ASSET_COMBOTYPE_ID,typeList),0,wx.EXPAND)

    nbBox = wx.StaticBox(self,-1)
    nbSizer = wx.StaticBoxSizer(nbBox,wx.VERTICAL)
    mainSizer.Add(nbSizer,1,wx.EXPAND)
    nbSizer.Add(AssetSummaryNotebook(self),1,wx.EXPAND)

    mainSizer.Add(AssetEnvironmentPanel(self,self.dbProxy),1,wx.EXPAND)
    if (isUpdateable):
      mainSizer.Add(self.buildCommitButtonSizer(ASSET_BUTTONCOMMIT_ID,isCreate),0,wx.CENTER)
    self.SetSizer(mainSizer)
    environmentCtrl = self.FindWindowById(ASSET_PANELENVIRONMENT_ID)

  def loadControls(self,asset,isReadOnly=False):
    self.theAssetId = asset.id()
    nameCtrl = self.FindWindowById(ASSET_TEXTNAME_ID)
    nameCtrl.SetValue(asset.name())
    tagsCtrl = self.FindWindowById(ASSET_TAGS_ID)
    tagsCtrl.set(asset.tags())
    ifCtrl = self.FindWindowById(ASSET_PAGEINTERFACE_ID)
    ifCtrl.load(asset.interfaces())
    shortCodeCtrl = self.FindWindowById(ASSET_TEXTSHORTCODE_ID)
    shortCodeCtrl.SetValue(asset.shortCode())
    typeCtrl = self.FindWindowById(ASSET_COMBOTYPE_ID)
    typeCtrl.SetValue(asset.type())
    descriptionCtrl = self.FindWindowById(ASSET_TEXTDESCRIPTION_ID)
    descriptionCtrl.SetValue(asset.description())
    sigCtrl = self.FindWindowById(ASSET_TEXTSIGNIFICANCE_ID)
    sigCtrl.SetValue(asset.significance())
    criticalCtrl = self.FindWindowById(ASSET_CHECKCRITICAL_ID)
    criticalCtrl.SetValue(asset.critical())
    if (asset.critical() == True):
      criticalRationaleCtrl = self.FindWindowById(ASSET_TEXTCRITICALRATIONALE_ID)
      criticalRationaleCtrl.Enable()
      criticalRationaleCtrl.SetValue(asset.criticalRationale())

    environmentCtrl = self.FindWindowById(ASSET_PANELENVIRONMENT_ID)
    environmentCtrl.loadControls(asset)
