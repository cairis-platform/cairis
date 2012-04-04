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
import ARM
from Environment import Environment
from EnvironmentDialog import EnvironmentDialog
from DialogClassParameters import DialogClassParameters
from EnvironmentParameters import EnvironmentParameters
from DimensionBaseDialog import DimensionBaseDialog

class EnvironmentsDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,armid.ENVIRONMENTS_ID,'Environments',(930,300),'environment.png')
    self.rmFrame = parent
    idList = [armid.ENVIRONMENTS_LISTENVIRONMENTS_ID,armid.ENVIRONMENTS_BUTTONADD_ID,armid.ENVIRONMENTS_BUTTONDELETE_ID]
    columnList = ['Name','Description']
    self.buildControls(idList,columnList,self.dbProxy.getEnvironments,'environment')
    listCtrl = self.FindWindowById(armid.ENVIRONMENTS_LISTENVIRONMENTS_ID)
    listCtrl.SetColumnWidth(0,150)
    listCtrl.SetColumnWidth(1,600)

  def addObjectRow(self,environmentListCtrl,listRow,environment):
    environmentListCtrl.InsertStringItem(listRow,environment.name())
    environmentListCtrl.SetStringItem(listRow,1,environment.description())

  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters(armid.ENVIRONMENT_ID,'Add environment',EnvironmentDialog,armid.ENVIRONMENT_BUTTONCOMMIT_ID,self.dbProxy.addEnvironment,True)
      self.addObject(addParameters)
      self.rmFrame.updateEnvironmentSelection(self.selectedLabel)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add environment',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.selectedLabel]
    try:
      updateParameters = DialogClassParameters(armid.ENVIRONMENT_ID,'Edit environment',EnvironmentDialog,armid.ENVIRONMENT_BUTTONCOMMIT_ID,self.dbProxy.updateEnvironment,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit environment',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No environment','Delete environment',self.dbProxy.deleteEnvironment)
      self.rmFrame.updateEnvironmentSelection()
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete environment',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy
