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
from Borg import Borg
from PersonaImpactDialog import PersonaImpactDialog

class PersonaImpactListCtrl(wx.ListCtrl):
  def __init__(self,parent,winId,cvName,envName):
    wx.ListCtrl.__init__(self,parent,winId,size=wx.DefaultSize,style=wx.LC_REPORT)
    self.theCvName = cvName
    self.theEnvironmentName = envName
    self.InsertColumn(0,'Persona')
    self.SetColumnWidth(0,150)
    self.InsertColumn(1,'Impact')
    self.SetColumnWidth(1,100)
    self.theSelectedIdx = -1
    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.onPersonaActivated)

    b = Borg()
    for pName,pImpact in b.dbProxy.personasImpact(cvName,envName):
      idx = self.GetItemCount()
      self.InsertStringItem(idx,pName)
      self.SetStringItem(idx,1,pImpact)

  def OnItemSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()

  def OnItemDeselected(self,evt):
    self.theSelectedIdx = -1

  def onPersonaActivated(self,evt):
    personaName = evt.GetLabel()
    dlg = PersonaImpactDialog(self,self.theCvName,personaName,self.theEnvironmentName)
    dlg.ShowModal()
    dlg.Destroy()
