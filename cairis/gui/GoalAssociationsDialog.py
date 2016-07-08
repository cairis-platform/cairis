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
import cairis.core.GoalAssociation
from GoalAssociationDialog import GoalAssociationDialog
from DialogClassParameters import DialogClassParameters
from cairis.core.ARM import *
from DimensionBaseDialog import DimensionBaseDialog

class GoalAssociationsDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,GOALASSOCIATIONS_ID,'GoalAssociations',(930,300),'goalassociations.png')
    idList = [GOALASSOCIATIONS_GOALASSOCIATIONLIST_ID,GOALASSOCIATIONS_BUTTONADD_ID,GOALASSOCIATIONS_BUTTONDELETE_ID]
    columnList = ['Environment/Head/Tail','Type','Alternative','Rationale']
    self.buildControls(idList,columnList,self.dbProxy.getGoalAssociations,'goalassociation')
    listCtrl = self.FindWindowById(GOALASSOCIATIONS_GOALASSOCIATIONLIST_ID)
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
      addParameters = DialogClassParameters(GOALASSOCIATION_ID,'Add goal association',GoalAssociationDialog,GOALASSOCIATION_BUTTONCOMMIT_ID,self.dbProxy.addGoalAssociation,True)
      self.addObject(addParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add goal association',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.selectedLabel]
    goalId = selectedObjt.id()
    try:
      updateParameters = DialogClassParameters(GOALASSOCIATION_ID,'Edit goal association',GoalAssociationDialog,GOALASSOCIATION_BUTTONCOMMIT_ID,self.dbProxy.updateGoalAssociation,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit goal association',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No goal association','Delete goal association',self.dbProxy.deleteGoalAssociation)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete goal association',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy
