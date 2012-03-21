#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/SecurityPatternsDialog.py $ $Id: SecurityPatternsDialog.py 564 2012-03-12 17:53:00Z shaf $
import wx
import armid
import Asset
from SecurityPatternDialog import SecurityPatternDialog
from DialogClassParameters import DialogClassParameters
import ARM
from DimensionBaseDialog import DimensionBaseDialog

class SecurityPatternsDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,armid.SECURITYPATTERNS_ID,'Security Patterns',(930,300),'countermeasure.png')
    self.theMainWindow = parent
    idList = [armid.SECURITYPATTERNS_PATTERNLIST_ID,armid.SECURITYPATTERNS_BUTTONADD_ID,armid.SECURITYPATTERNS_BUTTONDELETE_ID]
    columnList = ['Name']
    self.buildControls(idList,columnList,self.dbProxy.getSecurityPatterns,'securitypattern')
    listCtrl = self.FindWindowById(armid.SECURITYPATTERNS_PATTERNLIST_ID)
    listCtrl.SetColumnWidth(0,300)


  def addObjectRow(self,listCtrl,listRow,pattern):
    listCtrl.InsertStringItem(listRow,pattern.name())

  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters(armid.SECURITYPATTERN_ID,'Add Security Pattern',SecurityPatternDialog,armid.SECURITYPATTERN_BUTTONCOMMIT_ID,self.dbProxy.addSecurityPattern,True)
      self.addObject(addParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add security pattern',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.selectedLabel]
    assetId = selectedObjt.id()
    try:
      updateParameters = DialogClassParameters(armid.SECURITYPATTERN_ID,'Edit Security Pattern',SecurityPatternDialog,armid.SECURITYPATTERN_BUTTONCOMMIT_ID,self.dbProxy.updateSecurityPattern,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit security pattern',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No security pattern','Delete security pattern',self.dbProxy.deleteSecurityPattern)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete security pattern',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy
