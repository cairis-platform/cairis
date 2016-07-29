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
import cairis.core.Goal
from GoalDialog import GoalDialog
from DialogClassParameters import DialogClassParameters
from cairis.core.ARM import *
from DimensionBaseDialog import DimensionBaseDialog

__author__ = 'Shamal Faily'

class GoalsDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,GOALS_ID,'Goals',(930,300),'goal.png')
    self.theMainWindow = parent
    idList = [GOALS_GOALLIST_ID,GOALS_BUTTONADD_ID,GOALS_BUTTONDELETE_ID]
    columnList = ['Name','Originator','Status']
    self.buildControls(idList,columnList,self.dbProxy.getColouredGoals,'goal')
    listCtrl = self.FindWindowById(GOALS_GOALLIST_ID)
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
      addParameters = DialogClassParameters(GOAL_ID,'Add goal',GoalDialog,GOAL_BUTTONCOMMIT_ID,self.dbProxy.addGoal,True)
      self.addObject(addParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add goal',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.selectedLabel]
    try:
      updateParameters = DialogClassParameters(GOAL_ID,'Edit goal',GoalDialog,GOAL_BUTTONCOMMIT_ID,self.dbProxy.updateGoal,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit goal',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No goal','Delete goal',self.dbProxy.deleteGoal)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete goal',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy
