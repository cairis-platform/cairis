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
import Asset
from AssetDialog import AssetDialog
from DialogClassParameters import DialogClassParameters
import ARM
import os
import xml.sax
from DimensionBaseDialog import DimensionBaseDialog

class AssetsDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,armid.ASSETS_ID,'Assets',(930,300),'asset.png')
    self.rmFrame = parent
    idList = [armid.ASSETS_ASSETLIST_ID,armid.ASSETS_BUTTONADD_ID,armid.ASSETS_BUTTONDELETE_ID]
    columnList = ['Name','Type']
    self.buildControls(idList,columnList,self.dbProxy.getAssets,'asset')
    listCtrl = self.FindWindowById(armid.ASSETS_ASSETLIST_ID)
    listCtrl.SetColumnWidth(0,200)
    listCtrl.SetColumnWidth(1,200)
    
  def addObjectRow(self,assetListCtrl,listRow,asset):
    assetListCtrl.InsertStringItem(listRow,asset.name())
    assetListCtrl.SetStringItem(listRow,1,asset.type())

  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters(armid.ASSET_ID,'Add asset',AssetDialog,armid.ASSET_BUTTONCOMMIT_ID,self.dbProxy.addAsset,True)
      self.addObject(addParameters)
      self.rmFrame.updateObjectSelection(self.selectedLabel)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add asset',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.selectedLabel]
    assetId = selectedObjt.id()
    try:
      updateParameters = DialogClassParameters(armid.ASSET_ID,'Edit asset',AssetDialog,armid.ASSET_BUTTONCOMMIT_ID,self.dbProxy.updateAsset,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit asset',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No asset','Delete asset',self.dbProxy.deleteAsset)
      self.rmFrame.updateObjectSelection()
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete asset',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy
