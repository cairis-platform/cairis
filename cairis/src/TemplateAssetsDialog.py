#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/TemplateAssetsDialog.py $ $Id: TemplateAssetsDialog.py 249 2010-05-30 17:07:31Z shaf $
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
