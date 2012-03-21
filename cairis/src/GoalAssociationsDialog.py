#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/GoalAssociationsDialog.py $ $Id: GoalAssociationsDialog.py 421 2011-01-30 13:30:15Z shaf $
import wx
import armid
import GoalAssociation
from GoalAssociationDialog import GoalAssociationDialog
from DialogClassParameters import DialogClassParameters
import ARM
from DimensionBaseDialog import DimensionBaseDialog

class GoalAssociationsDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,armid.GOALASSOCIATIONS_ID,'GoalAssociations',(930,300),'goalassociations.png')
    idList = [armid.GOALASSOCIATIONS_GOALASSOCIATIONLIST_ID,armid.GOALASSOCIATIONS_BUTTONADD_ID,armid.GOALASSOCIATIONS_BUTTONDELETE_ID]
    columnList = ['Environment/Head/Tail','Type','Alternative','Rationale']
    self.buildControls(idList,columnList,self.dbProxy.getGoalAssociations,'goalassociation')
    listCtrl = self.FindWindowById(armid.GOALASSOCIATIONS_GOALASSOCIATIONLIST_ID)
    listCtrl.SetColumnWidth(0,300)
    listCtrl.SetColumnWidth(1,100)
    listCtrl.SetColumnWidth(2,100)
    listCtrl.SetColumnWidth(3,500)


  def addObjectRow(self,listCtrl,listRow,association):
    label = association.environment() + '/' + association.goal() + '/' + association.subGoal() + '/' + association.type()
    listCtrl.InsertStringItem(listRow,label)
    listCtrl.SetStringItem(listRow,1,association.type())
    alternativeString = 'No'
    if (association.alternative() == True):
      alternativeString = 'Yes'
    listCtrl.SetStringItem(listRow,2,alternativeString)
    listCtrl.SetStringItem(listRow,3,association.rationale())

  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters(armid.GOALASSOCIATION_ID,'Add goal association',GoalAssociationDialog,armid.GOALASSOCIATION_BUTTONCOMMIT_ID,self.dbProxy.addGoalAssociation,True)
      self.addObject(addParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add goal association',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.selectedLabel]
    goalId = selectedObjt.id()
    try:
      updateParameters = DialogClassParameters(armid.GOALASSOCIATION_ID,'Edit goal association',GoalAssociationDialog,armid.GOALASSOCIATION_BUTTONCOMMIT_ID,self.dbProxy.updateGoalAssociation,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit goal association',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No goal association','Delete goal association',self.dbProxy.deleteGoalAssociation)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete goal association',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy
