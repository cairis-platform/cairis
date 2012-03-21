#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/RisksDialog.py $ $Id: RisksDialog.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
import Risk
from RiskDialog import RiskDialog
from DialogClassParameters import DialogClassParameters
from DimensionBaseDialog import DimensionBaseDialog
import ARM

class RisksDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,armid.RISKS_ID,'Risks',(800,300),'risk.png')
    idList = [armid.RISKS_LISTRISKS_ID,armid.RISKS_BUTTONADD_ID,armid.RISKS_BUTTONDELETE_ID]
    columnList = ['Name']
    self.buildControls(idList,columnList,self.dbProxy.getRisks,'risk')
    listCtrl = self.FindWindowById(armid.RISKS_LISTRISKS_ID)
    listCtrl.SetColumnWidth(0,600)


  def addObjectRow(self,riskListCtrl,listRow,risk):
    riskListCtrl = self.FindWindowById(armid.RISKS_LISTRISKS_ID)
    riskListCtrl.InsertStringItem(listRow,risk.name())

  def onAdd(self,evt):
    try:
      threats = self.dbProxy.getDimensions('threat')
      vulnerabilities = self.dbProxy.getDimensions('vulnerability')
      if (len(threats) == 0):
        dlg = wx.MessageDialog(self,'Cannot add a risk as no threats have been defined','Add risk',wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        return
      elif (len(vulnerabilities) == 0):
        dlg = wx.MessageDialog(self,'Cannot add a risk as no vulnerabilities have been defined','Add risk',wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        return
      addParameters = DialogClassParameters(armid.RISK_ID,'Add risk',RiskDialog,armid.RISK_BUTTONCOMMIT_ID,self.dbProxy.addRisk,True)
      self.addObject(addParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add risk',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()

  def onUpdate(self,evt):
    try:
      selectedObjt = self.objts[self.selectedLabel]
      updateParameters = DialogClassParameters(armid.VULNERABILITY_ID,'Edit risk',RiskDialog,armid.RISK_BUTTONCOMMIT_ID,self.dbProxy.updateRisk,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit risk',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No risk','Delete risk',self.dbProxy.deleteRisk)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete risk',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy
