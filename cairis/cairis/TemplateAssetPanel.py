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
from BasePanel import BasePanel
import TemplateAsset
from Borg import Borg
from ValueDictionary import ValueDictionary
from AssetSummaryNotebook import AssetSummaryNotebook
from SingleEnvironmentPropertiesListCtrl import SingleEnvironmentPropertiesListCtrl

class TemplateAssetPanel(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,armid.TEMPLATEASSET_ID)
    self.theAssetId = None
    b = Borg()
    self.dbProxy = b.dbProxy
    
  def buildControls(self,isCreate,isUpdateable=True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(self.buildTextSizer('Name',(87,30),armid.ASSET_TEXTNAME_ID),0,wx.EXPAND)
    mainSizer.Add(self.buildTagCtrlSizer((87,30),armid.ASSET_TAGS_ID),0,wx.EXPAND)
    mainSizer.Add(self.buildTextSizer('Short Code',(87,30),armid.ASSET_TEXTSHORTCODE_ID),0,wx.EXPAND)
    typeList = self.dbProxy.getDimensionNames('asset_type')
    mainSizer.Add(self.buildComboSizerList('Type',(87,30),armid.ASSET_COMBOTYPE_ID,typeList),0,wx.EXPAND)

    stList =self.dbProxy.getDimensionNames('surface_type')
    arList =self.dbProxy.getDimensionNames('access_right')
    mainSizer.Add(self.buildComboSizerList('Surface Type',(87,30),armid.ASSET_COMBOSURFACETYPE_ID,stList),0,wx.EXPAND)
    mainSizer.Add(self.buildComboSizerList('Access Right',(87,30),armid.ASSET_COMBOACCESSRIGHT_ID,arList),0,wx.EXPAND)

    nbBox = wx.StaticBox(self,-1)
    nbSizer = wx.StaticBoxSizer(nbBox,wx.VERTICAL)
    mainSizer.Add(nbSizer,1,wx.EXPAND)
    nbSizer.Add(AssetSummaryNotebook(self,True),1,wx.EXPAND)

    valueLookup = ValueDictionary(['None','Low','Medium','High'])
    pBox = wx.StaticBox(self,-1)
    pSizer = wx.StaticBoxSizer(pBox,wx.VERTICAL)
    mainSizer.Add(pSizer,1,wx.EXPAND)
    self.propertiesList = SingleEnvironmentPropertiesListCtrl(self,armid.TEMPLATEASSET_LISTPROPERTIES_ID,valueLookup)
    pSizer.Add(self.propertiesList,1,wx.EXPAND)

    mainSizer.Add(self.buildCommitButtonSizer(armid.TEMPLATEASSET_BUTTONCOMMIT_ID,isCreate),0,wx.CENTER)
    self.SetSizer(mainSizer)

  def loadControls(self,asset,isReadOnly=False):
    self.theAssetId = asset.id()
    nameCtrl = self.FindWindowById(armid.ASSET_TEXTNAME_ID)
    nameCtrl.SetValue(asset.name())
    tagsCtrl = self.FindWindowById(armid.ASSET_TAGS_ID)
    tagsCtrl.set(asset.tags())
    shortCodeCtrl = self.FindWindowById(armid.ASSET_TEXTSHORTCODE_ID)
    shortCodeCtrl.SetValue(asset.shortCode())
    typeCtrl = self.FindWindowById(armid.ASSET_COMBOTYPE_ID)
    typeCtrl.SetValue(asset.type())
    stCtrl = self.FindWindowById(armid.ASSET_COMBOSURFACETYPE_ID)
    stCtrl.SetValue(asset.surfaceType())
    arCtrl = self.FindWindowById(armid.ASSET_COMBOACCESSRIGHT_ID)
    arCtrl.SetValue(asset.accessRight())
    descriptionCtrl = self.FindWindowById(armid.ASSET_TEXTDESCRIPTION_ID)
    descriptionCtrl.SetValue(asset.description())
    sigCtrl = self.FindWindowById(armid.ASSET_TEXTSIGNIFICANCE_ID)
    sigCtrl.SetValue(asset.significance())
    ifCtrl = self.FindWindowById(armid.ASSET_PAGEINTERFACE_ID)
    ifCtrl.load(asset.interfaces())
    propertiesCtrl = self.FindWindowById(armid.TEMPLATEASSET_LISTPROPERTIES_ID)
    propertiesCtrl.load(asset.properties())

