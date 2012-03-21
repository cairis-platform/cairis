#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/VulnerabilitiesDialog.py $ $Id: VulnerabilitiesDialog.py 293 2010-07-11 17:32:06Z shaf $
import wx
import armid
import Vulnerability
import VulnerabilityDialog
from DialogClassParameters import DialogClassParameters
from DirectoryDialog import DirectoryDialog
import DimensionBaseDialog
import ARM

class VulnerabilitiesDialog(DimensionBaseDialog.DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.DimensionBaseDialog.__init__(self,parent,armid.VULNERABILITIES_ID,'Vulnerabilities',(800,300),'vulnerability.png')
    idList = [armid.VULNERABILITIES_VULNERABILITYLIST_ID,armid.VULNERABILITIES_BUTTONADD_ID,armid.VULNERABILITIES_BUTTONDELETE_ID]
    columnList = ['Name','Type']
    self.buildControls(idList,columnList,self.dbProxy.getVulnerabilities,'vulnerability')
    wx.EVT_BUTTON(self,armid.CC_DIRECTORYIMPORT_ID,self.onImport)

    listCtrl = self.FindWindowById(armid.VULNERABILITIES_VULNERABILITYLIST_ID)
    listCtrl.SetColumnWidth(0,300)
    listCtrl.SetColumnWidth(1,200)


  def addObjectRow(self,vulnerabilityListCtrl,listRow,vulnerability):
    vulnerabilityListCtrl.InsertStringItem(listRow,vulnerability.name())
    vulnerabilityListCtrl.SetStringItem(listRow,1,vulnerability.type())


  def onAdd(self,evt):
    try:
      assets = self.dbProxy.getDimensions('asset')
      if (len(assets) == 0):
        dlg = wx.MessageDialog(self,'Cannot add a vulnerability as no assets have been defined','Add vulnerability',wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        return
      addParameters = DialogClassParameters(armid.VULNERABILITY_ID,'Add vulnerability',VulnerabilityDialog.VulnerabilityDialog,armid.VULNERABILITY_BUTTONCOMMIT_ID,self.dbProxy.addVulnerability,True)
      self.addObject(addParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add vulnerability',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onImport(self,evt):
    try:
      assets = self.dbProxy.getDimensions('asset')
      if (len(assets) == 0):
        dlg = wx.MessageDialog(self,'Cannot import a vulnerability as no assets have been defined','Add vulnerability',wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        return
      dirDlg = DirectoryDialog(self,'vulnerability')
      if (dirDlg.ShowModal() == armid.DIRECTORYDIALOG_BUTTONIMPORT_ID):
        objt = dirDlg.object()
        importParameters = DialogClassParameters(armid.VULNERABILITY_ID,'Import vulnerability',VulnerabilityDialog.VulnerabilityDialog,armid.VULNERABILITY_BUTTONCOMMIT_ID,self.dbProxy.addVulnerability,False)
        self.importObject(objt,importParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Import vulnerability',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    try:
      selectedObjt = self.objts[self.selectedLabel]
      updateParameters = DialogClassParameters(armid.VULNERABILITY_ID,'Edit vulnerability',VulnerabilityDialog.VulnerabilityDialog,armid.VULNERABILITY_BUTTONCOMMIT_ID,self.dbProxy.updateVulnerability,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit vulnerability',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No vulnerability','Delete vulnerability',self.dbProxy.deleteVulnerability)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete vulnerability',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy
