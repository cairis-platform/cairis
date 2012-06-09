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
from CodeNetworkView import CodeNetworkView
from CodeNetworkModel import CodeNetworkModel

class SpecificationPage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,armid.IMPLIEDPROCESS_PAGESPECIFICATION_ID)
    topSizer = wx.BoxSizer(wx.VERTICAL)
    specBox = wx.StaticBox(self,-1)
    specBoxSizer = wx.StaticBoxSizer(specBox,wx.HORIZONTAL)
    topSizer.Add(specBoxSizer,1,wx.EXPAND)
    self.specificationCtrl = wx.TextCtrl(self,armid.IMPLIEDPROCESS_TEXTSPECIFICATION_ID,'None',style=wx.TE_MULTILINE)
    specBoxSizer.Add(self.specificationCtrl,1,wx.EXPAND)
    self.SetSizer(topSizer)

class RelationshipPage(wx.Panel):
  def __init__(self,parent,personaName):
    wx.Panel.__init__(self,parent,armid.IMPLIEDPROCESS_PAGERELATIONSHIP_ID)
    topSizer = wx.BoxSizer(wx.VERTICAL)
    rshipBox = wx.StaticBox(self,-1)
    rshipBoxSizer = wx.StaticBoxSizer(rshipBox,wx.HORIZONTAL)
    topSizer.Add(rshipBoxSizer,1,wx.EXPAND)
    self.codeRelationships = wx.ListCtrl(self,armid.IMPLIEDPROCESS_LISTRELATIONSHIPS_ID,size=wx.DefaultSize,style=wx.LC_REPORT)
    self.codeRelationships.InsertColumn(0,'From')
    self.codeRelationships.SetColumnWidth(0,150)
    self.codeRelationships.InsertColumn(1,'Relationship')
    self.codeRelationships.SetColumnWidth(1,150)
    self.codeRelationships.InsertColumn(2,'To')
    self.codeRelationships.SetColumnWidth(2,150)
    rshipBoxSizer.Add(self.codeRelationships,1,wx.EXPAND)
    self.buildList(personaName)
    self.SetSizer(topSizer)

  def buildList(self,personaName):
    self.codeRelationships.DeleteAllItems()
    b = Borg()
    for fromName,toName,rType in b.dbProxy.personaCodeNetwork(personaName):
      idx = self.codeRelationships.GetItemCount()
      self.codeRelationships.InsertStringItem(idx,fromName)
      self.codeRelationships.SetStringItem(idx,1,rType)
      self.codeRelationships.SetStringItem(idx,2,toName)


class ImpliedProcessNotebook(wx.Notebook):
  def __init__(self,parent,personaName):
    wx.Notebook.__init__(self,parent,armid.IMPLIEDPROCESS_NOTEBOOKSPECIFICATION_ID)
    p1 = RelationshipPage(self,personaName)
    p2 = SpecificationPage(self)
    self.AddPage(p1,'Relationships')
    self.AddPage(p2,'Specification')


class ImpliedProcessPanel(BasePanel):
  def __init__(self,parent,personaName):
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
    idnSizer.Add(ImpliedProcessNotebook(self,personaName),1,wx.EXPAND)

    self.codeRelationships = self.FindWindowById(armid.IMPLIEDPROCESS_LISTRELATIONSHIPS_ID)
    self.codeRelationships.Bind(wx.EVT_LIST_ITEM_SELECTED,self.onRelationshipAdded)
    self.codeRelationships.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.onRelationshipRemoved)

    self.personaCtrl = self.FindWindowById(armid.IMPLIEDPROCESS_COMBOPERSONA_ID)
    self.personaCtrl.SetValue(personaName)
    self.personaCtrl.Bind(wx.EVT_COMBOBOX,self.onPersonaChange)
    self.SetSizer(mainSizer)
    self.regenerateView(personaName)

  def onRelationshipAdded(self,evt):
    personaName = self.personaCtrl.GetValue()
    idx = evt.GetIndex()
    fromName = self.codeRelationships.GetItemText(idx)
    rType = self.codeRelationships.GetItem(idx,1)
    toName = self.codeRelationships.GetItem(idx,2)
    sKey = (fromName,toName.GetText(),rType.GetText())
    self.theSelectedSet.add(sKey)
    self.regenerateView(personaName)

  def onRelationshipRemoved(self,evt):
    personaName = self.personaCtrl.GetValue()
    idx = evt.GetIndex()
    fromName = self.codeRelationships.GetItemText(idx)
    rType = self.codeRelationships.GetItem(idx,1)
    toName = self.codeRelationships.GetItem(idx,2)
    sKey = (fromName,toName.GetText(),rType.GetText())
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

