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
import cairis.core.PersonaCharacteristic
from PersonaCharacteristicDialog import PersonaCharacteristicDialog
from PersonaCharacteristicDialogParameters import PersonaCharacteristicDialogParameters
from TaskCharacteristicDialog import TaskCharacteristicDialog
from TaskCharacteristicDialogParameters import TaskCharacteristicDialogParameters
from cairis.core.ARM import *
from DimensionBaseDialog import DimensionBaseDialog
from cairis.core.Borg import Borg

__author__ = 'Shamal Faily'

class BehaviouralCharacteristicsDialog(DimensionBaseDialog):
  def __init__(self,parent,aName,bvName = ''):
    b = Borg()
    self.dbProxy = b.dbProxy
    windowLabel = 'Persona Characteristics'
    windowIcon = 'persona.png'
    getFn = self.dbProxy.getPersonaBehaviouralCharacteristics
    if (bvName == ''):
      windowLabel = 'Task Characteristics'
      windowIcon = 'task.png'
      getFn = self.dbProxy.getTaskSpecificCharacteristics
    DimensionBaseDialog.__init__(self,parent,PERSONACHARACTERISTICS_ID,windowLabel,(930,300),windowIcon)
    self.theMainWindow = parent
    self.theName = aName
    self.theBehaviouralVariable = bvName
    idList = [PERSONACHARACTERISTICS_CHARLIST_ID,PERSONACHARACTERISTICS_BUTTONADD_ID,PERSONACHARACTERISTICS_BUTTONDELETE_ID]
    columnList = ['Characteristic']
    self.buildControls(idList,columnList,getFn,'behavioural_characteristic')
    listCtrl = self.FindWindowById(PERSONACHARACTERISTICS_CHARLIST_ID)
    listCtrl.SetColumnWidth(0,700)


  def addObjectRow(self,listCtrl,listRow,objt):
    listCtrl.InsertStringItem(listRow,objt.characteristic())

  def onAdd(self,evt):
    try:
      if (self.theBehaviouralVariable != ''):
        addParameters = PersonaCharacteristicDialogParameters(PERSONACHARACTERISTIC_ID,'Add Persona Characteristic',PersonaCharacteristicDialog,PERSONACHARACTERISTIC_BUTTONCOMMIT_ID,self.dbProxy.addPersonaCharacteristic,True,self.theName,self.theBehaviouralVariable)
      else:
        addParameters = TaskCharacteristicDialogParameters(TASKCHARACTERISTIC_ID,'Add Task Characteristic',TaskCharacteristicDialog,TASKCHARACTERISTIC_BUTTONCOMMIT_ID,self.dbProxy.addTaskCharacteristic,True,self.theName,False)
      self.addObject(addParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add characteristic',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.deprecatedLabel()]
    objtId = selectedObjt.id()
    try:
      if (self.theBehaviouralVariable != ''):
        updateParameters = PersonaCharacteristicDialogParameters(PERSONACHARACTERISTIC_ID,'Edit Persona Characteristic',PersonaCharacteristicDialog,PERSONACHARACTERISTIC_BUTTONCOMMIT_ID,self.dbProxy.updatePersonaCharacteristic,False,self.theName,self.theBehaviouralVariable)
      else:
        updateParameters = TaskCharacteristicDialogParameters(TASKCHARACTERISTIC_ID,'Edit Task Characteristic',TaskCharacteristicDialog,TASKCHARACTERISTIC_BUTTONCOMMIT_ID,self.dbProxy.updateTaskCharacteristic,False,self.theName,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit characteristic',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      if (self.theBehaviouralVariable != ''):
        self.deleteObject('No persona characteristic','Delete persona characteristic',self.dbProxy.deletePersonaCharacteristic)
      else:
        self.deleteObject('No task characteristic','Delete task characteristic',self.dbProxy.deleteTaskCharacteristic)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete task characteristic',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy


  def deprecatedLabel(self):
    listCtrl = self.FindWindowById(PERSONACHARACTERISTICS_CHARLIST_ID)
    charItem = listCtrl.GetItem(listCtrl.theSelectedIdx,0)
    charTxt = charItem.GetText()
    if (self.theBehaviouralVariable != ''):
      pcLabel = self.theName + '/' + self.theBehaviouralVariable + '/' + charTxt
    else:
      pcLabel = self.theName + '/' + charTxt
    return pcLabel
