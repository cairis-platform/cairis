#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.


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
