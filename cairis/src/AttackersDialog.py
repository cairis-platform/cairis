#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/AttackersDialog.py $ $Id: AttackersDialog.py 330 2010-10-31 15:01:28Z shaf $
import wx
import armid
from AttackerDialog import AttackerDialog
from DialogClassParameters import DialogClassParameters
from DimensionBaseDialog import DimensionBaseDialog
import ARM

class AttackersDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,armid.ATTACKERS_ID,'Attackers',(800,300),'attacker.png')
    idList = [armid.ATTACKERS_ATTACKERLIST_ID,armid.ATTACKERS_BUTTONADD_ID,armid.ATTACKERS_BUTTONDELETE_ID]
    columnList = ['Name','Description']
    self.buildControls(idList,columnList,self.dbProxy.getAttackers,'attacker')
    listCtrl = self.FindWindowById(armid.ATTACKERS_ATTACKERLIST_ID)
    listCtrl.SetColumnWidth(0,150)
    listCtrl.SetColumnWidth(1,600)
    
  def addObjectRow(self,attackerListCtrl,listRow,attacker):
    attackerListCtrl.InsertStringItem(listRow,attacker.name())
    attackerListCtrl.SetStringItem(listRow,1,attacker.description())

  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters(armid.ATTACKER_ID,'Add attacker',AttackerDialog,armid.ATTACKER_BUTTONCOMMIT_ID,self.dbProxy.addAttacker,creationFlag=True)
      self.addObject(addParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add attacker',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.selectedLabel]
    try:
      updateParameters = DialogClassParameters(armid.ATTACKER_ID,'Edit attacker',AttackerDialog,armid.ATTACKER_BUTTONCOMMIT_ID,self.dbProxy.updateAttacker,creationFlag=False)
      self.updateObject(selectedObjt,updateParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit attacker',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onDelete(self,evt):
    try:
      self.deleteObject('No attacker','Delete attacker',self.dbProxy.deleteAttacker)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete attacker',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return
