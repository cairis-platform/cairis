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
from TraceabilityPanel import TraceabilityPanel
from Borg import Borg
from MySQLDatabaseProxy import MySQLDatabaseProxy

class TraceabilityEditor(wx.Dialog):
  def __init__(self,parent):
    wx.Dialog.__init__(self,parent,armid.TRACEABILITY_ID,'Traceability Relations',style=wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX | wx.THICK_FRAME | wx.RESIZE_BORDER, size=(700,500))
    b = Borg()
    self.dbProxy = b.dbProxy
    mainSizer = wx.BoxSizer(wx.VERTICAL)

    tcBox = wx.StaticBox(self,-1,'Environment')
    comboSizer = wx.StaticBoxSizer(tcBox,wx.HORIZONTAL)
    environments = self.dbProxy.getDimensionNames('environment')
    self.environmentCtrl = wx.ComboBox(self,armid.TRACEABILITY_COMBOENVIRONMENT_ID,"",choices=environments,size=wx.DefaultSize,style=wx.CB_READONLY)
    mainSizer.Add(comboSizer,0,wx.EXPAND)
    comboSizer.Add(self.environmentCtrl,1,wx.EXPAND)

    self.traceList = wx.ListCtrl(self,armid.TRACEABILITY_LISTTRACES_ID,style=wx.LC_REPORT)
    self.traceList.InsertColumn(0,'From')
    self.traceList.InsertColumn(1,'Name')
    self.traceList.InsertColumn(2,'From')
    self.traceList.InsertColumn(3,'Name')
    self.traceList.SetColumnWidth(0,150)
    self.traceList.SetColumnWidth(1,150)
    self.traceList.SetColumnWidth(2,150)
    self.traceList.SetColumnWidth(3,150)

    
    mainSizer.Add(self.traceList,1,wx.EXPAND)

    buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(buttonSizer,0,wx.EXPAND)
    deleteButton = wx.Button(self,armid.TRACEABILITY_BUTTONDELETE_ID,"Delete")
    buttonSizer.Add(deleteButton)
    closeButton = wx.Button(self,wx.ID_CLOSE,"Close")
    buttonSizer.Add(closeButton)

    self.SetSizer(mainSizer)

    self.selectedIdx = -1
    wx.EVT_LIST_ITEM_SELECTED(self,armid.TRACEABILITY_LISTTRACES_ID,self.onItemSelected)
    wx.EVT_LIST_ITEM_DESELECTED(self,armid.TRACEABILITY_LISTTRACES_ID,self.onItemDeselected)
    wx.EVT_COMBOBOX(self,armid.TRACEABILITY_COMBOENVIRONMENT_ID,self.onEnvironmentChange)
    wx.EVT_BUTTON(self,armid.TRACEABILITY_BUTTONDELETE_ID,self.onDelete)
    wx.EVT_BUTTON(self,wx.ID_CLOSE,self.onClose)

  def onItemSelected(self,evt):
    self.selectedIdx = evt.GetIndex()

  def onItemDeselected(self,evt):
    self.selectedIdx = -1

  def onEnvironmentChange(self,evt):
    environmentName = self.environmentCtrl.GetStringSelection()
    traces = self.dbProxy.removableTraces(environmentName) 
    self.traceList.DeleteAllItems()
    for idx,trace in enumerate(traces):
      self.traceList.InsertStringItem(idx,trace[0])
      self.traceList.SetStringItem(idx,1,trace[1])
      self.traceList.SetStringItem(idx,2,trace[2])
      self.traceList.SetStringItem(idx,3,trace[3])

  def onDelete(self,evt):
    if (self.selectedIdx != -1):
      fromObjt = (self.traceList.GetItem(self.selectedIdx,0)).GetText()
      fromName = (self.traceList.GetItem(self.selectedIdx,1)).GetText()
      toObjt = (self.traceList.GetItem(self.selectedIdx,2)).GetText()
      toName = (self.traceList.GetItem(self.selectedIdx,3)).GetText()
      self.dbProxy.deleteTrace(fromObjt,fromName,toObjt,toName)
      self.traceList.DeleteItem(self.selectedIdx)
      self.selectedIdx = -1

  def onClose(self,evt):
    self.EndModal(wx.ID_CLOSE)

