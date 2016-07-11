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
import cairis.core.Asset
from TemplateRequirementDialog import TemplateRequirementDialog
from DialogClassParameters import DialogClassParameters
from cairis.core.ARM import *
from DimensionBaseDialog import DimensionBaseDialog

class TemplateRequirementsDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,TEMPLATEREQUIREMENTS_ID,'Template Requirements',(930,300),'requirement.png')
    self.rmFrame = parent
    idList = [TEMPLATEREQUIREMENTS_REQUIREMENTLIST_ID,TEMPLATEREQUIREMENTS_BUTTONADD_ID,TEMPLATEREQUIREMENTS_BUTTONDELETE_ID]
    columnList = ['Name','Type']
    self.buildControls(idList,columnList,self.dbProxy.getTemplateRequirements,'template_requirement')
    listCtrl = self.FindWindowById(TEMPLATEREQUIREMENTS_REQUIREMENTLIST_ID)
    listCtrl.SetColumnWidth(0,150)
    listCtrl.SetColumnWidth(1,150)


  def addObjectRow(self,listCtrl,listRow,objt):
    listCtrl.InsertStringItem(listRow,objt.name())
    listCtrl.SetStringItem(listRow,1,objt.type())

  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters(TEMPLATEREQUIREMENT_ID,'Add template requirement',TemplateRequirementDialog,TEMPLATEREQUIREMENT_BUTTONCOMMIT_ID,self.dbProxy.addTemplateRequirement,True)
      self.addObject(addParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add template requirement',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.selectedLabel]
    assetId = selectedObjt.id()
    try:
      updateParameters = DialogClassParameters(TEMPLATEREQUIREMENT_ID,'Edit template requirement',TemplateRequirementDialog,TEMPLATEREQUIREMENT_BUTTONCOMMIT_ID,self.dbProxy.updateTemplateRequirement,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit template requirement',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No template requirement','Delete template requirement',self.dbProxy.deleteTemplateRequirement)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete template requirement',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy
