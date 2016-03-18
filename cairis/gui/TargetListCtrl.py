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
from TargetDialog import TargetDialog
from Target import Target

class TargetListCtrl(wx.ListCtrl):
  def __init__(self,parent,winId,boxSize=wx.DefaultSize):
    wx.ListCtrl.__init__(self,parent,winId,size=boxSize,style=wx.LC_REPORT)
    self.theParentWindow = parent
    self.InsertColumn(0,'Target')
    self.SetColumnWidth(0,150)
    self.InsertColumn(1,'Effectiveness')
    self.SetColumnWidth(1,100)
    self.InsertColumn(2,'Rationale')
    self.SetColumnWidth(1,300)
    self.theDimMenu = wx.Menu()
    self.theDimMenu.Append(armid.TARGETLISTCTRL_MENUADD_ID,'Add')
    self.theDimMenu.Append(armid.TARGETLISTCTRL_MENUDELETE_ID,'Delete')
    self.theSelectedValue = ''
    self.theSelectedIdx = -1
    self.setTargets = {}
    self.Bind(wx.EVT_RIGHT_DOWN,self.OnRightDown)
    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.onItemActivated)
    wx.EVT_MENU(self.theDimMenu,armid.TARGETLISTCTRL_MENUADD_ID,self.onAddTarget)
    wx.EVT_MENU(self.theDimMenu,armid.TARGETLISTCTRL_MENUDELETE_ID,self.onDeleteTarget)

  def setEnvironment(self,environmentName):
    self.theCurrentEnvironment = environmentName
    if ((self.theCurrentEnvironment in self.setTargets) == False):
      self.setTargets[self.theCurrentEnvironment] = set([])
 
  def OnItemSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()

  def OnItemDeselected(self,evt):
    self.theSelectedIdx = -1

  def OnRightDown(self,evt):
    self.PopupMenu(self.theDimMenu)

  def onItemActivated(self,evt):
    x = evt.GetIndex()
    targetName = self.GetItemText(x)
    targetEffectiveness = self.GetItem(x,1).GetText()
    eRationale = self.GetItem(x,2).GetText()
    reqCtrl = self.theParentWindow.FindWindowById(armid.COUNTERMEASURE_LISTREQUIREMENTS_ID)
    reqList = reqCtrl.dimensions()
    dlg = TargetDialog(self,reqList,self.setTargets[self.theCurrentEnvironment],self.theCurrentEnvironment)
    dlg.load(targetName,targetEffectiveness,eRationale)
    if (dlg.ShowModal() == armid.TARGET_BUTTONCOMMIT_ID):
      targetName = dlg.target()
      effectivenessValue = dlg.effectiveness()
      eRat = dlg.rationale()
      self.SetStringItem(x,0,targetName)
      self.SetStringItem(x,1,effectivenessValue)
      self.SetStringItem(x,2,eRat)
      (self.setTargets[self.theCurrentEnvironment]).add(targetName)

  def onAddTarget(self,evt):
    reqCtrl = self.theParentWindow.FindWindowById(armid.COUNTERMEASURE_LISTREQUIREMENTS_ID)
    reqList = reqCtrl.dimensions()
    if (len(reqList) == 0):
      dlg = wx.MessageDialog(self,'Add target','No requirements selected',wx.OK | wx.ICON_EXCLAMATION)
      dlg.ShowModal()
      dlg.Destroy()
      return
    dlg = TargetDialog(self,reqList,self.setTargets[self.theCurrentEnvironment],self.theCurrentEnvironment)
    if (dlg.ShowModal() == armid.TARGET_BUTTONCOMMIT_ID):
      targetName = dlg.target()
      effectivenessValue = dlg.effectiveness()
      eRat = dlg.rationale()
      idx = self.GetItemCount()
      self.InsertStringItem(idx,targetName)
      self.SetStringItem(idx,1,effectivenessValue)
      self.SetStringItem(idx,2,eRat)
      self.theSelectedValue = targetName
      (self.setTargets[self.theCurrentEnvironment]).add(targetName)

  def onDeleteTarget(self,evt):
    if (self.theSelectedIdx == -1):
      errorText = 'No target selected'
      errorLabel = 'Delete mitigation target'
      dlg = wx.MessageDialog(self,errorText,errorLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
    else:
      selectedValue = self.GetItemText(self.theSelectedIdx)
      self.DeleteItem(self.theSelectedIdx)
      (self.setTargets[self.theCurrentEnvironment]).remove(selectedValue)

  def load(self,targets):
    for idx,target in enumerate(targets):
      targetName = target.name()
      self.InsertStringItem(idx,targetName)
      self.SetStringItem(idx,1,target.effectiveness())
      self.SetStringItem(idx,2,target.rationale())
      (self.setTargets[self.theCurrentEnvironment]).add(targetName)

  def targets(self):
    targetList = []
    for x in range(self.GetItemCount()):
      targetName = self.GetItemText(x)
      targetEffectiveness = self.GetItem(x,1).GetText()
      eRationale = self.GetItem(x,2).GetText()
      targetList.append(Target(self.GetItemText(x),targetEffectiveness,eRationale))
    return targetList
