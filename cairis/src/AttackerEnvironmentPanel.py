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
from EnvironmentListCtrl import EnvironmentListCtrl
from DimensionListCtrl import DimensionListCtrl
from CapabilitiesListCtrl import CapabilitiesListCtrl
from AttackerEnvironmentProperties import AttackerEnvironmentProperties


class AttackerEnvironmentPanel(wx.Panel):
  def __init__(self,parent,dp):
    wx.Panel.__init__(self,parent,armid.ATTACKER_PANELENVIRONMENT_ID)
    self.dbProxy = dp
    self.theAttackerId = None
    self.theEnvironmentDictionary = {}
    self.theSelectedIdx = -1

    mainSizer = wx.BoxSizer(wx.HORIZONTAL)
    environmentBox = wx.StaticBox(self)
    environmentListSizer = wx.StaticBoxSizer(environmentBox,wx.HORIZONTAL)
    mainSizer.Add(environmentListSizer,0,wx.EXPAND)
    self.environmentList = EnvironmentListCtrl(self,armid.ATTACKERENVIRONMENT_LISTENVIRONMENTS_ID,self.dbProxy)
    environmentListSizer.Add(self.environmentList,1,wx.EXPAND)
    environmentDimSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(environmentDimSizer,1,wx.EXPAND)
    rmSizer = wx.BoxSizer(wx.HORIZONTAL)
    environmentDimSizer.Add(rmSizer,1,wx.EXPAND)
    self.roleList = DimensionListCtrl(self,armid.ATTACKERENVIRONMENT_LISTROLES_ID,wx.DefaultSize,'Role','role',self.dbProxy)
    roleBox = wx.StaticBox(self)
    roleSizer = wx.StaticBoxSizer(roleBox,wx.HORIZONTAL)
    roleSizer.Add(self.roleList,1,wx.EXPAND)
    rmSizer.Add(roleSizer,1,wx.EXPAND)

    self.motiveList = DimensionListCtrl(self,armid.ATTACKERENVIRONMENT_LISTMOTIVES_ID,wx.DefaultSize,'Motive','motivation',self.dbProxy)
    motiveBox = wx.StaticBox(self)
    motiveSizer = wx.StaticBoxSizer(motiveBox,wx.HORIZONTAL)
    motiveSizer.Add(self.motiveList,1,wx.EXPAND)
    rmSizer.Add(motiveSizer,1,wx.EXPAND)
    capBox = wx.StaticBox(self)
    capSizer = wx.StaticBoxSizer(capBox,wx.HORIZONTAL)
    environmentDimSizer.Add(capSizer,1,wx.EXPAND)
    self.capabilitiesList = CapabilitiesListCtrl(self,armid.ATTACKERENVIRONMENT_LISTCAPABILITIES_ID,self.dbProxy)
    capSizer.Add(self.capabilitiesList,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    self.environmentList.Bind(wx.EVT_LIST_INSERT_ITEM,self.OnAddEnvironment)
    self.environmentList.Bind(wx.EVT_LIST_DELETE_ITEM,self.OnDeleteEnvironment)


  def loadControls(self,attacker):
    self.environmentList.Unbind(wx.EVT_LIST_ITEM_SELECTED)
    self.environmentList.Unbind(wx.EVT_LIST_ITEM_DESELECTED)
    self.theAttackerId = attacker.id()
    environmentNames = []
    for cp in attacker.environmentProperties():
      environmentNames.append(cp.name())
    self.environmentList.load(environmentNames)

    for cp in attacker.environmentProperties():
      environmentName = cp.name()
      self.theEnvironmentDictionary[environmentName] = cp
      environmentNames.append(environmentName) 
    environmentName = environmentNames[0]
    p = self.theEnvironmentDictionary[environmentName]
    self.roleList.setEnvironment(environmentName)
    self.roleList.load(p.roles()) 
    self.motiveList.setEnvironment(environmentName)
    self.motiveList.load(p.motives()) 
    self.capabilitiesList.setEnvironment(environmentName)
    self.capabilitiesList.load(p.capabilities())
    self.environmentList.Select(0)
    self.environmentList.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnEnvironmentSelected)
    self.environmentList.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnEnvironmentDeselected)
    self.theSelectedIdx = 0

  def OnEnvironmentSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    p = self.theEnvironmentDictionary[environmentName]
    self.roleList.setEnvironment(environmentName)
    self.roleList.load(p.roles()) 
    self.motiveList.setEnvironment(environmentName)
    self.motiveList.load(p.motives()) 
    self.capabilitiesList.setEnvironment(environmentName)
    self.capabilitiesList.load(p.capabilities())

  def OnEnvironmentDeselected(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    self.theEnvironmentDictionary[environmentName] = AttackerEnvironmentProperties(environmentName,self.roleList.dimensions(),self.motiveList.dimensions(),self.capabilitiesList.capabilities())

    self.roleList.setEnvironment('')
    self.roleList.DeleteAllItems() 
    self.motiveList.setEnvironment('')
    self.motiveList.DeleteAllItems() 
    self.capabilitiesList.setEnvironment('')
    self.capabilitiesList.DeleteAllItems()
    self.theSelectedIdx = -1

  def OnAddEnvironment(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    self.theEnvironmentDictionary[environmentName] = AttackerEnvironmentProperties(environmentName,[],[],[])
    self.environmentList.Select(self.theSelectedIdx)
    self.capabilitiesList.setEnvironment(environmentName)
    inheritedEnv = self.environmentList.inheritedEnvironment()
    if (inheritedEnv != '' and self.theAttackerId != None):
      p = self.dbProxy.inheritedAttackerProperties(self.theAttackerId,inheritedEnv)
      self.theEnvironmentDictionary[environmentName] = p
      self.roleList.setEnvironment(environmentName)
      self.roleList.load(p.roles()) 
      self.motiveList.setEnvironment(environmentName)
      self.motiveList.load(p.motives()) 
      self.capabilitiesList.setEnvironment(environmentName)
      self.capabilitiesList.load(p.capabilities())


  def OnDeleteEnvironment(self,evt):
    selectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(selectedIdx)
    del self.theEnvironmentDictionary[environmentName]
    self.theSelectedIdx = -1

  def environmentProperties(self):
    if (self.theSelectedIdx != -1):
      environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
      self.theEnvironmentDictionary[environmentName] = AttackerEnvironmentProperties(environmentName,self.roleList.dimensions(),self.motiveList.dimensions(),self.capabilitiesList.capabilities())
    return self.theEnvironmentDictionary.values() 
