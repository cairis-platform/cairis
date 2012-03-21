#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/AssetsDialog.py $ $Id: AssetsDialog.py 527 2011-11-07 11:46:40Z shaf $
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
