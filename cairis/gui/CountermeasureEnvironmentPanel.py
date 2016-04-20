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
from EnvironmentListCtrl import EnvironmentListCtrl
from CountermeasureEnvironmentNotebook import CountermeasureEnvironmentNotebook
from TargetListCtrl import TargetListCtrl
from PropertiesListCtrl import PropertiesListCtrl
from RoleCostListCtrl import RoleCostListCtrl
from CountermeasureRoleListCtrl import CountermeasureRoleListCtrl
from CountermeasureTaskPersonaListCtrl import CountermeasureTaskPersonaListCtrl
from cairis.core.CountermeasureEnvironmentProperties import CountermeasureEnvironmentProperties


class CountermeasureEnvironmentPanel(wx.Panel):
  def __init__(self,parent,dp):
    wx.Panel.__init__(self,parent,COUNTERMEASURE_PANELENVIRONMENT_ID)
    self.dbProxy = dp
    self.theEnvironmentDictionary = {}
    self.theSelectedIdx = -1

    mainSizer = wx.BoxSizer(wx.HORIZONTAL)
    environmentBox = wx.StaticBox(self)
    environmentListSizer = wx.StaticBoxSizer(environmentBox,wx.HORIZONTAL)
    mainSizer.Add(environmentListSizer,0,wx.EXPAND)
    self.environmentList = EnvironmentListCtrl(self,COUNTERMEASURE_LISTENVIRONMENTS_ID,self.dbProxy)
    environmentListSizer.Add(self.environmentList,1,wx.EXPAND)


    environmentDimSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(environmentDimSizer,1,wx.EXPAND)
 
    costBox = wx.StaticBox(self,-1,'Cost')
    costBoxSizer = wx.StaticBoxSizer(costBox,wx.HORIZONTAL)
    environmentDimSizer.Add(costBoxSizer,0,wx.EXPAND)
    self.costCombo = wx.ComboBox(self,COUNTERMEASURE_COMBOCOST_ID,"",choices=['Low','Medium','High'],style=wx.CB_READONLY)
    costBoxSizer.Add(self.costCombo,1,wx.EXPAND)

    nbBox = wx.StaticBox(self,-1)
    nbSizer = wx.StaticBoxSizer(nbBox,wx.HORIZONTAL)
    environmentDimSizer.Add(nbSizer,1,wx.EXPAND)
    self.notebook = CountermeasureEnvironmentNotebook(self,self.dbProxy)
    nbSizer.Add(self.notebook,1,wx.EXPAND)

    self.reqList = self.notebook.FindWindowById(COUNTERMEASURE_LISTREQUIREMENTS_ID)
    self.targetList = self.notebook.FindWindowById(COUNTERMEASURE_LISTTARGETS_ID)
    self.propertiesList = self.notebook.FindWindowById(COUNTERMEASURE_LISTPROPERTIES_ID)
    self.personaList = self.notebook.FindWindowById(COUNTERMEASURE_LISTPERSONAS_ID)
    self.roleList = self.notebook.FindWindowById(COUNTERMEASURE_LISTROLES_ID)

    self.reqList.Disable()
    self.targetList.Disable()
    self.propertiesList.Disable()
    self.costCombo.Disable()
    self.roleList.Disable()
    
    self.SetSizer(mainSizer)
    self.environmentList.Bind(wx.EVT_LIST_INSERT_ITEM,self.OnAddEnvironment)
    self.environmentList.Bind(wx.EVT_LIST_DELETE_ITEM,self.OnDeleteEnvironment)
    self.environmentList.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnEnvironmentSelected)
    self.environmentList.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnEnvironmentDeselected)

  def loadControls(self,countermeasure):
    self.environmentList.Unbind(wx.EVT_LIST_ITEM_SELECTED)
    self.environmentList.Unbind(wx.EVT_LIST_ITEM_DESELECTED)
    environmentNames = []
    for cp in countermeasure.environmentProperties():
      environmentNames.append(cp.name())
    self.environmentList.load(environmentNames)

    for cp in countermeasure.environmentProperties():
      environmentName = cp.name()
      self.theEnvironmentDictionary[environmentName] = cp
      environmentNames.append(environmentName) 
    environmentName = environmentNames[0]
    p = self.theEnvironmentDictionary[environmentName]
    
    self.reqList.setEnvironment(environmentName)
    self.reqList.load(p.requirements())
    self.targetList.setEnvironment(environmentName)
    self.targetList.load(p.targets())
    self.propertiesList.setEnvironment(environmentName)
    self.propertiesList.load(p.properties(),p.rationale())
    self.costCombo.SetStringSelection(p.cost())
    self.roleList.setEnvironment(environmentName)
    self.roleList.load(p.roles())
    self.personaList.load(p.personas())

    self.environmentList.Select(0)

    self.reqList.Enable()
    self.targetList.Enable()
    self.propertiesList.Enable()
    self.costCombo.Enable()
    self.roleList.Enable()
    self.environmentList.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnEnvironmentSelected)
    self.environmentList.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnEnvironmentDeselected)
    self.theSelectedIdx = 0

  def OnEnvironmentSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    p = self.theEnvironmentDictionary[environmentName]
    self.reqList.setEnvironment(environmentName)
    self.reqList.load(p.requirements())
    self.targetList.setEnvironment(environmentName)
    self.targetList.load(p.targets())
    self.propertiesList.setEnvironment(environmentName)
    self.propertiesList.load(p.properties(),p.rationale())
    self.costCombo.SetStringSelection(p.cost())
    self.roleList.setEnvironment(environmentName)
    self.roleList.load(p.roles())
    self.personaList.load(p.personas())
    self.reqList.Enable()
    self.targetList.Enable()
    self.propertiesList.Enable()
    self.costCombo.Enable()
    self.roleList.Enable()
    self.personaList.Enable()


  def OnEnvironmentDeselected(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    syProperties, pRationale = self.propertiesList.properties() 
    properties = CountermeasureEnvironmentProperties(environmentName,self.reqList.dimensions(),self.targetList.targets(),syProperties,pRationale,self.costCombo.GetValue(),self.roleList.dimensions(),self.personaList.dimensions())
    self.theEnvironmentDictionary[environmentName] = properties

    self.reqList.setEnvironment('')
    self.reqList.DeleteAllItems()
    self.targetList.setEnvironment('')
    self.targetList.DeleteAllItems()
    self.propertiesList.setEnvironment('')
    self.propertiesList.DeleteAllItems()
    self.costCombo.SetValue('')
    self.roleList.setEnvironment('')
    self.roleList.DeleteAllItems()
    self.personaList.DeleteAllItems()

    self.theSelectedIdx = -1
    self.reqList.Disable()
    self.targetList.Disable()
    self.propertiesList.Disable()
    self.costCombo.Disable()
    self.roleList.Disable()

  def OnAddEnvironment(self,evt):
    if (self.theSelectedIdx != -1):
      environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
      syProperties,pRationale = self.propertiesList.properties()
      properties = CountermeasureEnvironmentProperties(environmentName,self.reqList.dimensions(),self.targetList.targets(),syProperties,pRationale,self.costCombo.GetValue(),self.roleList.dimensions(),self.personaList.dimensions())
      self.theEnvironmentDictionary[environmentName] = properties
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    self.theEnvironmentDictionary[environmentName] = CountermeasureEnvironmentProperties(environmentName)

    self.reqList.setEnvironment(environmentName)
    self.reqList.DeleteAllItems()
    self.targetList.setEnvironment(environmentName)
    self.targetList.DeleteAllItems()
    self.propertiesList.setEnvironment(environmentName)
    self.propertiesList.DeleteAllItems()
    self.costCombo.SetValue('')
    self.roleList.setEnvironment(environmentName)
    self.roleList.DeleteAllItems()
    self.personaList.DeleteAllItems()

    self.reqList.Enable()
    self.targetList.Enable()
    self.propertiesList.Enable()
    self.costCombo.Enable()
    self.roleList.Enable()

  def OnDeleteEnvironment(self,evt):
    selectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(selectedIdx)
    del self.theEnvironmentDictionary[environmentName]
    self.theSelectedIdx = -1

  def environmentProperties(self):
    if (self.theSelectedIdx != -1):
      environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
      syProperties,pRationale = self.propertiesList.properties()
      properties = CountermeasureEnvironmentProperties(environmentName,self.reqList.dimensions(),self.targetList.targets(),syProperties,pRationale,self.costCombo.GetValue(),self.roleList.dimensions(),self.personaList.dimensions())
      self.theEnvironmentDictionary[environmentName] = properties
    for cname in self.environmentList.dimensions():
      p = self.theEnvironmentDictionary[cname]
      if (len(p.requirements()) == 0):
        exceptionText = 'No requirements selected for environment ' + p.name()
        raise EnvironmentValidationError(exceptionText)
      if (len(p.targets()) == 0):
        exceptionText = 'No targets selected for environment ' + p.name()
        raise EnvironmentValidationError(exceptionText)
      if (len(p.cost()) == 0):
        exceptionText = 'No cost selected for environment ' + p.name()
        raise EnvironmentValidationError(exceptionText)
      if (len(p.roles()) == 0):
        exceptionText = 'No roles selected for environment ' + p.name()
        raise EnvironmentValidationError(exceptionText)
    return self.theEnvironmentDictionary.values() 
