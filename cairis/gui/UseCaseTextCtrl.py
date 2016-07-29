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
from SingleGoalDialog import SingleGoalDialog
from cairis.core.GoalAssociationParameters import GoalAssociationParameters
from SingleRequirementDialog import SingleRequirementDialog
import cairis.core.RequirementFactory

__author__ = 'Shamal Faily'

class UseCaseTextCtrl(wx.TextCtrl):
  def __init__(self,parent,winId):
    wx.TextCtrl.__init__(self,parent,winId,'',style=wx.TE_MULTILINE)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theUseCaseName = ''
    self.theEnvironmentName = ''

    self.theDimMenu = wx.Menu()
    self.theDimMenu.Append(UCTCTRL_MENUGOAL_ID,'Refining Goal')
    self.theDimMenu.Append(UCTCTRL_MENUREQUIREMENT_ID,'Refining Requirement')
    self.Bind(wx.EVT_RIGHT_DOWN,self.OnRightDown)
    wx.EVT_MENU(self.theDimMenu,UCTCTRL_MENUGOAL_ID,self.onGoal)
    wx.EVT_MENU(self.theDimMenu,UCTCTRL_MENUREQUIREMENT_ID,self.onRequirement)
    self.goalItem = self.theDimMenu.FindItemById(UCTCTRL_MENUGOAL_ID)
    self.goalItem.Enable(False)
    self.reqItem = self.theDimMenu.FindItemById(UCTCTRL_MENUREQUIREMENT_ID)
    self.reqItem.Enable(False)

  def setUseCase(self,ucName):
    self.theUseCaseName = ucName
    if (self.theUseCaseName != ''):
      self.goalItem.Enable()
      self.reqItem.Enable()
    else:
      self.goalItem.Enable(False)
      self.reqItem.Enable(False)

  def setEnvironment(self,envName):
    self.theEnvironmentName = envName

  def OnRightDown(self,evt):
    self.PopupMenu(self.theDimMenu)

  def onGoal(self,evt):
    try:
      dlg = SingleGoalDialog(self,self.theEnvironmentName)
      if (dlg.ShowModal() == GOAL_BUTTONCOMMIT_ID):
        gp = dlg.parameters()
        self.dbProxy.addGoal(gp)
        gap = GoalAssociationParameters(self.theEnvironmentName,gp.name(),'goal','and',self.theUseCaseName,'usecase',0,'')
        self.dbProxy.addGoalAssociation(gap)
        ackDlg = wx.MessageDialog(self,'Added goal ' + gp.name(),'Refining goal',wx.OK)
        ackDlg.ShowModal()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Refining goal',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()

  def onRequirement(self,evt):
    try:
      ucId = self.dbProxy.getDimensionId(self.theUseCaseName,'usecase')
      dlg = SingleRequirementDialog(self)
      if (dlg.ShowModal() == SINGLEREQUIREMENT_BUTTONCOMMIT_ID):
        refName = dlg.referrer()
        completeReqLabel = self.dbProxy.lastRequirementLabel(refName)
        referrer,reqLabel = completeReqLabel.split('-')
        reqId = self.dbProxy.newId()
        reqLabel = int(reqLabel)
        reqLabel += 1
        r = cairis.core.RequirementFactory.build(reqId,reqLabel,dlg.description(),dlg.priority(),dlg.rationale(),dlg.fitCriterion(),dlg.originator(),dlg.type(),refName)
        isAsset = True
        if (dlg.referrerType() == 'environment'):
          isAsset = False
        self.dbProxy.addRequirement(r,refName,isAsset)
        self.dbProxy.addTrace('requirement_usecase',reqId,ucId,dlg.theContributionType)
        completeReqLabel = self.dbProxy.lastRequirementLabel(refName)
        ackDlg = wx.MessageDialog(self,'Added requirement ' + completeReqLabel,'Refining requirement',wx.OK)
        ackDlg.ShowModal()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Refining requirement',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
