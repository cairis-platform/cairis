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
from ObstacleEnvironmentProperties import ObstacleEnvironmentProperties
from ObstacleEnvironmentNotebook import ObstacleEnvironmentNotebook
from EnvironmentListCtrl import EnvironmentListCtrl

class ObstacleEnvironmentPanel(wx.Panel):
  def __init__(self,parent,dp):
    wx.Panel.__init__(self,parent,armid.OBSTACLE_PANELENVIRONMENT_ID)
    self.dbProxy = dp
    self.theObstacleId = None
    self.theEnvironmentDictionary = {}
    self.theSelectedIdx = -1

    mainSizer = wx.BoxSizer(wx.HORIZONTAL)
    environmentBox = wx.StaticBox(self)
    environmentListSizer = wx.StaticBoxSizer(environmentBox,wx.HORIZONTAL)
    mainSizer.Add(environmentListSizer,0,wx.EXPAND)
    self.environmentList = EnvironmentListCtrl(self,armid.OBSTACLE_LISTENVIRONMENTS_ID,self.dbProxy)
    environmentListSizer.Add(self.environmentList,1,wx.EXPAND)
    environmentDimSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(environmentDimSizer,1,wx.EXPAND)

    nbBox = wx.StaticBox(self,-1)
    nbSizer = wx.StaticBoxSizer(nbBox,wx.VERTICAL)
    environmentDimSizer.Add(nbSizer,1,wx.EXPAND)
    self.notebook = ObstacleEnvironmentNotebook(self,self.dbProxy)
    nbSizer.Add(self.notebook,1,wx.EXPAND)

    self.labelCtrl = self.notebook.FindWindowById(armid.OBSTACLE_TEXTLABEL_ID)
    self.probCtrl = self.notebook.FindWindowById(armid.OBSTACLE_TEXTPROBABILITY_ID)
    self.categoryCtrl = self.notebook.FindWindowById(armid.OBSTACLE_COMBOCATEGORY_ID)
    self.definitionCtrl = self.notebook.FindWindowById(armid.OBSTACLE_TEXTDEFINITION_ID)
    self.goalAssociationCtrl = self.notebook.FindWindowById(armid.OBSTACLE_LISTGOALS_ID)
    self.subGoalAssociationCtrl = self.notebook.FindWindowById(armid.OBSTACLE_LISTSUBGOALS_ID)
    self.concernsCtrl = self.notebook.FindWindowById(armid.OBSTACLE_LISTCONCERNS_ID)

    self.SetSizer(mainSizer)
    self.environmentList.Bind(wx.EVT_LIST_INSERT_ITEM,self.OnAddEnvironment)
    self.environmentList.Bind(wx.EVT_LIST_DELETE_ITEM,self.OnDeleteEnvironment)

    self.categoryCtrl.Disable()
    self.definitionCtrl.Disable()
    self.goalAssociationCtrl.Disable()
    self.subGoalAssociationCtrl.Disable()
    self.concernsCtrl.Disable()


  def loadControls(self,obstacle):
    self.environmentList.Unbind(wx.EVT_LIST_ITEM_SELECTED)
    self.environmentList.Unbind(wx.EVT_LIST_ITEM_DESELECTED)
    self.theObstacleId = obstacle.id()
    environmentNames = []
    for cp in obstacle.environmentProperties():
      environmentNames.append(cp.name())
    self.environmentList.load(environmentNames)

    for cp in obstacle.environmentProperties():
      environmentName = cp.name()
      self.theEnvironmentDictionary[environmentName] = cp
      environmentNames.append(environmentName) 
    environmentName = environmentNames[0]
    p = self.theEnvironmentDictionary[environmentName]

    self.labelCtrl.SetValue(p.label())
    self.probCtrl.SetValue(str(p.probability()))
    self.categoryCtrl.SetValue(p.category())
    self.definitionCtrl.SetValue(p.definition())
    self.goalAssociationCtrl.setEnvironment(environmentName)
    self.goalAssociationCtrl.load(p.goalRefinements())
    self.subGoalAssociationCtrl.setEnvironment(environmentName)
    self.concernsCtrl.setEnvironment(environmentName)
    self.subGoalAssociationCtrl.load(p.subGoalRefinements())
    self.concernsCtrl.load(p.concerns())

    self.environmentList.Select(0)
    self.environmentList.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnEnvironmentSelected)
    self.environmentList.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnEnvironmentDeselected)

    self.categoryCtrl.Enable()
    self.definitionCtrl.Enable()
    self.goalAssociationCtrl.Enable()
    self.subGoalAssociationCtrl.Enable()
    self.concernsCtrl.Enable()
    self.theSelectedIdx = 0

  def OnEnvironmentSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    p = self.theEnvironmentDictionary[environmentName]

    self.labelCtrl.SetValue(p.label())
    self.probCtrl.SetValue(str(p.probability()))
    self.categoryCtrl.SetValue(p.category())
    self.definitionCtrl.SetValue(p.definition())
    self.goalAssociationCtrl.setEnvironment(environmentName)
    self.goalAssociationCtrl.load(p.goalRefinements())
    self.subGoalAssociationCtrl.setEnvironment(environmentName)
    self.concernsCtrl.setEnvironment(environmentName)
    self.subGoalAssociationCtrl.load(p.subGoalRefinements())
    self.concernsCtrl.load(p.concerns())

    self.categoryCtrl.Enable()
    self.definitionCtrl.Enable()
    self.goalAssociationCtrl.Enable()
    self.subGoalAssociationCtrl.Enable()
    self.concernsCtrl.Enable()

  def OnEnvironmentDeselected(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    self.theEnvironmentDictionary[environmentName] = ObstacleEnvironmentProperties(environmentName,self.labelCtrl.GetValue(),self.definitionCtrl.GetValue(),self.categoryCtrl.GetValue(),self.goalAssociationCtrl.dimensions(),self.subGoalAssociationCtrl.dimensions(),self.concernsCtrl.dimensions())
    self.labelCtrl.SetValue('')
    self.probCtrl.SetValue('')
    self.categoryCtrl.SetValue('')
    self.definitionCtrl.SetValue('')
    self.goalAssociationCtrl.DeleteAllItems()
    self.goalAssociationCtrl.setEnvironment('')
    self.subGoalAssociationCtrl.DeleteAllItems()
    self.concernsCtrl.DeleteAllItems()
    self.subGoalAssociationCtrl.setEnvironment('')
    self.concernsCtrl.setEnvironment('')
    self.theSelectedIdx = -1
    self.categoryCtrl.Disable()
    self.definitionCtrl.Disable()
    self.goalAssociationCtrl.Disable()
    self.subGoalAssociationCtrl.Disable()
    self.concernsCtrl.Disable()

  def OnAddEnvironment(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    self.theEnvironmentDictionary[environmentName] = ObstacleEnvironmentProperties(environmentName)
    self.environmentList.Select(self.theSelectedIdx)
    self.labelCtrl.SetValue('')
    self.probCtrl.SetValue('')
    self.categoryCtrl.SetValue('')
    self.definitionCtrl.SetValue('None')
    self.goalAssociationCtrl.setEnvironment(environmentName)
    self.goalAssociationCtrl.DeleteAllItems()
    self.subGoalAssociationCtrl.setEnvironment(environmentName)
    self.concernsCtrl.setEnvironment(environmentName)
    self.subGoalAssociationCtrl.DeleteAllItems()
    self.concernsCtrl.DeleteAllItems()
    self.categoryCtrl.Enable()
    self.definitionCtrl.Enable()
    self.goalAssociationCtrl.Enable()
    self.subGoalAssociationCtrl.Enable()
    self.concernsCtrl.Enable()
    inheritedEnv = self.environmentList.inheritedEnvironment()
    if (inheritedEnv != '' and self.theObstacleId != None):
      p = self.dbProxy.inheritedObstacleProperties(self.theObstacleId,inheritedEnv)
      self.theEnvironmentDictionary[environmentName] = p
      self.labelCtrl.SetValue(p.label())
      self.labelCtrl.SetValue(str(p.probability()))
      self.categoryCtrl.SetValue(p.category())
      self.definitionCtrl.SetValue(p.definition())
      self.goalAssociationCtrl.setEnvironment(environmentName)
      self.goalAssociationCtrl.load(p.goalRefinements())
      self.subGoalAssociationCtrl.setEnvironment(environmentName)
      self.concernsCtrl.setEnvironment(environmentName)
      self.subGoalAssociationCtrl.load(p.subGoalRefinements())
      self.concernsCtrl.load(p.concerns())

  def OnDeleteEnvironment(self,evt):
    selectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(selectedIdx)
    del self.theEnvironmentDictionary[environmentName]
    self.theSelectedIdx = -1
    self.labelCtrl.SetValue('')
    self.probCtrl.SetValue('')
    self.categoryCtrl.SetValue('')
    self.definitionCtrl.SetValue('')
    self.goalAssociationCtrl.DeleteAllItems()
    self.goalAssociationCtrl.setEnvironment('')
    self.subGoalAssociationCtrl.DeleteAllItems()
    self.subGoalAssociationCtrl.setEnvironment('')
    self.concernsCtrl.DeleteAllItems()
    self.concernsCtrl.setEnvironment('')
    self.categoryCtrl.Disable()
    self.definitionCtrl.Disable()
    self.goalAssociationCtrl.Disable()
    self.subGoalAssociationCtrl.Disable()
    self.concernsCtrl.Disable()


  def environmentProperties(self):
    if (self.theSelectedIdx != -1):
      environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
      self.theEnvironmentDictionary[environmentName] = ObstacleEnvironmentProperties(environmentName,self.labelCtrl.GetValue(),self.definitionCtrl.GetValue(),self.categoryCtrl.GetValue(),self.goalAssociationCtrl.dimensions(),self.subGoalAssociationCtrl.dimensions(),self.concernsCtrl.dimensions())
    return self.theEnvironmentDictionary.values() 
