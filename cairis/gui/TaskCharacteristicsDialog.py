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
from cairis.core.armid import *
import cairis.core.TaskCharacteristic
from TaskCharacteristicDialog import TaskCharacteristicDialog
from DialogClassParameters import DialogClassParameters
from TaskCharacteristicDialogParameters import TaskCharacteristicDialogParameters
from cairis.core.ARM import *
from DimensionBaseDialog import DimensionBaseDialog

class TaskCharacteristicsDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,TASKCHARACTERISTICS_ID,'Task Characteristics',(930,300),'task.png')
    self.theMainWindow = parent
    idList = [TASKCHARACTERISTICS_CHARLIST_ID,TASKCHARACTERISTICS_BUTTONADD_ID,TASKCHARACTERISTICS_BUTTONDELETE_ID]
    columnList = ['Task','Characteristic']
    self.buildControls(idList,columnList,self.dbProxy.getTaskCharacteristics,'task_characteristic')
    listCtrl = self.FindWindowById(TASKCHARACTERISTICS_CHARLIST_ID)
    listCtrl.SetColumnWidth(0,100)
    listCtrl.SetColumnWidth(1,700)


  def addObjectRow(self,listCtrl,listRow,objt):
    listCtrl.InsertStringItem(listRow,objt.task())
    listCtrl.SetStringItem(listRow,1,objt.characteristic())

  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters(TASKCHARACTERISTIC_ID,'Add Task Characteristic',TaskCharacteristicDialog,TASKCHARACTERISTIC_BUTTONCOMMIT_ID,self.dbProxy.addTaskCharacteristic,True)
      self.addObject(addParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add task characteristic',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.deprecatedLabel()]
    objtId = selectedObjt.id()
    try:
      updateParameters = TaskCharacteristicDialogParameters(TASKCHARACTERISTIC_ID,'Edit Task Characteristic',TaskCharacteristicDialog,TASKCHARACTERISTIC_BUTTONCOMMIT_ID,self.dbProxy.updateTaskCharacteristic,False,selectedObjt.task())
      self.updateObject(selectedObjt,updateParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit task characteristic',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No task characteristic','Delete task characteristic',self.dbProxy.deleteTaskCharacteristic)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete task characteristic',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def deprecatedLabel(self):
    listCtrl = self.FindWindowById(TASKCHARACTERISTICS_CHARLIST_ID)
    pItem = listCtrl.GetItem(self.selectedIdx,0)
    pTxt = pItem.GetText()
    charItem = listCtrl.GetItem(self.selectedIdx,1)
    charTxt = charItem.GetText()
    pcLabel = pTxt + '/' + charTxt
    return pcLabel
