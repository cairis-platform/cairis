#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/GoalsDialog.py $ $Id: GoalsDialog.py 406 2011-01-13 00:25:07Z shaf $
import wx
import armid
import Goal
from GoalDialog import GoalDialog
from DialogClassParameters import DialogClassParameters
import ARM
from DimensionBaseDialog import DimensionBaseDialog

class GoalsDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,armid.GOALS_ID,'Goals',(930,300),'goal.png')
    self.theMainWindow = parent
    idList = [armid.GOALS_GOALLIST_ID,armid.GOALS_BUTTONADD_ID,armid.GOALS_BUTTONDELETE_ID]
    columnList = ['Name','Originator','Status']
    self.buildControls(idList,columnList,self.dbProxy.getColouredGoals,'goal')
    listCtrl = self.FindWindowById(armid.GOALS_GOALLIST_ID)
    listCtrl.SetColumnWidth(0,300)


  def addObjectRow(self,listCtrl,listRow,goal):
    listCtrl.InsertStringItem(listRow,goal.name())
    listCtrl.SetStringItem(listRow,1,goal.originator())
    if (goal.colour() == 'black'):
      listCtrl.SetStringItem(listRow,2,'Check')
    elif (goal.colour() == 'red'):
      listCtrl.SetStringItem(listRow,2,'To refine')
    else: 
      listCtrl.SetStringItem(listRow,2,'OK')

  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters(armid.GOAL_ID,'Add goal',GoalDialog,armid.GOAL_BUTTONCOMMIT_ID,self.dbProxy.addGoal,True)
      self.addObject(addParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add goal',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.selectedLabel]
    try:
      updateParameters = DialogClassParameters(armid.GOAL_ID,'Edit goal',GoalDialog,armid.GOAL_BUTTONCOMMIT_ID,self.dbProxy.updateGoal,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit goal',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No goal','Delete goal',self.dbProxy.deleteGoal)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete goal',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy
