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
import cairis.core.TemplateAsset
from cairis.core.Borg import Borg
from cairis.core.ValueDictionary import ValueDictionary
from AssetSummaryNotebook import AssetSummaryNotebook
from SingleEnvironmentPropertiesListCtrl import SingleEnvironmentPropertiesListCtrl

class TemplateAssetPanel(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,TEMPLATEASSET_ID)
    self.theAssetId = None
    b = Borg()
    self.dbProxy = b.dbProxy
    
  def buildControls(self,isCreate,isUpdateable=True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    nameSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(nameSizer,0,wx.EXPAND)
    nameSizer.Add(self.buildTextSizer('Name',(87,30),ASSET_TEXTNAME_ID),1,wx.EXPAND)
    nameSizer.Add(self.buildTextSizer('Short Code',(87,30),ASSET_TEXTSHORTCODE_ID),1,wx.EXPAND)
    typeList = self.dbProxy.getDimensionNames('asset_type')
    mainSizer.Add(self.buildComboSizerList('Type',(87,30),ASSET_COMBOTYPE_ID,typeList),0,wx.EXPAND)

    stList =self.dbProxy.getDimensionNames('surface_type')
    arList =self.dbProxy.getDimensionNames('access_right')
    metricsSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(metricsSizer,0,wx.EXPAND)
    metricsSizer.Add(self.buildComboSizerList('Surface Type',(87,30),ASSET_COMBOSURFACETYPE_ID,stList),1,wx.EXPAND)
    metricsSizer.Add(self.buildComboSizerList('Access Right',(87,30),ASSET_COMBOACCESSRIGHT_ID,arList),1,wx.EXPAND)
    mainSizer.Add(self.buildTagCtrlSizer((87,30),ASSET_TAGS_ID),0,wx.EXPAND)

    nbBox = wx.StaticBox(self,-1)
    nbSizer = wx.StaticBoxSizer(nbBox,wx.VERTICAL)
    mainSizer.Add(nbSizer,1,wx.EXPAND)
    nbSizer.Add(AssetSummaryNotebook(self,True),1,wx.EXPAND)

    valueLookup = ValueDictionary(['None','Low','Medium','High'])
    pBox = wx.StaticBox(self,-1)
    pSizer = wx.StaticBoxSizer(pBox,wx.VERTICAL)
    mainSizer.Add(pSizer,1,wx.EXPAND)
    self.propertiesList = SingleEnvironmentPropertiesListCtrl(self,TEMPLATEASSET_LISTPROPERTIES_ID,valueLookup)
    pSizer.Add(self.propertiesList,1,wx.EXPAND)

    mainSizer.Add(self.buildCommitButtonSizer(TEMPLATEASSET_BUTTONCOMMIT_ID,isCreate),0,wx.CENTER)
    self.SetSizer(mainSizer)

  def loadControls(self,asset,isReadOnly=False):
    self.theAssetId = asset.id()
    nameCtrl = self.FindWindowById(ASSET_TEXTNAME_ID)
    nameCtrl.SetValue(asset.name())
    tagsCtrl = self.FindWindowById(ASSET_TAGS_ID)
    tagsCtrl.set(asset.tags())
    shortCodeCtrl = self.FindWindowById(ASSET_TEXTSHORTCODE_ID)
    shortCodeCtrl.SetValue(asset.shortCode())
    typeCtrl = self.FindWindowById(ASSET_COMBOTYPE_ID)
    typeCtrl.SetValue(asset.type())
    stCtrl = self.FindWindowById(ASSET_COMBOSURFACETYPE_ID)
    stCtrl.SetValue(asset.surfaceType())
    arCtrl = self.FindWindowById(ASSET_COMBOACCESSRIGHT_ID)
    arCtrl.SetValue(asset.accessRight())
    descriptionCtrl = self.FindWindowById(ASSET_TEXTDESCRIPTION_ID)
    descriptionCtrl.SetValue(asset.description())
    sigCtrl = self.FindWindowById(ASSET_TEXTSIGNIFICANCE_ID)
    sigCtrl.SetValue(asset.significance())
    ifCtrl = self.FindWindowById(ASSET_PAGEINTERFACE_ID)
    ifCtrl.load(asset.interfaces())
    propertiesCtrl = self.FindWindowById(TEMPLATEASSET_LISTPROPERTIES_ID)
    propertiesCtrl.load(asset.properties())

