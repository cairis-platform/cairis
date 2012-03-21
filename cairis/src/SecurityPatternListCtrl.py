#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/SecurityPatternListCtrl.py $ $Id: SecurityPatternListCtrl.py 527 2011-11-07 11:46:40Z shaf $
import wx
import armid
from Borg import Borg
from SecurityPatternEnvironmentDialog import SecurityPatternEnvironmentDialog
import AssetParametersFactory
from ARM import *

class SecurityPatternListCtrl(wx.ListCtrl):

  def __init__(self,parent,winId):
    wx.ListCtrl.__init__(self,parent,winId,style=wx.LC_REPORT)
    self.theParentDialog = parent
    self.theTraceMenu = wx.Menu()
    self.theTraceMenu.Append(armid.TRACE_MENUTRACE_GENERATESPECIFIC_ID,'Situate pattern')
    wx.EVT_MENU(self,armid.TRACE_MENUTRACE_GENERATESPECIFIC_ID,self.onSituate)
    self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onRightClick)


  def onRightClick(self,evt):
    self.PopupMenu(self.theTraceMenu)

  def onSituate(self,evt):
    spObjt = self.theParentDialog.objts[self.theParentDialog.selectedLabel]
    patternId = spObjt.id()
    try:
      dlg = SecurityPatternEnvironmentDialog(self,patternId)
      if (dlg.ShowModal() == armid.SPENVIRONMENT_BUTTONCOMMIT_ID):
        self.situatePattern(patternId,dlg.assetEnvironments())
      dlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Situate security pattern',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def situatePattern(self,patternId,assetEnvs):
    assetParametersList = []
    for assetName,envs in assetEnvs.iteritems():
      assetParametersList.append(AssetParametersFactory.buildFromTemplate(assetName,envs))
    b = Borg()
    b.dbProxy.addSituatedAssets(patternId,assetParametersList)
    self.theParentDialog.theMainWindow.updateObjectSelection()
