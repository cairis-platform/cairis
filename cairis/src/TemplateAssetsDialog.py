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
from TemplateAssetDialog import TemplateAssetDialog
from DialogClassParameters import DialogClassParameters
import ARM
from DimensionBaseDialog import DimensionBaseDialog

class TemplateAssetsDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,armid.TEMPLATEASSETS_ID,'Template Assets',(930,300),'asset.png')
    self.rmFrame = parent
    idList = [armid.TEMPLATEASSETS_ASSETLIST_ID,armid.TEMPLATEASSETS_BUTTONADD_ID,armid.TEMPLATEASSETS_BUTTONDELETE_ID]
    columnList = ['Name','Type']
    self.buildControls(idList,columnList,self.dbProxy.getTemplateAssets,'template_asset')
    listCtrl = self.FindWindowById(armid.TEMPLATEASSETS_ASSETLIST_ID)
    listCtrl.SetColumnWidth(0,150)
    listCtrl.SetColumnWidth(1,150)


  def addObjectRow(self,assetListCtrl,listRow,asset):
    assetListCtrl.InsertStringItem(listRow,asset.name())
    assetListCtrl.SetStringItem(listRow,1,asset.type())

  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters(armid.TEMPLATEASSET_ID,'Add template asset',TemplateAssetDialog,armid.TEMPLATEASSET_BUTTONCOMMIT_ID,self.dbProxy.addTemplateAsset,True)
      self.addObject(addParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add template asset',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.selectedLabel]
    assetId = selectedObjt.id()
    try:
      updateParameters = DialogClassParameters(armid.TEMPLATEASSET_ID,'Edit template asset',TemplateAssetDialog,armid.TEMPLATEASSET_BUTTONCOMMIT_ID,self.dbProxy.updateTemplateAsset,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit template asset',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No template asset','Delete template asset',self.dbProxy.deleteTemplateAsset)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete template asset',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy
