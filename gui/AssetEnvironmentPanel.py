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
from PropertiesListCtrl import PropertiesListCtrl
from AssetEnvironmentProperties import AssetEnvironmentProperties
from EnvironmentListCtrl import EnvironmentListCtrl
from AssetEnvironmentNotebook import AssetEnvironmentNotebook

class AssetEnvironmentPanel(wx.Panel):
  def __init__(self,parent,dp):
    wx.Panel.__init__(self,parent,armid.ASSET_PANELENVIRONMENT_ID)
    self.dbProxy = dp
    self.theAssetId = None
    self.theEnvironmentDictionary = {}
    self.theSelectedIdx = -1

    mainSizer = wx.BoxSizer(wx.HORIZONTAL)
    environmentBox = wx.StaticBox(self)
    environmentListSizer = wx.StaticBoxSizer(environmentBox,wx.HORIZONTAL)
    mainSizer.Add(environmentListSizer,0,wx.EXPAND)
    self.environmentList = EnvironmentListCtrl(self,armid.ASSETENVIRONMENT_LISTENVIRONMENTS_ID,self.dbProxy)
    environmentListSizer.Add(self.environmentList,1,wx.EXPAND)
    dimBox = wx.StaticBox(self)
    environmentDimSizer = wx.StaticBoxSizer(dimBox,wx.VERTICAL)
    mainSizer.Add(environmentDimSizer,1,wx.EXPAND)

    nbBox = wx.StaticBox(self,-1)
    nbSizer = wx.StaticBoxSizer(nbBox,wx.HORIZONTAL)
    environmentDimSizer.Add(nbSizer,1,wx.EXPAND)
    self.notebook = AssetEnvironmentNotebook(self,self.dbProxy)
    nbSizer.Add(self.notebook,1,wx.EXPAND)

    self.propertiesList = self.notebook.FindWindowById(armid.ASSETENVIRONMENT_LISTPROPERTIES_ID)
    self.associationCtrl = self.notebook.FindWindowById(armid.ASSET_LISTASSOCIATIONS_ID)

    self.SetSizer(mainSizer)
    self.environmentList.Bind(wx.EVT_LIST_INSERT_ITEM,self.OnAddEnvironment)
    self.environmentList.Bind(wx.EVT_LIST_DELETE_ITEM,self.OnDeleteEnvironment)
    self.environmentList.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnEnvironmentSelected)
    self.environmentList.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnEnvironmentDeselected)

    self.propertiesList.Disable()
    self.associationCtrl.Disable()

  def loadControls(self,asset):
    self.theAssetId = asset.id()
    self.environmentList.Unbind(wx.EVT_LIST_ITEM_SELECTED)
    self.environmentList.Unbind(wx.EVT_LIST_ITEM_DESELECTED)
    noOfProperties = len(asset.environmentProperties())
    if (noOfProperties > 0):
      environmentNames = []
      for cp in asset.environmentProperties():
        environmentNames.append(cp.name())
      self.environmentList.load(environmentNames)

      for cp in asset.environmentProperties():
        environmentName = cp.name()
        self.theEnvironmentDictionary[environmentName] = cp
        environmentNames.append(environmentName) 
      environmentName = environmentNames[0]
      p = self.theEnvironmentDictionary[environmentName]
      self.propertiesList.setEnvironment(environmentName)
      self.propertiesList.load(p.properties(),p.rationale()) 
      self.associationCtrl.setEnvironment(environmentName)
      self.associationCtrl.load(p.associations()) 
      self.environmentList.Select(0)

    self.environmentList.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnEnvironmentSelected)
    self.environmentList.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnEnvironmentDeselected)

    self.propertiesList.Enable()
    self.associationCtrl.Enable()
    if (noOfProperties > 0):
      self.theSelectedIdx = 0

  def OnEnvironmentSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    p = self.theEnvironmentDictionary[environmentName]
    self.propertiesList.setEnvironment(environmentName)
    self.propertiesList.load(p.properties(),p.rationale())
    self.associationCtrl.setEnvironment(environmentName)
    self.associationCtrl.load(p.associations()) 
    self.propertiesList.Enable()
    self.associationCtrl.Enable()

  def OnEnvironmentDeselected(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    syProperties,pRationale = self.propertiesList.properties()
    self.theEnvironmentDictionary[environmentName] = AssetEnvironmentProperties(environmentName,syProperties,pRationale,self.associationCtrl.dimensions())
    self.propertiesList.setEnvironment('')
    self.propertiesList.DeleteAllItems() 
    self.associationCtrl.setEnvironment('')
    self.associationCtrl.DeleteAllItems() 
    self.propertiesList.Disable()
    self.associationCtrl.Disable()

    self.theSelectedIdx = -1

  def OnAddEnvironment(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    self.theEnvironmentDictionary[environmentName] = AssetEnvironmentProperties(environmentName,[0,0,0,0,0,0,0,0],['None','None','None','None','None','None','None','None'])
    self.environmentList.Select(self.theSelectedIdx)
    self.propertiesList.setEnvironment(environmentName)
    self.propertiesList.DeleteAllItems()
    self.associationCtrl.setEnvironment(environmentName)
    self.associationCtrl.DeleteAllItems()
    self.propertiesList.Enable()
    self.associationCtrl.Enable()
    inheritedEnv = self.environmentList.inheritedEnvironment()
    if (inheritedEnv != '' and self.theAssetId != None):
      p = self.dbProxy.inheritedAssetProperties(self.theAssetId,inheritedEnv)
      self.theEnvironmentDictionary[environmentName] = p
      self.propertiesList.setEnvironment(environmentName)
      self.propertiesList.load(p.properties(),p.rationale()) 
      self.associationCtrl.setEnvironment(environmentName)
      self.associationCtrl.load(p.associations())


  def OnDeleteEnvironment(self,evt):
    selectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(selectedIdx)
    del self.theEnvironmentDictionary[environmentName]
    self.theSelectedIdx = -1
    self.propertiesList.setEnvironment('')
    self.propertiesList.DeleteAllItems()
    self.associationCtrl.setEnvironment('')
    self.associationCtrl.DeleteAllItems()
    self.propertiesList.Disable()
    self.associationCtrl.Disable()

  def environmentProperties(self):
    if (self.theSelectedIdx != -1):
      environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
      syProperties,pRationale = self.propertiesList.properties()
      self.theEnvironmentDictionary[environmentName] = AssetEnvironmentProperties(environmentName,syProperties,pRationale,self.associationCtrl.dimensions())
    return self.theEnvironmentDictionary.values() 
