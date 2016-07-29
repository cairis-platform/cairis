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
from ExceptionDialog import ExceptionDialog
import cairis.core.ObstacleFactory

__author__ = 'Shamal Faily'

class ExceptionListCtrl(wx.ListCtrl):
  def __init__(self,parent,envName,stepGrid):
    wx.ListCtrl.__init__(self,parent,USECASE_LISTEXCEPTIONS_ID,size=wx.DefaultSize,style=wx.LC_REPORT)
    self.stepGrid = stepGrid
    self.theEnvironmentName = envName
    self.theLastSelection = ''
    self.InsertColumn(0,'Exception')
    self.SetColumnWidth(0,250)

    self.theSelectedIdx = -1
    self.theExcMenu = wx.Menu()
    self.theExcMenu.Append(DIMLIST_MENUADD_ID,'Add')
    self.theExcMenu.Append(DIMLIST_MENUDELETE_ID,'Delete')
    self.theExcMenu.Append(DIMLIST_MENUGENERATE_ID,'Generate Obstacle')
    self.Bind(wx.EVT_RIGHT_DOWN,self.OnRightDown)
    wx.EVT_MENU(self.theExcMenu,DIMLIST_MENUADD_ID,self.onAddException)
    wx.EVT_MENU(self.theExcMenu,DIMLIST_MENUDELETE_ID,self.onDeleteException)
    wx.EVT_MENU(self.theExcMenu,DIMLIST_MENUGENERATE_ID,self.onGenerateObstacle)

    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.onExceptionActivated)

  def setEnvironment(self,envName):
    self.theEnvironmentName = envName

  def OnItemSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    self.theLastSelection = self.GetItemText(self.theSelectedIdx)

  def OnItemDeselected(self,evt):
    self.theSelectedIdx = -1

  def OnRightDown(self,evt):
    self.PopupMenu(self.theExcMenu)

  def onAddException(self,evt):
    dlg = ExceptionDialog(self,self.theEnvironmentName)
    if (dlg.ShowModal() == EXCEPTION_BUTTONCOMMIT_ID):
      exc = dlg.parameters()
      pos = self.stepGrid.GetGridCursorRow()
      table = self.stepGrid.GetTable()
      currentStep = table.steps[pos]
      currentStep.addException(exc)
      table.steps[pos] = currentStep
      self.InsertStringItem(0,exc[0])

  def onDeleteException(self,evt):
    if (self.theSelectedIdx == -1):
      dlg = wx.MessageDialog(self,'No exception selected','Delete exception',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
    else:
      excName = self.GetItemText(self.theSelectedIdx)
      self.DeleteItem(self.theSelectedIdx)
      pos = self.stepGrid.GetGridCursorRow()
      table = self.stepGrid.GetTable()
      currentStep = table.steps[pos]
      currentStep.deleteException(excName)
      table.steps[pos] = currentStep


  def onExceptionActivated(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    excName = self.GetItemText(self.theSelectedIdx)
     
    exc = self.stepGrid.stepException(excName)
    dlg = ExceptionDialog(self,self.theEnvironmentName,exc[0],exc[1],exc[2],exc[3],exc[4])
    if (dlg.ShowModal() == EXCEPTION_BUTTONCOMMIT_ID):
      updExc = dlg.parameters()
      self.stepGrid.setStepException(self.theSelectedIdx,excName,updExc)
      self.SetStringItem(self.theSelectedIdx,0,updExc[0])

  def onGenerateObstacle(self,evt):
    obsParameters = ObstacleFactory.build(self.theEnvironmentName,self.stepGrid.stepException(self.theLastSelection))
    b = Borg()
    obsId = b.dbProxy.addObstacle(obsParameters)
    obsDict = b.dbProxy.getObstacles(obsId)
    obsName = (obsDict.keys())[0]
    dlg = wx.MessageDialog(self,'Generated obstacle: ' + obsName,'Generate obstacle',wx.OK)
    dlg.ShowModal()

  def load(self,excs):
    self.DeleteAllItems()
    for ex in excs:
      idx = self.GetItemCount()
      self.InsertStringItem(idx,ex)
