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
from BasePanel import BasePanel
from cairis.core.Borg import Borg

class PersonaImpactPanel(BasePanel):
  def __init__(self,parent,cvName,personaName,envName):
    BasePanel.__init__(self,parent,PERSONAIMPACT_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theTaskIdx = -1
    self.theUseCaseIdx = -1

    self.theImpactRationale = self.dbProxy.personaImpactRationale(cvName,personaName,envName)
    mainSizer = wx.BoxSizer(wx.VERTICAL)

    taskBox = wx.StaticBox(self,-1)
    taskSizer = wx.StaticBoxSizer(taskBox,wx.VERTICAL)

    ucCompSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(taskSizer,1,wx.EXPAND)
    mainSizer.Add(ucCompSizer,1,wx.EXPAND)

    self.theTaskList = wx.ListCtrl(self,PERSONAIMPACT_LISTTASKIMPACT_ID,size=wx.DefaultSize,style=wx.LC_REPORT)
    self.theTaskList.InsertColumn(0,'Task')
    self.theTaskList.SetColumnWidth(0,150)
    self.theTaskList.InsertColumn(1,'Duration')
    self.theTaskList.SetColumnWidth(1,100)
    self.theTaskList.InsertColumn(2,'Frequency')
    self.theTaskList.SetColumnWidth(2,100)
    self.theTaskList.InsertColumn(3,'Demands')
    self.theTaskList.SetColumnWidth(3,100)
    self.theTaskList.InsertColumn(4,'Goals')
    self.theTaskList.SetColumnWidth(4,100)

    taskNames = self.theImpactRationale.keys()
    taskNames.sort()
    
    for idx,taskName in enumerate(taskNames):
      self.theTaskList.InsertStringItem(idx,taskName)
      taskImpact = self.theImpactRationale[taskName]
      self.theTaskList.SetStringItem(idx,1,taskImpact[0]) 
      self.theTaskList.SetStringItem(idx,2,taskImpact[1]) 
      self.theTaskList.SetStringItem(idx,3,taskImpact[2]) 
      self.theTaskList.SetStringItem(idx,4,taskImpact[3]) 
    taskSizer.Add(self.theTaskList,1,wx.EXPAND)

    self.theUcList = wx.ListCtrl(self,PERSONAIMPACT_LISTUSECASES_ID,size=wx.DefaultSize,style=wx.LC_REPORT)
    self.theUcList.InsertColumn(0,'Use Case')
    self.theUcList.SetColumnWidth(0,150)

    self.theComponentList = wx.ListCtrl(self,PERSONAIMPACT_LISTCOMPONENTS_ID,size=wx.DefaultSize,style=wx.LC_REPORT)
    self.theComponentList.InsertColumn(0,'Component')
    self.theComponentList.SetColumnWidth(0,150)

    ucCompListSizer = wx.BoxSizer(wx.HORIZONTAL)
    ucCompSizer.Add(ucCompListSizer,1,wx.EXPAND)

    ucListBox = wx.StaticBox(self,-1)
    ucListBoxSizer = wx.StaticBoxSizer(ucListBox,wx.VERTICAL)
    ucCompListSizer.Add(ucListBoxSizer,1,wx.EXPAND)
    ucListBoxSizer.Add(self.theUcList,1,wx.EXPAND)

    compBox = wx.StaticBox(self,-1)
    compBoxSizer = wx.StaticBoxSizer(compBox,wx.VERTICAL)
    ucCompListSizer.Add(compBoxSizer,1,wx.EXPAND)
    compBoxSizer.Add(self.theComponentList,1,wx.EXPAND)

    self.theTaskList.Bind(wx.EVT_LIST_ITEM_SELECTED,self.onTaskSelected)
    self.theTaskList.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.onTaskDeselected)
    self.theUcList.Bind(wx.EVT_LIST_ITEM_SELECTED,self.onUseCaseSelected)
    self.theUcList.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.onUseCaseDeselected)

    self.SetSizer(mainSizer)

  def loadList(self,aList,listCtrl):
    for idx,item in enumerate(aList):
      listCtrl.InsertStringItem(idx,item)
 
  def onTaskSelected(self,evt):
    self.theTaskIdx = evt.GetIndex()
    taskName = self.theTaskList.GetItemText(self.theTaskIdx)

    self.theUcList.DeleteAllItems()
    self.theComponentList.DeleteAllItems()
 
    taskImpact = self.theImpactRationale[taskName]
    ucDict = taskImpact[4]
    ucNames = ucDict.keys()
    ucNames.sort()
    self.loadList(ucNames,self.theUcList)

  def onTaskDeselected(self,evt):
    self.theTaskIdx = -1
    self.theUcList.DeleteAllItems()
    self.theComponentList.DeleteAllItems()

  def onUseCaseSelected(self,evt):
    self.theUseCaseIdx = evt.GetIndex()
    ucName = self.theUcList.GetItemText(self.theUseCaseIdx)
    self.theComponentList.DeleteAllItems()

    taskName = self.theTaskList.GetItemText(self.theTaskIdx)
    taskImpact = self.theImpactRationale[taskName]

    ucDict = taskImpact[4]
    componentNames = ucDict[ucName]
    componentNames.sort()
    self.loadList(componentNames,self.theComponentList)

  def onUseCaseDeselected(self,evt):
    self.theUseCaseIdx = -1
    self.theComponentList.DeleteAllItems()
