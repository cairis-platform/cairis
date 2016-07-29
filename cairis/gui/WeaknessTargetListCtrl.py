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
from cairis.core.armid import *
from cairis.core.ARM import *
from cairis.core.Borg import Borg
from WeaknessTreatmentDialog import WeaknessTreatmentDialog

__author__ = 'Shamal Faily'

class WeaknessTargetListCtrl(wx.ListCtrl):
  def __init__(self,parent,winId,cvName):
    wx.ListCtrl.__init__(self,parent,winId,size=wx.DefaultSize,style=wx.LC_REPORT)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theViewName = cvName
    self.theComponents = []
    self.InsertColumn(0,'Target')
    self.SetColumnWidth(0,100)
    self.InsertColumn(1,'Components')
    self.SetColumnWidth(1,250)
    self.InsertColumn(2,'Assets')
    self.SetColumnWidth(2,250)
    self.theSelectedIdx = -1
    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.onTargetActivated)

  def OnItemSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()

  def OnItemDeselected(self,evt):
    self.theSelectedIdx = -1

  def onTargetActivated(self,evt):
    try:
      targetName = evt.GetLabel()
      target = self.theTargets[targetName]
      dlg = WeaknessTreatmentDialog(self,targetName,self.theViewName,target.requirement(),target.asset(),target.effectiveness())  
      if (dlg.ShowModal() == WEAKNESSTREATMENT_BUTTONCOMMIT_ID):
        target.addTreatment(dlg.requirement(),dlg.asset(),dlg.effectiveness(),dlg.rationale())
        self.theTargets[targetName] = target
      dlg.Destroy()
    except KeyError:
      return

  def load(self,targets):
    self.theTargets = targets
    for targetKey in targets:
      idx = self.GetItemCount()
      self.InsertStringItem(idx,targetKey)
      target = targets[targetKey]      
      self.SetStringItem(idx,1,",".join(target.components()))
      self.SetStringItem(idx,2,",".join(target.templateAssets()))

  def dimensions(self):
    return self.theTargets
