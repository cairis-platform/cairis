#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ThreatsDialog.py $ $Id: ThreatsDialog.py 293 2010-07-11 17:32:06Z shaf $
import wx
import armid
from ThreatDialog import ThreatDialog
from DialogClassParameters import DialogClassParameters
from DirectoryDialog import DirectoryDialog
import DimensionBaseDialog
import ARM

class ThreatsDialog(DimensionBaseDialog.DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.DimensionBaseDialog.__init__(self,parent,armid.THREATS_ID,'Threats',(800,300),'threat.png')
    idList = [armid.THREATS_THREATLIST_ID,armid.THREATS_BUTTONADD_ID,armid.THREATS_BUTTONDELETE_ID]
    columnList = ['Name','Type']
    self.buildControls(idList,columnList,self.dbProxy.getThreats,'threat')
    wx.EVT_BUTTON(self,armid.CC_DIRECTORYIMPORT_ID,self.onImport)
    listCtrl = self.FindWindowById(armid.THREATS_THREATLIST_ID)
    listCtrl.SetColumnWidth(0,300)
    listCtrl.SetColumnWidth(1,300)


  def addObjectRow(self,threatListCtrl,listRow,threat):
    threatListCtrl.InsertStringItem(listRow,threat.name())
    threatListCtrl.SetStringItem(listRow,1,threat.type())

  def onAdd(self,evt):
    try:
      attackers = self.dbProxy.getDimensions('attacker')
      assets = self.dbProxy.getDimensions('asset')
      if (len(attackers) == 0):
        dlg = wx.MessageDialog(self,'Cannot add a threat as no attackers have been defined','Add threat',wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        return
      elif (len(assets) == 0):
        dlg = wx.MessageDialog(self,'Cannot add a threat as no assets have been defined','Add threat',wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        return
      addParameters = DialogClassParameters(armid.THREAT_ID,'Add threat',ThreatDialog,armid.THREAT_BUTTONCOMMIT_ID,self.dbProxy.addThreat,True)
      self.addObject(addParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add threat',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onImport(self,evt):
    try:
      assets = self.dbProxy.getDimensions('asset')
      if (len(assets) == 0):
        dlg = wx.MessageDialog(self,'Cannot import a threat as no assets have been defined','Add threat',wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        return
      dirDlg = DirectoryDialog(self,'threat')
      if (dirDlg.ShowModal() == armid.DIRECTORYDIALOG_BUTTONIMPORT_ID):
        objt = dirDlg.object()
        importParameters = DialogClassParameters(armid.THREAT_ID,'Import threat',ThreatDialog,armid.THREAT_BUTTONCOMMIT_ID,self.dbProxy.addThreat,False)
        self.importObject(objt,importParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Import threat',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    try:
      selectedObjt = self.objts[self.selectedLabel]
      updateParameters = DialogClassParameters(armid.THREAT_ID,'Edit threat',ThreatDialog,armid.THREAT_BUTTONCOMMIT_ID,self.dbProxy.updateThreat,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Update threat',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No threat','Delete threat',self.dbProxy.deleteThreat)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete threat',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy
