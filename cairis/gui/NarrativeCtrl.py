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
from cairis.core.ARM import *
from cairis.core.Borg import Borg
from CodingTextCtrl import CodingTextCtrl
from SingleGoalDialog import SingleGoalDialog
from SingleObstacleDialog import SingleObstacleDialog
from SingleRequirementDialog import SingleRequirementDialog
from cairis.core.GoalAssociationParameters import GoalAssociationParameters
import cairis.core.RequirementFactory

__author__ = 'Shamal Faily'

class NarrativeCtrl(CodingTextCtrl):
  def __init__(self,parent,winId):
    CodingTextCtrl.__init__(self,parent,winId)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theTaskName = ''
    self.theEnvironmentName = ''

    self.theDimMenu = wx.Menu()
    self.theDimMenu.Append(NARCTRL_MENUGOAL_ID,'Refining Goal')
    self.theDimMenu.Append(NARCTRL_MENUOBSTACLE_ID,'Refining Obstacle')
    self.theDimMenu.Append(NARCTRL_MENUREQUIREMENT_ID,'Refining Requirement')
    self.theDimMenu.AppendMenu(BVNTC_MENU_CODING,'Coding',self.codingMenu)

    self.Bind(wx.EVT_RIGHT_DOWN,self.OnRightDown)
    wx.EVT_MENU(self.theDimMenu,NARCTRL_MENUGOAL_ID,self.onGoal)
    wx.EVT_MENU(self.theDimMenu,NARCTRL_MENUOBSTACLE_ID,self.onObstacle)
    wx.EVT_MENU(self.theDimMenu,NARCTRL_MENUREQUIREMENT_ID,self.onRequirement)
    self.goalItem = self.theDimMenu.FindItemById(NARCTRL_MENUGOAL_ID)
    self.goalItem.Enable(False)
    self.reqItem = self.theDimMenu.FindItemById(NARCTRL_MENUREQUIREMENT_ID)
    self.reqItem.Enable(False)
    self.obsItem = self.theDimMenu.FindItemById(NARCTRL_MENUOBSTACLE_ID)
    self.obsItem.Enable(False)

  def setTask(self,tName):
    self.theTaskName = tName
    if (self.theTaskName != ''):
      self.goalItem.Enable()
      self.reqItem.Enable()
      self.obsItem.Enable()
    else:
      self.goalItem.Enable(False)
      self.reqItem.Enable(False)
      self.obsItem.Enable(False)

  def setEnvironment(self,envName):
    self.theEnvironmentName = envName

  def OnRightDown(self,evt):
    self.enableCodingCtrls()
    self.PopupMenu(self.theDimMenu)

  def onGoal(self,evt):
    try:
      dlg = SingleGoalDialog(self,self.theEnvironmentName)
      if (dlg.ShowModal() == GOAL_BUTTONCOMMIT_ID):
        gp = dlg.parameters()
        self.dbProxy.addGoal(gp)
        gap = GoalAssociationParameters(self.theEnvironmentName,gp.name(),'goal',dlg.theContributionType,self.theTaskName,'task',0,'')
        self.dbProxy.addGoalAssociation(gap)
        ackDlg = wx.MessageDialog(self,'Added goal ' + gp.name(),'Refining goal',wx.OK)
        ackDlg.ShowModal()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Refining goal',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()

  def onObstacle(self,evt):
    try:
      dlg = SingleObstacleDialog(self,self.theEnvironmentName)
      if (dlg.ShowModal() == OBSTACLE_BUTTONCOMMIT_ID):
        op = dlg.parameters()
        self.dbProxy.addObstacle(op)
        gap = GoalAssociationParameters(self.theEnvironmentName,op.name(),'obstacle','and',self.theTaskName,'task',0,'')
        self.dbProxy.addGoalAssociation(gap)
        ackDlg = wx.MessageDialog(self,'Added obstacle ' + op.name(),'Refining goal',wx.OK)
        ackDlg.ShowModal()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Refining obstacle',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()


  def onRequirement(self,evt):
    try:
      taskId = self.dbProxy.getDimensionId(self.theTaskName,'task')
      dlg = SingleRequirementDialog(self)
      if (dlg.ShowModal() == SINGLEREQUIREMENT_BUTTONCOMMIT_ID):
        refName = dlg.referrer()
        completeReqLabel = self.dbProxy.lastRequirementLabel(refName)
        referrer,reqLabel = completeReqLabel.split('-')
        reqId = self.dbProxy.newId()
        reqLabel = int(reqLabel)
        reqLabel += 1
        r = RequirementFactory.build(reqId,reqLabel,dlg.description(),dlg.priority(),dlg.rationale(),dlg.fitCriterion(),dlg.originator(),dlg.type(),refName)
        isAsset = True
        if (dlg.referrerType() == 'environment'):
          isAsset = False
        self.dbProxy.addRequirement(r,refName,isAsset)
        self.dbProxy.addTrace('requirement_task',reqId,taskId)
        completeReqLabel = self.dbProxy.lastRequirementLabel(refName)
        ackDlg = wx.MessageDialog(self,'Added requirement ' + completeReqLabel,'Refining requirement',wx.OK)
        ackDlg.ShowModal()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Refining requirement',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
