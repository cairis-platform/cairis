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
from CodeRelationshipListCtrl import CodeRelationshipListCtrl
from CodeNetworkModel import CodeNetworkModel
from Borg import Borg

class CodeRelationshipEditor(wx.Dialog):
  def __init__(self,parent,personaName):
    wx.Dialog.__init__(self,parent,armid.CODERELATIONSHIPEDITOR_ID,'Code Relationships',style=wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX | wx.THICK_FRAME | wx.RESIZE_BORDER, size=(400,200))
    b = Borg()
    self.dbProxy = b.dbProxy
    self.thePersonaName = personaName
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.crListCtrl = CodeRelationshipListCtrl(self,personaName)
    mainSizer.Add(self.crListCtrl,1,wx.EXPAND)

    buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(buttonSizer,0,wx.EXPAND | wx.ALIGN_CENTER)
    commitButton = wx.Button(self,armid.CODERELATIONSHIP_BUTTONCOMMIT_ID,"Commit")
    buttonSizer.Add(commitButton)
    closeButton = wx.Button(self,wx.ID_CLOSE,"Close")
    buttonSizer.Add(closeButton)

    self.SetSizer(mainSizer)

    self.selectedIdx = -1
    wx.EVT_BUTTON(self,armid.CODERELATIONSHIP_BUTTONCOMMIT_ID,self.onCommit)
    wx.EVT_BUTTON(self,wx.ID_CLOSE,self.onClose)

  def onCommit(self,evt):
    relationships = self.crListCtrl.dimensions()
    self.dbProxy.updateCodeNetwork(self.thePersonaName,relationships)
    model = CodeNetworkModel(relationships,self.thePersonaName)
    model.graph()
    self.EndModal(armid.CODERELATIONSHIP_BUTTONCOMMIT_ID)


  def onClose(self,evt):
    self.EndModal(wx.ID_CLOSE)

