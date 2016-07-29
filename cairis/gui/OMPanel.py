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
from cairis.core.armid import *
from EditorBase import EditorBase
from ObstaclesGrid import ObstaclesGrid
from datetime import datetime

__author__ = 'Shamal Faily'

NAME_POS = 0
DEFINITION_POS = 1
CATEGORY_POS = 2
ORIGINATOR_POS = 3

class OMPanel(EditorBase):
  def __init__(self,parent,id):
    self.objectDimension = 'obstacle'
    self.objectLabel = 'Obstacles'
    self.statusBar = parent.statusBar
    EditorBase.__init__(self,parent,id)
    self.grid = ObstaclesGrid(self,self.modCombo,self.envCombo)
    self.sizer.Add( self.grid,1,wx.EXPAND )
    self.resizeColumns()
    self.SetSizeHints(1150,400)
    self.SetSizer(self.sizer)
    self.Bind(wx.EVT_COMBOBOX, self.onObjectChange,id = RMFRAME_TOOL_COMBOOBJECT)
    self.Bind(wx.EVT_COMBOBOX, self.onEnvironmentChange,id = RMFRAME_TOOL_COMBOENVIRONMENT)

    
  def onObjectChange(self,evt):
    obsName = self.modCombo.GetValue()
    self.updateObjectSelection(obsName)
    self.refresh()


  def updateEnvironments(self):
    obsName = self.modCombo.GetValue()
    envs = self.dbProxy.obstacleEnvironments(obsName)
    self.envCombo.SetItems(envs)
    if (len(envs) > 0):
      self.envCombo.SetValue(envs[1])
    


  def resizeColumns(self):
    self.grid.SetColSize(NAME_POS,200)
    self.grid.SetColSize(DEFINITION_POS,450)
    self.grid.SetColSize(CATEGORY_POS,150)
    self.grid.SetColSize(ORIGINATOR_POS,150)
    self.grid.SetDefaultRowSize(35)


  def updateObjectSelection(self,selectedObs = ''):
    obsName = self.modCombo.GetValue()
    if (obsName != ''):
      self.updateEnvironments()
    else:
      self.envCombo.Clear()
      self.envCombo.SetItems([''])
      self.envCombo.SetValue('')

    self.modCombo.Clear()

    envName = self.envCombo.GetValue()
    if (selectedObs == ''):
      obsMods = self.dbProxy.getDimensionNames(self.objectDimension,envName)
    else:
      obsMods = self.dbProxy.getSubObstacleNames(obsName,envName)

    obsMods.sort()
    self.modCombo.SetItems(obsMods)
    if (selectedObs != ''):
      self.modCombo.SetStringSelection(selectedObs)
    self.refresh()

  def onEnvironmentChange(self,evt):
    obsName = self.modCombo.GetValue()
    envName = self.envCombo.GetValue()
    obsMods = self.dbProxy.getSubObstacleNames(obsName,envName)
    self.modCombo.SetItems(obsMods)
    self.refresh()

  def relabel(self):
    envName = self.envCombo.GetValue()
    self.dbProxy.relabelObstacles(envName)
    self.statusBar.SetStatusText(str(datetime.now())[:19] + ' : obstacles relabelled')

  def addObject(self):
    grid = self.FindWindowById(ID_REQGRID)
    pos = grid.GetGridCursorRow()
    grid.InsertRows(pos)

