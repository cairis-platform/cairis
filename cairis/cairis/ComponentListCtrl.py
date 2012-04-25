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
from TraceableList import TraceableList
from ComponentDialog import ComponentDialog
from ComponentParameters import ComponentParameters

class ComponentListCtrl(TraceableList):
  def __init__(self,parent,winId = armid.COMPONENTVIEW_LISTCOMPONENTS_ID):
    TraceableList.__init__(self,parent,winId,'component')
    self.theParentDialog = parent
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theSelectedLabel = ""
    self.theSelectedIdx = -1
    self.theViewName = ''
    self.theComponents = []
    self.InsertColumn(0,'Component')
    self.SetColumnWidth(0,100)
    self.InsertColumn(1,'Description')
    self.SetColumnWidth(1,100)
    self.InsertColumn(2,'Interface')
    self.SetColumnWidth(2,100)
    self.theSelectedIdx = -1
    self.theTraceMenu.Append(armid.AA_MENUADD_ID,'Add')
    self.theTraceMenu.Append(armid.AA_MENUDELETE_ID,'Delete')
    self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK,self.onRightClick)
    wx.EVT_MENU(self.theTraceMenu,armid.AA_MENUADD_ID,self.onAddComponent)
    wx.EVT_MENU(self.theTraceMenu,armid.AA_MENUDELETE_ID,self.onDeleteComponent)

    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.onComponentActivated)

  def setView(self,cvName): self.theViewName = cvName

  def onAddComponent(self,evt):
    dlg = ComponentDialog(self)
    if (dlg.ShowModal() == armid.COMPONENT_BUTTONCOMMIT_ID):
      parameters = dlg.parameters()
      self.theSelectedIdx = self.GetItemCount()
      self.InsertStringItem(self.theSelectedIdx,parameters.name())
      self.SetStringItem(self.theSelectedIdx,1,parameters.description())
      self.theComponents.append(parameters)

  def onDeleteComponent(self,evt):
    if (self.theSelectedIdx == -1):
      errorText = 'No component selected'
      errorLabel = 'Delete component'
      dlg = wx.MessageDialog(self,errorText,errorLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
    else:
      selectedValue = self.GetItemText(self.theSelectedIdx)
      self.DeleteItem(self.theSelectedIdx)
      del self.theComponents[self.theSelectedIdx]

  
  def OnItemSelected(self,evt):
    self.theSelectedLabel = evt.GetLabel()
    self.theSelectedIdx = evt.GetIndex()

  def OnItemDeselected(self,evt):
    self.theSelectedIdx = -1

  def onComponentActivated(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    dlg = ComponentDialog(self)
    inParameters = self.theComponents[self.theSelectedIdx]
    dlg.load(inParameters)
    if (dlg.ShowModal() == armid.COMPONENT_BUTTONCOMMIT_ID):
      outParameters = dlg.parameters()
      self.theComponents[self.theSelectedIdx] = outParameters
      self.SetStringItem(self.theSelectedIdx,0,outParameters.name())
      self.SetStringItem(self.theSelectedIdx,1,outParameters.description())

  def load(self,components):
    self.theComponents = components
    for p in self.theComponents:
      idx = self.GetItemCount()
      self.InsertStringItem(idx,p.name())
      self.SetStringItem(idx,1,p.description())

  def dimensions(self):
    return self.theComponents
