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
from CodeRelationshipDialog import CodeRelationshipDialog

class CodeNetworkPanel(BasePanel):
  def __init__(self,parent,personaName,codeNet):
    BasePanel.__init__(self,parent,armid.CODENETWORK_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theCodeNetwork = codeNet

    self.theViewMenu = wx.Menu()
    self.theViewMenu.Append(armid.CNV_MENU_ADD_ID,'Add')
    wx.EVT_MENU(self,armid.CNV_MENU_ADD_ID,self.onAddRelationship)

    mainSizer = wx.BoxSizer(wx.VERTICAL)
    personas = self.dbProxy.getDimensionNames('persona')
    mainSizer.Add(self.buildComboSizerList('Persona',(87,30),armid.CODENETWORK_COMBOPERSONA_ID,personas),0,wx.EXPAND)

    cnBox = wx.StaticBox(self,-1,'Code Network')
    cnSizer = wx.StaticBoxSizer(cnBox,wx.HORIZONTAL)
    mainSizer.Add(cnSizer,1,wx.EXPAND)
    self.codeNetView = CodeNetworkView(self,armid.CODENETWORK_IMAGENETWORK_ID)
    self.codeNetView.reloadImage()
    cnSizer.Add(self.codeNetView,1,wx.EXPAND)

    self.personaCtrl = self.FindWindowById(armid.CODENETWORK_COMBOPERSONA_ID)
    self.personaCtrl.SetValue(personaName)
    self.personaCtrl.Bind(wx.EVT_COMBOBOX,self.onPersonaChange)
    self.SetSizer(mainSizer)


  def onPersonaChange(self,evt):
    personaName = self.personaCtrl.GetValue()
    self.regenerateView(personaName)

  def regenerateView(self,personaName):
    self.theCodeNetwork = CodeNetworkModel(self.dbProxy.personaCodeNetwork(personaName),personaName)
    self.theCodeNetwork.graph()
    self.codeNetView.reloadImage()

  def onAddRelationship(self,evt):
    personaName = self.personaCtrl.GetValue()
    dlg = CodeRelationshipDialog(self)
    if (dlg.ShowModal() == armid.CODERELATIONSHIP_BUTTONADD_ID):
      fromName = dlg.fromName()
      toName = dlg.toName()
      rshipType = dlg.relationship()
      b = Borg()
      b.dbProxy.addCodeRelationship(personaName,fromName,toName,rshipType)
      self.regenerateView(personaName)
    dlg.Destroy() 
