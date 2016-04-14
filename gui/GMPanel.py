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
import os
import armid
from EditorBase import EditorBase
from GoalsGrid import GoalsGrid
from datetime import datetime

NAME_POS = 0
DEFINITION_POS = 1
CATEGORY_POS = 2
PRIORITY_POS = 3
FITCRITERION_POS = 4
ISSUE_POS = 5
ORIGINATOR_POS = 6

class GMPanel(EditorBase):
  def __init__(self,parent,id):
    self.objectDimension = 'goal'
    self.objectLabel = 'Goals'
    self.statusBar = parent.statusBar
    EditorBase.__init__(self,parent,id)
    self.grid = GoalsGrid(self,self.modCombo,self.envCombo)
    self.sizer.Add( self.grid,1,wx.EXPAND )
    self.resizeColumns()
    self.SetSizeHints(1150,400)
    self.SetSizer(self.sizer)
#    self.updateEnvironments()
    self.Bind(wx.EVT_COMBOBOX, self.onObjectChange,id = armid.RMFRAME_TOOL_COMBOOBJECT)
    self.Bind(wx.EVT_COMBOBOX, self.onEnvironmentChange,id = armid.RMFRAME_TOOL_COMBOENVIRONMENT)

    
  def onObjectChange(self,evt):
    goalName = self.modCombo.GetValue()
    if (goalName == ''):
      envNames = ['']
      envNames += self.dbProxy.getDimensionNames('environment')
      self.envCombo.SetItems(envNames)
      self.envCombo.SetValue('')
    else:
      self.updateEnvironments()
    self.updateObjectSelection(goalName)
    self.refresh()


  def updateEnvironments(self):
    goalName = self.modCombo.GetValue()
    envs = self.dbProxy.goalEnvironments(goalName)
    self.envCombo.SetItems(envs)
    if (len(envs) > 0):
      self.envCombo.SetValue(envs[1])
    


  def resizeColumns(self):
    self.grid.SetColSize(NAME_POS,150)
    self.grid.SetColSize(DEFINITION_POS,300)
    self.grid.SetColSize(CATEGORY_POS,100)
    self.grid.SetColSize(PRIORITY_POS,70)
    self.grid.SetColSize(FITCRITERION_POS,250)
    self.grid.SetColSize(ISSUE_POS,100)
    self.grid.SetColSize(ORIGINATOR_POS,75)
    self.grid.SetDefaultRowSize(35)


  def updateObjectSelection(self,selectedGoal = ''):
    goalName = self.modCombo.GetValue()
    self.modCombo.Clear()

    envName = self.envCombo.GetValue()
    goalMods = ['']
    if (selectedGoal == ''):
      goalMods = self.dbProxy.getDimensionNames(self.objectDimension,envName)
    else:
      goalMods = self.dbProxy.getSubGoalNames(goalName,envName)

    goalMods.sort()
    self.modCombo.SetItems(goalMods)
    if (selectedGoal != ''):
      self.modCombo.SetStringSelection(selectedGoal)
    self.refresh()

  def onEnvironmentChange(self,evt):
    goalName = self.modCombo.GetValue()
    envName = self.envCombo.GetValue()
    goalMods = self.dbProxy.getSubGoalNames(goalName,envName)
    self.modCombo.SetItems(goalMods)
    self.refresh()

  def relabel(self):
    envName = self.envCombo.GetValue()
    self.dbProxy.relabelGoals(envName)
    self.statusBar.SetStatusText(str(datetime.now())[:19] + ' : goals relabelled')


  def addObject(self):
    envName = self.envCombo.GetValue()
    if envName == '':
      dlg = wx.MessageDialog(self,'Environment not set','Add goal',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
    else:
      grid = self.FindWindowById(armid.ID_REQGRID)
      pos = grid.GetGridCursorRow()
      grid.InsertRows(pos)

