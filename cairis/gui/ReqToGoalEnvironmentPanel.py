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
from cairis.core.Borg import Borg
from cairis.core.GoalEnvironmentProperties import GoalEnvironmentProperties
from ReqToGoalNotebook import ReqToGoalNotebook
from EnvironmentListCtrl import EnvironmentListCtrl

__author__ = 'Shamal Faily'

class ReqToGoalEnvironmentPanel(wx.Panel):
  def __init__(self,parent,goalDef,goalCat,goalPri,goalFc,goalIssue,goalAssets,defaultEnv):
    wx.Panel.__init__(self,parent,GOAL_PANELENVIRONMENT_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theGoalId = None
    self.theEnvironmentDictionary = {}
    self.theSelectedIdx = -1
    self.theGoalDefinition = goalDef
    self.theGoalCategory = goalCat
    self.theGoalPriority = goalPri
    self.theGoalFitCriterion = goalFc
    self.theGoalIssue = goalIssue
    self.theGoalAssets = goalAssets

    mainSizer = wx.BoxSizer(wx.HORIZONTAL)
    environmentBox = wx.StaticBox(self)
    environmentListSizer = wx.StaticBoxSizer(environmentBox,wx.HORIZONTAL)
    mainSizer.Add(environmentListSizer,0,wx.EXPAND)
    self.environmentList = EnvironmentListCtrl(self,GOAL_LISTENVIRONMENTS_ID,self.dbProxy)
    environmentListSizer.Add(self.environmentList,1,wx.EXPAND)
    environmentDimSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(environmentDimSizer,1,wx.EXPAND)

    nbBox = wx.StaticBox(self,-1)
    nbSizer = wx.StaticBoxSizer(nbBox,wx.VERTICAL)
    environmentDimSizer.Add(nbSizer,1,wx.EXPAND)
    self.notebook = ReqToGoalNotebook(self,self.dbProxy)
    nbSizer.Add(self.notebook,1,wx.EXPAND)

    self.SetSizer(mainSizer)

    self.goalAssociationCtrl = self.notebook.FindWindowById(GOAL_LISTGOALREFINEMENTS_ID)
    self.subGoalAssociationCtrl = self.notebook.FindWindowById(GOAL_LISTSUBGOALREFINEMENTS_ID)

    self.environmentList.Bind(wx.EVT_LIST_INSERT_ITEM,self.OnAddEnvironment)
    self.environmentList.Bind(wx.EVT_LIST_DELETE_ITEM,self.OnDeleteEnvironment)

    self.goalAssociationCtrl.Disable()
    self.subGoalAssociationCtrl.Disable()

    self.theEnvironmentDictionary[defaultEnv] = GoalEnvironmentProperties(defaultEnv)
    self.environmentList.Select(0)
    self.goalAssociationCtrl.setEnvironment(defaultEnv)
    self.goalAssociationCtrl.DeleteAllItems()
    self.subGoalAssociationCtrl.setEnvironment(defaultEnv)
    self.subGoalAssociationCtrl.DeleteAllItems()
    self.goalAssociationCtrl.Enable()
    self.subGoalAssociationCtrl.Enable()

  def OnEnvironmentSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    p = self.theEnvironmentDictionary[environmentName]

    self.goalAssociationCtrl.setEnvironment(environmentName)
    self.goalAssociationCtrl.load(p.goalRefinements())
    self.subGoalAssociationCtrl.setEnvironment(environmentName)
    self.subGoalAssociationCtrl.load(p.subGoalRefinements())
    self.goalAssociationCtrl.Enable()
    self.subGoalAssociationCtrl.Enable()

  def OnEnvironmentDeselected(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    self.theEnvironmentDictionary[environmentName] = GoalEnvironmentProperties(environmentName,'',self.theGoalDefinition,self.theGoalCategory,self.theGoalPriority,self.theGoalFitCriterion,self.theGoalIssue,self.goalAssociationCtrl.dimensions(),self.subGoalAssociationCtrl.dimensions(),self.theGoalAssets,[])
    self.goalAssociationCtrl.DeleteAllItems()
    self.goalAssociationCtrl.setEnvironment('')
    self.subGoalAssociationCtrl.DeleteAllItems()
    self.subGoalAssociationCtrl.setEnvironment('')
    self.theSelectedIdx = -1
    self.goalAssociationCtrl.Disable()
    self.subGoalAssociationCtrl.Disable()

  def OnAddEnvironment(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    self.theEnvironmentDictionary[environmentName] = GoalEnvironmentProperties(environmentName)
    self.environmentList.Select(self.theSelectedIdx)
    self.goalAssociationCtrl.setEnvironment(environmentName)
    self.goalAssociationCtrl.DeleteAllItems()
    self.subGoalAssociationCtrl.setEnvironment(environmentName)
    self.subGoalAssociationCtrl.DeleteAllItems()
    self.goalAssociationCtrl.Enable()
    self.subGoalAssociationCtrl.Enable()
    inheritedEnv = self.environmentList.inheritedEnvironment()
    if (inheritedEnv != '' and self.theGoalId != None):
      p = self.dbProxy.inheritedGoalProperties(self.theGoalId,inheritedEnv)
      self.theEnvironmentDictionary[environmentName] = p
      self.goalAssociationCtrl.setEnvironment(environmentName)
      self.goalAssociationCtrl.load(p.goalRefinements())
      self.subGoalAssociationCtrl.setEnvironment(environmentName)
      self.subGoalAssociationCtrl.load(p.subGoalRefinements())

  def OnDeleteEnvironment(self,evt):
    selectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(selectedIdx)
    del self.theEnvironmentDictionary[environmentName]
    self.theSelectedIdx = -1
    self.goalAssociationCtrl.DeleteAllItems()
    self.goalAssociationCtrl.setEnvironment('')
    self.subGoalAssociationCtrl.DeleteAllItems()
    self.subGoalAssociationCtrl.setEnvironment('')
    self.goalAssociationCtrl.Disable()
    self.subGoalAssociationCtrl.Disable()

  def environmentProperties(self):
    if (self.theSelectedIdx != -1):
      environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
      self.theEnvironmentDictionary[environmentName] = GoalEnvironmentProperties(environmentName,'',self.theGoalDefinition,self.theGoalCategory,self.theGoalPriority,self.theGoalFitCriterion,self.theGoalIssue,self.goalAssociationCtrl.dimensions(),self.subGoalAssociationCtrl.dimensions(),self.theGoalAssets,[])
    return self.theEnvironmentDictionary.values() 
