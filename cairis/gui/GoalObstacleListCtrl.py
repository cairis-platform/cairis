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
from GoalObstacleDialog import GoalObstacleDialog

__author__ = 'Shamal Faily'

class GoalObstacleListCtrl(wx.ListCtrl):
  def __init__(self,parent,winId,cvName,envName):
    wx.ListCtrl.__init__(self,parent,winId,size=wx.DefaultSize,style=wx.LC_REPORT)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theViewName = cvName
    self.theEnvironmentName = envName
    self.theGOFlags = {}
    self.InsertColumn(0,'Goal')
    self.SetColumnWidth(0,200)
    self.InsertColumn(1,'Obstacle')
    self.SetColumnWidth(1,200)
    self.InsertColumn(2,'Add/Ignore')
    self.SetColumnWidth(2,100)
    self.theSelectedIdx = -1
    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.onItemActivated)

    gos = self.dbProxy.candidateGoalObstacles(cvName,envName)

    for goalName,obsName in gos:
      idx = self.GetItemCount()
      self.InsertStringItem(idx,goalName)
      self.SetStringItem(idx,1,obsName)
      self.SetStringItem(idx,2,'Ignore')
      self.theGOFlags[(goalName,obsName)] = False

  def OnItemSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()

  def OnItemDeselected(self,evt):
    self.theSelectedIdx = -1

  def onItemActivated(self,evt):
    try:
      self.theSelectedIdx = evt.GetIndex()
      goalName = self.GetItemText(self.theSelectedIdx)
      obsItem = self.GetItem(self.theSelectedIdx,1)
      obsName = obsItem.GetText()
      dlg = GoalObstacleDialog(self,goalName,obsName,self.theEnvironmentName) 
      if (dlg.ShowModal() == GOALOBSTACLE_BUTTONCOMMIT_ID):
        self.theGOFlags[(goalName,obsName)] = dlg.ignore()
        if (dlg.ignore() == True):
          self.SetStringItem(self.theSelectedIdx,2,'Ignore')
        else:
          self.SetStringItem(self.theSelectedIdx,2,'Add')
      dlg.Destroy()
    except KeyError:
      return

  def dimensions(self):
    dims = []
    for goalName,obsName in self.theGOFlags:
      if self.theGOFlags[(goalName,obsName)] == False:
        dims.append((goalName,obsName)) 
    return dims
