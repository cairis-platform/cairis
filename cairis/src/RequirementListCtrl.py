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
from RequirementDialog import RequirementDialog

class RequirementListCtrl(wx.ListCtrl):
  def __init__(self,parent,structCtrl):
    wx.ListCtrl.__init__(self,parent,armid.SECURITYPATTERN_LISTREQUIREMENTS_ID,size=wx.DefaultSize,style=wx.LC_REPORT)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.reqs = {}
    self.theStructureCtrl = structCtrl
    self.InsertColumn(0,'Name')
    self.SetColumnWidth(0,250)
    self.theSelectedIdx = -1
    self.theDimMenu = wx.Menu()
    self.theDimMenu.Append(armid.AA_MENUADD_ID,'Add')
    self.theDimMenu.Append(armid.AA_MENUDELETE_ID,'Delete')
    self.Bind(wx.EVT_RIGHT_DOWN,self.OnRightDown)
    wx.EVT_MENU(self.theDimMenu,armid.AA_MENUADD_ID,self.onAddRequirement)
    wx.EVT_MENU(self.theDimMenu,armid.AA_MENUDELETE_ID,self.onDeleteRequirement)

    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.onRequirementActivated)

  def OnRightDown(self,evt):
    self.PopupMenu(self.theDimMenu)

  def onAddRequirement(self,evt):
    dlg = RequirementDialog(self,self.theStructureCtrl.assets())
    if (dlg.ShowModal() == armid.PATTERNREQUIREMENT_BUTTONCOMMIT_ID):
      self.theSelectedIdx = self.GetItemCount()
      reqName = dlg.name()
      self.InsertStringItem(self.theSelectedIdx,reqName)
      self.reqs[reqName] = (dlg.description(),dlg.type(),dlg.rationale(),dlg.fitCriterion(),dlg.asset())

  def onDeleteRequirement(self,evt):
    if (self.theSelectedIdx == -1):
      errorText = 'No association selected'
      errorLabel = 'Delete asset association'
      dlg = wx.MessageDialog(self,errorText,errorLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
    else:
      selectedValue = self.GetItemText(self.theSelectedIdx)
      self.DeleteItem(self.theSelectedIdx)
      del self.reqs[selectedValue]

  
  def OnItemSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()

  def OnItemDeselected(self,evt):
    self.theSelectedIdx = -1

  def onRequirementActivated(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    reqName = self.GetItemText(self.theSelectedIdx)
    reqData = self.reqs[reqName]
    reqDesc = reqData[0]
    reqType = reqData[1]
    reqRationale = reqData[2]
    reqFC = reqData[3]
    reqAsset = reqData[4]
     
    dlg = RequirementDialog(self,self.theStructureCtrl.assets(),reqName,reqDesc,reqType,reqRationale,reqFC,reqAsset)
    if (dlg.ShowModal() == armid.PATTERNREQUIREMENT_BUTTONCOMMIT_ID):
      del self.reqs[reqName]
      reqName = dlg.name()
      self.SetStringItem(self.theSelectedIdx,0,reqName)
      self.reqs[reqName] = (dlg.description(),dlg.type(),dlg.rationale(),dlg.fitCriterion(),dlg.asset())


  def load(self,reqs):
    for reqName,reqDesc,reqType,reqRationale,reqFC,reqAsset in reqs:
      idx = self.GetItemCount()
      self.InsertStringItem(idx,reqName)
      self.reqs[reqName] = (reqDesc,reqType,reqRationale,reqFC,reqAsset)

  def requirements(self):
    reqs = []
    for x in range(self.GetItemCount()):
      reqName = self.GetItemText(x)
      reqData = self.reqs[reqName]
      reqDesc = reqData[0]
      reqType = reqData[1]
      reqRationale = reqData[2]
      reqFC = reqData[3]
      reqAsset = reqData[4]
      reqs.append((reqName,reqDesc,reqType,reqRationale,reqFC,reqAsset))
    return reqs
