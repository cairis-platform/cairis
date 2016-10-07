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
from DimensionListCtrl import DimensionListCtrl
from EnvironmentListCtrl import EnvironmentListCtrl
from PropertiesListCtrl import PropertiesListCtrl
from cairis.core.ThreatEnvironmentProperties import ThreatEnvironmentProperties
from ValueDictionary import ValueDictionary

__author__ = 'Shamal Faily'

class ThreatEnvironmentPanel(wx.Panel):
  def __init__(self,parent,dp):
    wx.Panel.__init__(self,parent,THREAT_PANELENVIRONMENT_ID)
    self.dbProxy = dp
    self.theThreatId = None
    self.theEnvironmentDictionary = {}
    self.theSelectedIdx = -1

    mainSizer = wx.BoxSizer(wx.HORIZONTAL)
    environmentBox = wx.StaticBox(self)
    environmentListSizer = wx.StaticBoxSizer(environmentBox,wx.HORIZONTAL)
    mainSizer.Add(environmentListSizer,0,wx.EXPAND)
    self.environmentList = EnvironmentListCtrl(self,THREATENVIRONMENT_LISTENVIRONMENTS_ID,self.dbProxy)
    environmentListSizer.Add(self.environmentList,1,wx.EXPAND)

    environmentDimSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(environmentDimSizer,1,wx.EXPAND)

    lhoodBox = wx.StaticBox(self)
    lhoodSizer = wx.StaticBoxSizer(lhoodBox,wx.HORIZONTAL)
    environmentDimSizer.Add(lhoodSizer,0,wx.EXPAND)
    lhoodSizer.Add(wx.StaticText(self,-1,'Likelihood'))
    lhoodList = ['Incredible','Improbable','Remote','Occasional','Probable','Frequent']
    self.lhoodCtrl = wx.ComboBox(self,THREATENVIRONMENT_COMBOLIKELIHOOD_ID,choices=lhoodList,size=wx.DefaultSize,style=wx.CB_READONLY)
    lhoodSizer.Add(self.lhoodCtrl,1,wx.EXPAND) 

    aaSizer = wx.BoxSizer(wx.HORIZONTAL)
    environmentDimSizer.Add(aaSizer,1,wx.EXPAND)
    self.attackerList = DimensionListCtrl(self,THREATENVIRONMENT_LISTATTACKERS_ID,wx.DefaultSize,'Attacker','attacker',self.dbProxy)
    attackerBox = wx.StaticBox(self)
    attackerSizer = wx.StaticBoxSizer(attackerBox,wx.HORIZONTAL)
    attackerSizer.Add(self.attackerList,1,wx.EXPAND)
    aaSizer.Add(attackerSizer,1,wx.EXPAND)

    self.assetList = DimensionListCtrl(self,THREATENVIRONMENT_LISTASSETS_ID,wx.DefaultSize,'Asset','asset',self.dbProxy)
    assetBox = wx.StaticBox(self)
    assetSizer = wx.StaticBoxSizer(assetBox,wx.HORIZONTAL)
    assetSizer.Add(self.assetList,1,wx.EXPAND)
    aaSizer.Add(assetSizer,1,wx.EXPAND)

    propertiesBox = wx.StaticBox(self)
    propertiesSizer = wx.StaticBoxSizer(propertiesBox,wx.HORIZONTAL)
    environmentDimSizer.Add(propertiesSizer,1,wx.EXPAND)
    values = self.dbProxy.getDimensionNames('threat_value')
    valueLookup = ValueDictionary(values)
    self.propertiesList = PropertiesListCtrl(self,THREATENVIRONMENT_LISTPROPERTIES_ID,valueLookup)
    propertiesSizer.Add(self.propertiesList,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    self.environmentList.Bind(wx.EVT_LIST_INSERT_ITEM,self.OnAddEnvironment)
    self.environmentList.Bind(wx.EVT_LIST_DELETE_ITEM,self.OnDeleteEnvironment)


  def loadControls(self,threat):
    self.environmentList.Unbind(wx.EVT_LIST_ITEM_SELECTED)
    self.environmentList.Unbind(wx.EVT_LIST_ITEM_DESELECTED)
    self.theThreatId = threat.id()
# We load the environment name control before anything else.  Weird stuff happens if we don't do this.  Don't ask me why!!!
    environmentNames = []
    if (len(threat.environmentProperties()) > 0):
      for cp in threat.environmentProperties():
        environmentNames.append(cp.name())
      self.environmentList.load(environmentNames)
      for cp in threat.environmentProperties():
        environmentName = cp.name()
        self.theEnvironmentDictionary[environmentName] = cp
      environmentName = environmentNames[0]
      p = self.theEnvironmentDictionary[environmentName]
      self.lhoodCtrl.SetStringSelection(p.likelihood())
      self.attackerList.setEnvironment(environmentName)
      self.attackerList.load(p.attackers()) 
      self.assetList.setEnvironment(environmentName)
      self.assetList.load(p.assets()) 
      self.propertiesList.setEnvironment(environmentName)
      self.propertiesList.load(p.properties(),p.rationale())
      self.environmentList.Select(0)

    self.environmentList.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnEnvironmentSelected)
    self.environmentList.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnEnvironmentDeselected)
    self.theSelectedIdx = 0

  def OnEnvironmentSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    p = self.theEnvironmentDictionary[environmentName]
    self.lhoodCtrl.SetStringSelection(p.likelihood())
    self.attackerList.setEnvironment(environmentName)
    self.attackerList.load(p.attackers()) 
    self.assetList.setEnvironment(environmentName)
    self.assetList.load(p.assets()) 
    self.propertiesList.setEnvironment(environmentName)
    self.propertiesList.load(p.properties(),p.rationale())

  def OnEnvironmentDeselected(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    syProperties,pRationale = self.propertiesList.properties()
    self.theEnvironmentDictionary[environmentName] = ThreatEnvironmentProperties(environmentName,self.lhoodCtrl.GetValue(),self.assetList.dimensions(),self.attackerList.dimensions(),syProperties,pRationale)
    self.lhoodCtrl.SetValue('')
    self.attackerList.setEnvironment('')
    self.attackerList.DeleteAllItems() 
    self.assetList.setEnvironment('')
    self.assetList.DeleteAllItems() 
    self.propertiesList.setEnvironment('')
    self.propertiesList.DeleteAllItems()
    self.theSelectedIdx = -1

  def OnAddEnvironment(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    self.theEnvironmentDictionary[environmentName] = ThreatEnvironmentProperties(environmentName,'',[],[],[0,0,0,0,0,0,0,0],['None','None','None','None','None','None','None','None'])
    self.environmentList.Select(self.theSelectedIdx)
    self.attackerList.setEnvironment(environmentName)
    self.assetList.setEnvironment(environmentName)
    self.propertiesList.setEnvironment(environmentName)
    inheritedEnv = self.environmentList.inheritedEnvironment()
    if (inheritedEnv != '' and self.theThreatId != None):
      p = self.dbProxy.inheritedThreatProperties(self.theThreatId,inheritedEnv)
      self.theEnvironmentDictionary[environmentName] = p
      self.lhoodCtrl.SetStringSelection(p.likelihood())
      self.attackerList.setEnvironment(environmentName)
      self.attackerList.load(p.attackers()) 
      self.assetList.setEnvironment(environmentName)
      self.assetList.load(p.assets()) 
      self.propertiesList.setEnvironment(environmentName)
      self.propertiesList.load(p.properties(),p.rationale())

  def OnDeleteEnvironment(self,evt):
    selectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(selectedIdx)
    del self.theEnvironmentDictionary[environmentName]
    self.theSelectedIdx = -1

  def environmentProperties(self):
    if (self.theSelectedIdx != -1):
      environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
      syProperties,pRationale = self.propertiesList.properties() 
      self.theEnvironmentDictionary[environmentName] = ThreatEnvironmentProperties(environmentName,self.lhoodCtrl.GetValue(),self.assetList.dimensions(),self.attackerList.dimensions(),syProperties,pRationale)
    return self.theEnvironmentDictionary.values() 
