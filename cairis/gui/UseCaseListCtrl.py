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
from ARM import *
from TraceableList import TraceableList
from UseCaseContributionDialog import UseCaseContributionDialog
from DimensionNameDialog import DimensionNameDialog
from ReferenceContribution import ReferenceContribution

class UseCaseListCtrl(TraceableList):

  def __init__(self,parent,winId):
    TraceableList.__init__(self,parent,winId,'usecase')
    self.theParentDialog = parent
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theSelectedLabel = ""
    self.theSelectedIdx = -1
    self.theTraceMenu.Append(armid.CLC_MENU_REFERENCECONTRIBUTION_ID,'Use Case Contribution')
    wx.EVT_MENU(self,armid.CLC_MENU_REFERENCECONTRIBUTION_ID,self.onUseCaseContribution)

    self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onRightClick)
    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)

    self.rsItem = self.theTraceMenu.FindItemById(armid.CLC_MENU_REFERENCECONTRIBUTION_ID)
    self.rsItem.Enable(False)

  def OnItemSelected(self,evt):
    self.theSelectedLabel = evt.GetLabel()
    self.theSelectedIdx = evt.GetIndex()
    self.rsItem.Enable(True)

  def OnItemDeselected(self,evt):
    self.theSelectedLabel = ""
    self.theSelectedIdx = -1
    self.rsItem.Enable(False)

  def onUseCaseContribution(self,evt):
    ucName = self.GetItemText(self.theSelectedIdx)
    ucs  = self.dbProxy.getUseCaseContributions(ucName)
    ucKeys = ucs.keys()
    ucKeys.append('[New Contribution]')
    rsDlg = DimensionNameDialog(self,'usecase_contribution',ucKeys,'Select')
    if (rsDlg.ShowModal() == armid.DIMNAME_BUTTONACTION_ID):
      synName = rsDlg.dimensionName()
      rType = 'reference'
      if (synName != '[New Contribution]'):
        rc,rType = ucs[synName]
      else:
        rc = ReferenceContribution(ucName,'','','')
      dlg = UseCaseContributionDialog(self,rc,rType)
      if (dlg.ShowModal() == armid.REFERENCECONTRIBUTION_BUTTONCOMMIT_ID):
        if (rc.meansEnd() == ''):
          self.dbProxy.addUseCaseContribution(dlg.parameters())
        else:
          self.dbProxy.updateUseCaseContribution(dlg.parameters())

  def selectedLabel(self):
    return self.GetItemText(self.theSelectedIdx)
