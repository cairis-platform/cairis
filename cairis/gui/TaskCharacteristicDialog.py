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
from PersonaCharacteristicNotebook import PersonaCharacteristicNotebook
from cairis.core.TaskCharacteristicParameters import TaskCharacteristicParameters
import WidgetFactory

class TaskCharacteristicDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,parameters.id(),parameters.label(),style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(700,300))
    self.theTaskName = ''
    self.theModalQualifier = ''
    self.theCharacteristic = ''
    self.theGrounds = []
    self.theWarrant = []
    self.theBacking = []
    self.theRebuttal = []
    self.isCreate = True
    self.showTaskCombo = True

    self.theId = -1
    self.panel = 0
    self.inTask = False
    if (parameters.__class__.__name__ == 'TaskCharacteristicDialogParameters'):
      self.inTask = True
      self.showTaskCombo = parameters.showTask()

    if (self.inTask):
      self.theTaskName = parameters.task()

    self.commitVerb = 'Add'
    
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = PersonaCharacteristicNotebook(self,True,self.showTaskCombo)
    mainSizer.Add(self.panel,1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildCommitButtonSizer(self,TASKCHARACTERISTIC_BUTTONCOMMIT_ID,True),0,wx.CENTER)

    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,TASKCHARACTERISTIC_BUTTONCOMMIT_ID,self.onCommit)

  def load(self,objt):
    self.theId = objt.id()
    buttonCtrl = self.FindWindowById(TASKCHARACTERISTIC_BUTTONCOMMIT_ID)
    buttonCtrl.SetLabel('Edit')
    self.panel.loadControls(objt)

    if (self.inTask and self.showTaskCombo):
      pCtrl = self.FindWindowById(TASKCHARACTERISTIC_COMBOTASK_ID)
      pCtrl.SetValue(objt.task())

    self.commitVerb = 'Edit'

  def onCommit(self,evt):
    commitLabel = self.commitVerb + ' task characteristic'

    qualCtrl = self.FindWindowById(PERSONACHARACTERISTIC_TEXTQUALIFIER_ID)
    charCtrl = self.FindWindowById(PERSONACHARACTERISTIC_TEXTCHARACTERISTIC_ID)
    groundsCtrl = self.FindWindowById(PERSONACHARACTERISTIC_LISTGROUNDS_ID)
    warrantCtrl = self.FindWindowById(PERSONACHARACTERISTIC_LISTWARRANT_ID)
    rebuttalCtrl = self.FindWindowById(PERSONACHARACTERISTIC_LISTREBUTTAL_ID)

    self.theModalQualifier = qualCtrl.GetValue()
    self.theCharacteristic = charCtrl.GetValue()
    self.theGrounds = groundsCtrl.dimensions()
    self.theWarrant = warrantCtrl.dimensions()
    self.theRebuttal = rebuttalCtrl.dimensions()
 
    
    if (self.inTask == False):
      pCtrl = self.FindWindowById(TASKCHARACTERISTIC_COMBOTASK_ID)
      self.theTaskName = pCtrl.GetValue()

    if len(self.theTaskName) == 0:
      dlg = wx.MessageDialog(self,'Task cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theModalQualifier) == 0:
      dlg = wx.MessageDialog(self,'Model Qualifier cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theCharacteristic) == 0:
      dlg = wx.MessageDialog(self,'Characteristic cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theGrounds) == 0:
      dlg = wx.MessageDialog(self,'Some grounds for this characteristic must be provided',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(TASKCHARACTERISTIC_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = TaskCharacteristicParameters(self.theTaskName,self.theModalQualifier,self.theCharacteristic,self.theGrounds,self.theWarrant,[],self.theRebuttal)
    parameters.setId(self.theId)
    return parameters
