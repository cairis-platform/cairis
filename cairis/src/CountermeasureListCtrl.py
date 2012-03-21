#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/CountermeasureListCtrl.py $ $Id: CountermeasureListCtrl.py 527 2011-11-07 11:46:40Z shaf $
import wx
import armid
import AssetParametersFactory
from Borg import Borg
from DimensionNameDialog import DimensionNameDialog
from DependentsDialog import DependentsDialog
from SecurityPatternEnvironmentDialog import SecurityPatternEnvironmentDialog

from ARM import *

class CountermeasureListCtrl(wx.ListCtrl):

  def __init__(self,parent,winId):
    wx.ListCtrl.__init__(self,parent,winId,style=wx.LC_REPORT)
    self.theParentDialog = parent
    self.theTraceMenu = wx.Menu()
    self.theTraceMenu.Append(armid.TRACE_MENUTRACE_GENERATESPECIFIC_ID,'Generate Asset')
    self.theTraceMenu.Append(armid.TRACE_MENUTRACE_GENERATEFROMTEMPLATE_ID,'Generate Asset from template')
    self.theTraceMenu.Append(armid.TRACE_MENUTRACE_GENERATEPATTERN_ID,'Situate Countermeasure Pattern')
    self.theTraceMenu.Append(armid.TRACE_MENUTRACE_ASSOCIATESITUATED_ID,'Associate with situated Countermeasure Pattern')
    self.theTraceMenu.Append(armid.TRACE_MENUTRACE_REMOVEPATTERN_ID,'Remove Countermeasure Pattern')
    self.theRequirementGrid = parent.theMainWindow.requirementGrid()
    wx.EVT_MENU(self,armid.TRACE_MENUTRACE_GENERATESPECIFIC_ID,self.onSelectGenerate)
    wx.EVT_MENU(self,armid.TRACE_MENUTRACE_GENERATEFROMTEMPLATE_ID,self.onSelectGenerateFromTemplate)
    wx.EVT_MENU(self,armid.TRACE_MENUTRACE_GENERATEPATTERN_ID,self.onSelectSituate)
    wx.EVT_MENU(self,armid.TRACE_MENUTRACE_ASSOCIATESITUATED_ID,self.onAssociateSituated)
    wx.EVT_MENU(self,armid.TRACE_MENUTRACE_REMOVEPATTERN_ID,self.onRemovePattern)
    self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onRightClick)


  def onRightClick(self,evt):
    self.PopupMenu(self.theTraceMenu)

  def onSelectGenerate(self,evt):
    countermeasure = self.theParentDialog.objts[self.theParentDialog.selectedLabel]
    cmId = countermeasure.id()
    try:
      b = Borg()
      dbProxy = b.dbProxy
      assetId = dbProxy.addAsset(AssetParametersFactory.build(countermeasure))
      dbProxy.addTrace('countermeasure_asset',cmId,assetId)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Generate countermeasure asset',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onSelectGenerateFromTemplate(self,evt):
    countermeasure = self.theParentDialog.objts[self.theParentDialog.selectedLabel]
    cmId = countermeasure.id()
    try:
      b = Borg()
      dbProxy = b.dbProxy
      templateAssets = dbProxy.getDimensionNames('template_asset')
      cDlg = DimensionNameDialog(self,'template_asset',templateAssets,'Select')
      if (cDlg.ShowModal() == armid.DIMNAME_BUTTONACTION_ID):
        templateAssetName = cDlg.dimensionName()
        assetId = dbProxy.addAsset(AssetParametersFactory.buildFromTemplate(templateAssetName,countermeasure.environments()))
        dbProxy.addTrace('countermeasure_asset',cmId,assetId)
        cDlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Generate countermeasure asset',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onSelectSituate(self,evt):
    countermeasure = self.theParentDialog.objts[self.theParentDialog.selectedLabel]
    cmId = countermeasure.id()
    try:
      b = Borg()
      dbProxy = b.dbProxy
      patterns = dbProxy.getDimensionNames('securitypattern')
      cDlg = DimensionNameDialog(self,'securitypattern',patterns,'Select')
      if (cDlg.ShowModal() == armid.DIMNAME_BUTTONACTION_ID):
        patternName = cDlg.dimensionName()
        patternId = dbProxy.getDimensionId(patternName,'securitypattern')
        spDlg = SecurityPatternEnvironmentDialog(self,patternId,countermeasure.environments())
        if (spDlg.ShowModal() == armid.SPENVIRONMENT_BUTTONCOMMIT_ID):
          self.situatePattern(patternId,spDlg.assetEnvironments())
        spDlg.Destroy()
        dbProxy.addTrace('countermeasure_securitypattern',cmId,patternId)
      cDlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Generate countermeasure asset',wx.OK | wx.ICON_ERROR)
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

  def onRemovePattern(self,evt):
    countermeasure = self.theParentDialog.objts[self.theParentDialog.selectedLabel]
    cmId = countermeasure.id()
    try:
      b = Borg()
      dbProxy = b.dbProxy
      patterns = dbProxy.countermeasurePatterns(cmId)
      cDlg = DimensionNameDialog(self,'securitypattern',patterns,'Select')
      if (cDlg.ShowModal() == armid.DIMNAME_BUTTONACTION_ID):
        patternName = cDlg.dimensionName()
        patternId = dbProxy.getDimensionId(patternName,'securitypattern')
        spDeps = dbProxy.reportDependencies('securitypattern',cmId)
        if (len(spDeps) > 0):
          dlg = DependentsDialog(self,spDeps,'securitypattern')
          retValue = dlg.ShowModal()
          dlg.Destroy()
          if (retValue != armid.DEPENDENTS_BUTTONCONFIRM_ID):
            cDlg.Destroy()
            return
          else:
            dbProxy.deleteDependencies(spDeps)
        dbProxy.deleteSituatedPattern(cmId,patternName)
      cDlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Generate countermeasure asset',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onAssociateSituated(self,evt):
    countermeasure = self.theParentDialog.objts[self.theParentDialog.selectedLabel]
    cmId = countermeasure.id()
    try:
      b = Borg()
      dbProxy = b.dbProxy
      patterns = dbProxy.candidateCountermeasurePatterns(cmId)
      cDlg = DimensionNameDialog(self,'securitypattern',patterns,'Select')
      if (cDlg.ShowModal() == armid.DIMNAME_BUTTONACTION_ID):
        patternName = cDlg.dimensionName()
        dbProxy.associateCountermeasureToPattern(cmId,patternName)
      cDlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Generate countermeasure asset',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return
