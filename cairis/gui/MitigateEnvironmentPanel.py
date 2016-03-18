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
from DimensionListCtrl import DimensionListCtrl
from MitigateEnvironmentProperties import MitigateEnvironmentProperties


class MitigateEnvironmentPanel(wx.Panel):
  def __init__(self,parent,dp):
    wx.Panel.__init__(self,parent,armid.MITIGATE_PANELENVIRONMENT_ID)
    self.theResponsePanel = parent
    self.dbProxy = dp
    self.theEnvironmentDictionary = {}
    self.theSelectedIdx = -1

    mainSizer = wx.BoxSizer(wx.HORIZONTAL)
    environmentBox = wx.StaticBox(self)
    environmentListSizer = wx.StaticBoxSizer(environmentBox,wx.HORIZONTAL)
    mainSizer.Add(environmentListSizer,0,wx.EXPAND)
    self.environmentList = RiskEnvironmentListCtrl(self,armid.MITIGATE_LISTENVIRONMENTS_ID,self.dbProxy)
    environmentListSizer.Add(self.environmentList,1,wx.EXPAND)
    environmentDimSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(environmentDimSizer,1,wx.EXPAND)

    typeBox = wx.StaticBox(self,-1,'Type')
    typeBoxSizer = wx.StaticBoxSizer(typeBox,wx.HORIZONTAL)
    environmentDimSizer.Add(typeBoxSizer,0,wx.EXPAND)
    self.typeCombo = wx.ComboBox(self,armid.MITIGATE_COMBOTYPE_ID,"",choices=['Deter','Prevent','Detect','React'],style=wx.CB_READONLY)
    typeBoxSizer.Add(self.typeCombo,1,wx.EXPAND)
   
    pointBox = wx.StaticBox(self,-1,'Detection Point')
    pointBoxSizer = wx.StaticBoxSizer(pointBox,wx.HORIZONTAL)
    environmentDimSizer.Add(pointBoxSizer,0,wx.EXPAND)
    self.pointCombo = wx.ComboBox(self,armid.MITIGATE_COMBODETECTIONPOINT_ID,"",choices=['Before','At','After'],style=wx.CB_READONLY)
    pointBoxSizer.Add(self.pointCombo,1,wx.EXPAND)


    dmBox = wx.StaticBox(self,-1,)
    dmBoxSizer = wx.StaticBoxSizer(dmBox,wx.HORIZONTAL)
    environmentDimSizer.Add(dmBoxSizer,1,wx.EXPAND)
    self.dmList = DimensionListCtrl(self,armid.MITIGATE_LISTDETMECH_ID,wx.DefaultSize,'Detection Mechanism','detection_mechanism',self.dbProxy,listStyle=wx.LC_REPORT)
    dmBoxSizer.Add(self.dmList,1,wx.EXPAND)

    self.typeCombo.Disable()
    self.pointCombo.Disable() 
    self.dmList.Disable()
    
    self.SetSizer(mainSizer)
    self.typeCombo.Bind(wx.EVT_COMBOBOX,self.onTypeChange)
    self.environmentList.Bind(wx.EVT_LIST_INSERT_ITEM,self.OnAddEnvironment)
    self.environmentList.Bind(wx.EVT_LIST_DELETE_ITEM,self.OnDeleteEnvironment)
    self.environmentList.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnEnvironmentSelected)
    self.environmentList.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnEnvironmentDeselected)

  def onTypeChange(self,evt):
    self.activateTypeCtrls()
    mitType = self.typeCombo.GetValue()
    riskCombo = self.theResponsePanel.FindWindowById(armid.RESPONSE_COMBORISK_ID)
    riskName = riskCombo.GetValue()
    if (riskName != ''):
      riskNameCtrl = self.theResponsePanel.FindWindowById(armid.RESPONSE_TEXTNAME_ID)
      riskNameLabel = mitType + ' ' + riskName
      riskNameCtrl.SetValue(riskNameLabel)

  def activateTypeCtrls(self):
    mitType = self.typeCombo.GetValue()
    if ((mitType == 'Deter') or (mitType == 'Prevent')):
      self.pointCombo.SetValue('')
      self.pointCombo.Disable() 
      self.dmList.DeleteAllItems()
      self.dmList.Disable()
    elif (mitType == 'Detect'):
      self.pointCombo.Enable() 
      self.dmList.Disable()
    elif (mitType == 'React'):
      self.pointCombo.Disable() 
      self.dmList.Enable()
  
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
    
    self.typeCombo.SetStringSelection(p.type())
    self.pointCombo.SetStringSelection(p.detectionPoint())
    self.dmList.setEnvironment(environmentName)
    self.dmList.load(p.detectionMechanisms())

    self.environmentList.Select(0)

    self.activateTypeCtrls()
    self.environmentList.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnEnvironmentSelected)
    self.environmentList.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnEnvironmentDeselected)
    self.theSelectedIdx = 0

  def OnEnvironmentSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    p = self.theEnvironmentDictionary[environmentName]

    self.typeCombo.SetStringSelection(p.type())
    self.pointCombo.SetStringSelection(p.detectionPoint())
    self.dmList.setEnvironment(environmentName)
    self.dmList.load(p.detectionMechanisms())
    self.typeCombo.Enable()
    self.activateTypeCtrls()

  def OnEnvironmentDeselected(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    self.theEnvironmentDictionary[environmentName] = MitigateEnvironmentProperties(environmentName,self.typeCombo.GetValue(),self.pointCombo.GetValue(),self.dmList.dimensions())
    self.typeCombo.SetValue('')
    self.pointCombo.SetValue('')
    self.dmList.setEnvironment('')
    self.dmList.DeleteAllItems()

    self.theSelectedIdx = -1
    self.typeCombo.Disable() 
    self.pointCombo.Disable() 
    self.dmList.Disable() 

  def OnAddEnvironment(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    self.theEnvironmentDictionary[environmentName] = MitigateEnvironmentProperties(environmentName)
    self.typeCombo.SetValue('')
    self.pointCombo.SetValue('')
    self.dmList.setEnvironment(environmentName)
    self.dmList.DeleteAllItems()
    self.environmentList.Select(self.theSelectedIdx)
    self.typeCombo.Enable() 

  def OnDeleteEnvironment(self,evt):
    selectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(selectedIdx)
    del self.theEnvironmentDictionary[environmentName]
    self.theSelectedIdx = -1

  def environmentProperties(self):
    if (self.theSelectedIdx != -1):
      environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
      properties = MitigateEnvironmentProperties(environmentName,self.typeCombo.GetValue(),self.pointCombo.GetValue(),self.dmList.dimensions())
      self.theEnvironmentDictionary[environmentName] = properties
    for cname in self.environmentList.dimensions():
      p = self.theEnvironmentDictionary[cname]
      mitType = p.type()
      if (len(mitType) == 0):
        exceptionText = 'No mitigation type selected for environment ' + p.name()
        raise ARM.EnvironmentValidationError(exceptionText)
      if (mitType == 'Detect') and (len(p.detectionPoint()) == 0):
        exceptionText = 'No detection point selected for environment ' + p.name()
        raise ARM.EnvironmentValidationError(exceptionText)
      if (mitType == 'React') and (len(p.detectionMechanisms()) == 0):
        exceptionText = 'No detection mechanisms selected for environment ' + p.name()
        raise ARM.EnvironmentValidationError(exceptionText)
    return self.theEnvironmentDictionary.values() 

  def setRisk(self,riskName):
    self.environmentList.setRisk(riskName)
