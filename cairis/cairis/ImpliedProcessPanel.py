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
from Borg import Borg
from BasePanel import BasePanel
from ChannelListCtrl import ChannelListCtrl
from CodeNetworkView import CodeNetworkView
from CodeNetworkModel import CodeNetworkModel

class SummaryPage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,armid.IMPLIEDPROCESS_PAGESUMMARY_ID)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    nameBox = wx.StaticBox(self,-1,'Name')
    nameBoxSizer = wx.StaticBoxSizer(nameBox,wx.HORIZONTAL)
    topSizer.Add(nameBoxSizer,0,wx.EXPAND)
    nameBoxSizer.Add(wx.TextCtrl(self,armid.IMPLIEDPROCESS_TEXTNAME_ID,''),1,wx.EXPAND)

    descBox = wx.StaticBox(self,-1,'Description')
    descBoxSizer = wx.StaticBoxSizer(descBox,wx.HORIZONTAL)
    topSizer.Add(descBoxSizer,1,wx.EXPAND)
    descBoxSizer.Add(wx.TextCtrl(self,armid.IMPLIEDPROCESS_TEXTDESCRIPTION_ID,'None',style=wx.TE_MULTILINE),1,wx.EXPAND)
    self.SetSizer(topSizer)

class SpecificationPage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,armid.IMPLIEDPROCESS_PAGESPECIFICATION_ID)
    topSizer = wx.BoxSizer(wx.VERTICAL)
    self.channelList = ChannelListCtrl(self,armid.IMPLIEDPROCESS_LISTCHANNELS_ID)
    topSizer.Add(self.channelList,1,wx.EXPAND)
    specBox = wx.StaticBox(self,-1)
    specBoxSizer = wx.StaticBoxSizer(specBox,wx.HORIZONTAL)
    topSizer.Add(specBoxSizer,1,wx.EXPAND)
    self.specificationCtrl = wx.TextCtrl(self,armid.IMPLIEDPROCESS_TEXTSPECIFICATION_ID,'None',style=wx.TE_MULTILINE)
    specBoxSizer.Add(self.specificationCtrl,1,wx.EXPAND)
    self.SetSizer(topSizer)

class RelationshipPage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,armid.IMPLIEDPROCESS_PAGERELATIONSHIP_ID)
    topSizer = wx.BoxSizer(wx.VERTICAL)
    rshipBox = wx.StaticBox(self,-1)
    rshipBoxSizer = wx.StaticBoxSizer(rshipBox,wx.HORIZONTAL)
    topSizer.Add(rshipBoxSizer,1,wx.EXPAND)
    self.codeRelationships = wx.ListCtrl(self,armid.IMPLIEDPROCESS_LISTRELATIONSHIPS_ID,size=wx.DefaultSize,style=wx.LC_REPORT)
    self.codeRelationships.InsertColumn(0,'From')
    self.codeRelationships.SetColumnWidth(0,150)
    self.codeRelationships.InsertColumn(1,'Type')
    self.codeRelationships.SetColumnWidth(0,150)
    self.codeRelationships.InsertColumn(2,'Relationship')
    self.codeRelationships.SetColumnWidth(2,150)
    self.codeRelationships.InsertColumn(3,'To')
    self.codeRelationships.SetColumnWidth(3,150)
    self.codeRelationships.InsertColumn(4,'Type')
    self.codeRelationships.SetColumnWidth(4,150)
    rshipBoxSizer.Add(self.codeRelationships,1,wx.EXPAND)
    self.SetSizer(topSizer)

  def buildList(self,personaName):
    self.codeRelationships.DeleteAllItems()
    b = Borg()
    for fromName,fromType,toName,toType,rType in b.dbProxy.personaCodeNetwork(personaName):
      idx = self.codeRelationships.GetItemCount()
      self.codeRelationships.InsertStringItem(idx,fromName)
      self.codeRelationships.SetStringItem(idx,1,fromType)
      self.codeRelationships.SetStringItem(idx,2,rType)
      self.codeRelationships.SetStringItem(idx,3,toName)
      self.codeRelationships.SetStringItem(idx,4,toType)

  def highlightSet(self,rshipSet):
    for idx in range(self.codeRelationships.GetItemCount()):
      fromName = self.codeRelationships.GetItemText(idx)
      fromTypeItem = self.codeRelationships.GetItem(idx,1)
      rtItem = self.codeRelationships.GetItem(idx,2)
      toItem = self.codeRelationships.GetItem(idx,3)
      toTypeItem = self.codeRelationships.GetItem(idx,4)
      fromType = fromTypeItem.GetText()
      rtName = rtItem.GetText()
      toName = toItem.GetText()
      toType = toTypeItem.GetText()
      if (fromName,fromType,toName,toType,rtName) in rshipSet:
        self.codeRelationships.Select(idx) 


class ImpliedProcessNotebook(wx.Notebook):
  def __init__(self,parent):
    wx.Notebook.__init__(self,parent,armid.IMPLIEDPROCESS_NOTEBOOKSPECIFICATION_ID)
    p1 = SummaryPage(self)
    p2 = RelationshipPage(self)
    p3 = SpecificationPage(self)
    self.AddPage(p1,'Summary')
    self.AddPage(p2,'Relationships')
    self.AddPage(p3,'Specification')


class ImpliedProcessPanel(BasePanel):
  def __init__(self,parent,isCreate):
    BasePanel.__init__(self,parent,armid.IMPLIEDPROCESS_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theSelectedSet = set([])
    self.theGraphName = 'impliedProc'

    mainSizer = wx.BoxSizer(wx.VERTICAL)
    personas = self.dbProxy.getDimensionNames('persona')
    mainSizer.Add(self.buildComboSizerList('Persona',(87,30),armid.IMPLIEDPROCESS_COMBOPERSONA_ID,personas),0,wx.EXPAND)

    cnBox = wx.StaticBox(self,-1,'Code Network')
    cnSizer = wx.StaticBoxSizer(cnBox,wx.HORIZONTAL)
    mainSizer.Add(cnSizer,1,wx.EXPAND)
    self.codeNetView = CodeNetworkView(self,armid.IMPLIEDPROCESS_IMAGENETWORK_ID,self.theGraphName)

    cnSizer.Add(self.codeNetView,1,wx.EXPAND)

    idnSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(idnSizer,1,wx.EXPAND)
    idnSizer.Add(ImpliedProcessNotebook(self),1,wx.EXPAND)

    self.codeRelationships = self.FindWindowById(armid.IMPLIEDPROCESS_LISTRELATIONSHIPS_ID)
    self.codeRelationships.Bind(wx.EVT_LIST_ITEM_SELECTED,self.onRelationshipAdded)
    self.codeRelationships.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.onRelationshipRemoved)

    self.personaCtrl = self.FindWindowById(armid.IMPLIEDPROCESS_COMBOPERSONA_ID)
    self.personaCtrl.Bind(wx.EVT_COMBOBOX,self.onPersonaChange)

    mainSizer.Add(self.buildCommitButtonSizer(armid.IMPLIEDPROCESS_BUTTONCOMMIT_ID,isCreate),0,wx.ALIGN_CENTER)

    self.SetSizer(mainSizer)

  def loadControls(self,implProc):
    nameCtrl = self.FindWindowById(armid.IMPLIEDPROCESS_TEXTNAME_ID)
    descCtrl = self.FindWindowById(armid.IMPLIEDPROCESS_TEXTDESCRIPTION_ID)
    specCtrl = self.FindWindowById(armid.IMPLIEDPROCESS_TEXTSPECIFICATION_ID)
    nameCtrl.SetValue(implProc.name())
    descCtrl.SetValue(implProc.description())
    personaName = implProc.persona()
    self.personaCtrl.SetValue(personaName)
    self.theSelectedSet = set(implProc.network())

    relationshipPage = self.FindWindowById(armid.IMPLIEDPROCESS_PAGERELATIONSHIP_ID)
    relationshipPage.buildList(personaName)
    relationshipPage.highlightSet(self.theSelectedSet)
    self.regenerateView(personaName)
    specCtrl.SetValue(implProc.specification())

  def onRelationshipAdded(self,evt):
    personaName = self.personaCtrl.GetValue()
    idx = evt.GetIndex()
    fromName = self.codeRelationships.GetItemText(idx)
    fromType = self.codeRelationships.GetItem(idx,1)
    rType = self.codeRelationships.GetItem(idx,2)
    toName = self.codeRelationships.GetItem(idx,3)
    toType = self.codeRelationships.GetItem(idx,4)
    sKey = (fromName,fromType.GetText(),toName.GetText(),toType.GetText(),rType.GetText())
    self.theSelectedSet.add(sKey)
    self.regenerateView(personaName)

  def onRelationshipRemoved(self,evt):
    personaName = self.personaCtrl.GetValue()
    idx = evt.GetIndex()
    fromName = self.codeRelationships.GetItemText(idx)
    fromType = self.codeRelationships.GetItem(idx,1)
    rType = self.codeRelationships.GetItem(idx,2)
    toName = self.codeRelationships.GetItem(idx,3)
    toType = self.codeRelationships.GetItem(idx,4)
    sKey = (fromName,fromType.GetText(),toName.GetText(),toType.GetText(),rType.GetText())
    self.theSelectedSet.remove(sKey)
    self.regenerateView(personaName)

  def onPersonaChange(self,evt):
    personaName = self.personaCtrl.GetValue()
    self.theSelectedSet = set([])
    self.rshipPage = self.FindWindowById(armid.IMPLIEDPROCESS_PAGERELATIONSHIP_ID)
    self.rshipPage.buildList(personaName)
    self.regenerateView(personaName)

  def regenerateView(self,personaName):
    self.theCodeNetwork = CodeNetworkModel(list(self.theSelectedSet),personaName,self.theGraphName)
    self.theCodeNetwork.graph()
    self.codeNetView.reloadImage()

  def dimensions(self):  return list(self.theSelectedSet)
