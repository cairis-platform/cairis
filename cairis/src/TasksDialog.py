#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/TasksDialog.py $ $Id: TasksDialog.py 524 2011-11-04 20:40:47Z shaf $
import wx
import armid
from TaskDialog import TaskDialog
import ARM
from DimensionBaseDialog import DimensionBaseDialog
from TaskDialogParameters import TaskDialogParameters

class TasksDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,armid.TASKS_ID,'Tasks',(400,350),'task.png')
    idList = [armid.TASKS_TASKLIST_ID,armid.TASKS_BUTTONADD_ID,armid.TASKS_BUTTONDELETE_ID]
    columnList = ['Name']
    self.buildControls(idList,columnList,self.dbProxy.getTasks,'task')
    listCtrl = self.FindWindowById(armid.TASKS_TASKLIST_ID)
    listCtrl.SetColumnWidth(0,300)


  def addObjectRow(self,taskListCtrl,listRow,task):
    taskListCtrl.InsertStringItem(listRow,task.name())

  def onAdd(self,evt):
    try:
      addLabel = 'Add Task' 
      addParameters = TaskDialogParameters(armid.TASK_ID,addLabel,TaskDialog,armid.TASK_BUTTONCOMMIT_ID,self.dbProxy.addTask,True,self.dbProxy)
      self.addObject(addParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add Task',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.selectedLabel]
    updateLabel = 'Edit Task'
    try:
      updateParameters = TaskDialogParameters(armid.TASK_ID,updateLabel,TaskDialog,armid.TASK_BUTTONCOMMIT_ID,self.dbProxy.updateTask,False,self.dbProxy)
      self.updateObject(selectedObjt,updateParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),updateLabel,wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onDelete(self,evt):
    try:
      self.deleteObject('No task','Delete task',self.dbProxy.deleteTask)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete Task',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return
