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
from RiskEnvironmentListCtrl import RiskEnvironmentListCtrl
from AcceptEnvironmentProperties import AcceptEnvironmentProperties


class AcceptEnvironmentPanel(wx.Panel):
  def __init__(self,parent,dp):
    wx.Panel.__init__(self,parent,armid.ACCEPT_PANELENVIRONMENT_ID)
    self.dbProxy = dp
    self.theEnvironmentDictionary = {}
    self.theSelectedIdx = -1

    mainSizer = wx.BoxSizer(wx.HORIZONTAL)
    environmentBox = wx.StaticBox(self)
    environmentListSizer = wx.StaticBoxSizer(environmentBox,wx.HORIZONTAL)
    mainSizer.Add(environmentListSizer,0,wx.EXPAND)
    self.environmentList = RiskEnvironmentListCtrl(self,armid.ACCEPT_LISTENVIRONMENTS_ID,self.dbProxy)
    environmentListSizer.Add(self.environmentList,1,wx.EXPAND)
    environmentDimSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(environmentDimSizer,1,wx.EXPAND)

    costBox = wx.StaticBox(self,-1,'Cost')
    costBoxSizer = wx.StaticBoxSizer(costBox,wx.HORIZONTAL)
    environmentDimSizer.Add(costBoxSizer,0,wx.EXPAND)
    self.costCombo = wx.ComboBox(self,armid.ACCEPT_COMBOCOST_ID,"",choices=['Low','Medium','High'],style=wx.CB_READONLY)
    costBoxSizer.Add(self.costCombo,0,wx.EXPAND)
   
    rationaleBox = wx.StaticBox(self,-1,'Rationale')
    rationaleBoxSizer = wx.StaticBoxSizer(rationaleBox,wx.HORIZONTAL)
    environmentDimSizer.Add(rationaleBoxSizer,1,wx.EXPAND)
    self.rationaleCtrl = wx.TextCtrl(self,armid.ACCEPT_TEXTRATIONALE_ID,'',style=wx.TE_MULTILINE)
    rationaleBoxSizer.Add(self.rationaleCtrl,1,wx.EXPAND)
    self.costCombo.Disable() 
    self.rationaleCtrl.Disable()
    
    self.SetSizer(mainSizer)
    self.environmentList.Bind(wx.EVT_LIST_INSERT_ITEM,self.OnAddEnvironment)
    self.environmentList.Bind(wx.EVT_LIST_DELETE_ITEM,self.OnDeleteEnvironment)
    self.environmentList.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnEnvironmentSelected)
    self.environmentList.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnEnvironmentDeselected)

  def loadControls(self,accept):
    self.environmentList.Unbind(wx.EVT_LIST_ITEM_SELECTED)
    self.environmentList.Unbind(wx.EVT_LIST_ITEM_DESELECTED)
    environmentNames = []
    for cp in accept.environmentProperties():
      environmentNames.append(cp.name())
    self.environmentList.load(environmentNames)

    for cp in accept.environmentProperties():
      environmentName = cp.name()
      self.theEnvironmentDictionary[environmentName] = cp
      environmentNames.append(environmentName) 
    environmentName = environmentNames[0]
    p = self.theEnvironmentDictionary[environmentName]
    
    self.costCombo.SetStringSelection(p.cost())
    self.rationaleCtrl.SetValue(p.description()) 
    self.environmentList.Select(0)
    self.costCombo.Enable() 
    self.rationaleCtrl.Enable()
    self.environmentList.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnEnvironmentSelected)
    self.environmentList.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnEnvironmentDeselected)
    self.theSelectedIdx = 0

  def OnEnvironmentSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    p = self.theEnvironmentDictionary[environmentName]
    self.costCombo.SetStringSelection(p.cost())
    self.rationaleCtrl.SetValue(p.description()) 
    self.costCombo.Enable() 
    self.rationaleCtrl.Enable()

  def OnEnvironmentDeselected(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    self.theEnvironmentDictionary[environmentName] = AcceptEnvironmentProperties(environmentName,self.costCombo.GetValue(),self.rationaleCtrl.GetValue())
    self.costCombo.SetValue('')
    self.rationaleCtrl.SetValue('') 
    self.theSelectedIdx = -1
    self.costCombo.Disable() 
    self.rationaleCtrl.Disable()

  def OnAddEnvironment(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    self.theEnvironmentDictionary[environmentName] = AcceptEnvironmentProperties(environmentName)
    self.costCombo.SetValue('')
    self.rationaleCtrl.SetValue('') 
    self.environmentList.Select(self.theSelectedIdx)
    self.costCombo.Enable() 
    self.rationaleCtrl.Enable()

  def OnDeleteEnvironment(self,evt):
    selectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(selectedIdx)
    del self.theEnvironmentDictionary[environmentName]
    self.theSelectedIdx = -1

  def environmentProperties(self):
    if (self.theSelectedIdx != -1):
      environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
      properties = AcceptEnvironmentProperties(environmentName,self.costCombo.GetValue(),self.rationaleCtrl.GetValue())
      self.theEnvironmentDictionary[environmentName] = properties

    for cName in self.theEnvironmentDictionary:
      p = self.theEnvironmentDictionary[cName]
      if (len(p.cost()) == 0):
        exceptionText = 'No cost selected for environment ' + p.name()
        raise ARM.EnvironmentValidationError(exceptionText)
      if (len(p.description()) == 0):
        exceptionText = 'No rationale entered for environment ' + p.name()
        raise ARM.EnvironmentValidationError(exceptionText)
    return self.theEnvironmentDictionary.values() 

  def setRisk(self,riskName):
    self.environmentList.setRisk(riskName)
