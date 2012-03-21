#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/TemplateAssetListCtrl.py $ $Id: TemplateAssetListCtrl.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
import AssetParametersFactory
from Borg import Borg
from DimensionNameDialog import DimensionNameDialog

from ARM import *

class TemplateAssetListCtrl(wx.ListCtrl):

  def __init__(self,parent,winId):
    wx.ListCtrl.__init__(self,parent,winId,style=wx.LC_REPORT)
    self.theParentDialog = parent
    self.theTraceMenu = wx.Menu()
    self.theTraceMenu.Append(armid.TRACE_MENUTRACE_GENERATESPECIFIC_ID,'Situate')
    self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onRightClick)
    wx.EVT_MENU(self,armid.TRACE_MENUTRACE_GENERATESPECIFIC_ID,self.onSituate)


  def onRightClick(self,evt):
    self.PopupMenu(self.theTraceMenu)

  def onSituate(self,evt):
    tAsset = self.theParentDialog.objts[self.theParentDialog.selectedLabel]
    taId = tAsset.id()
    taName = tAsset.name()
    try:
      b = Borg()
      dbProxy = b.dbProxy
      envs = dbProxy.getEnvironmentNames()
      cDlg = DimensionNameDialog(self,'environment',envs,'Select')
      if (cDlg.ShowModal() == armid.DIMNAME_BUTTONACTION_ID):
        sitEnvs = cDlg.dimensionNames()
        assetId = dbProxy.addAsset(AssetParametersFactory.buildFromTemplate(taName,sitEnvs))
# NB: we don't add anything to asset_template_asset, as we only use this table when the derived asset is part of a situated pattern
        cDlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Situate template asset',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return
