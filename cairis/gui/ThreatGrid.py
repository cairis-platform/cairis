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
import wx.grid
from cairis.core.armid import *

class ThreatTable(wx.grid.PyGridTableBase):
  def __init__(self,threats):
    wx.grid.PyGridTableBase.__init__(self)
    self.colLabels = ['Threat','Likelihood']
    self.data = {}
    idx = 0
    for threat,likelihood in threats:
      self.data[(idx,0)] = threat
      self.data[(idx,1)] = likelihood
    self.likelihoodChoices = ['Incredible','Improbable','Remote','Occasional','Probable','Frequent']

  def GetNumberRows(self):
    return len(self.data) / 2

  def GetNumberCols(self):
    return 2

  def GetColLabelValue(self,col):
    return self.colLabels[col]

  def IsEmptyCell(self,row,col):
    return False

  def GetValue(self,row,col):
    return self.data.get((row,col))

  def SetValue(self,row,col,value):
    self.data[(row,col)] = value

  def addThreat(self,threatName):
    pos = (len(self.data) / 2)
    self.data[(pos,0)] = threatName
    self.data[(pos,1)] = ''
    grid = self.GetView()
    if grid:
      grid.BeginBatch()
      msg = wx.grid.GridTableMessage(self,wx.grid.GRIDTABLE_NOTIFY_ROWS_INSERTED,pos,1)
      grid.ProcessTableMessage(msg)
      grid.SetReadOnly(pos,0)
      grid.SetCellEditor(pos,1,wx.grid.GridCellChoiceEditor(self.likelihoodChoices))
      grid.EndBatch()

  def load(self,threats):
    idx = 0
    grid = self.GetView()
    if grid:
      for idx, threat in enumerate(threats):
        self.data[(idx,0)] = threat[0]
        self.data[(idx,1)] = threat[1]
        grid.BeginBatch()
        msg = wx.grid.GridTableMessage(self,wx.grid.GRIDTABLE_NOTIFY_ROWS_INSERTED,idx,1)
        grid.ProcessTableMessage(msg)
        grid.EndBatch()

  def AppendRows(self,numRows = 1):
    pos = (len(self.data) / 2) - 1
    self.InsertRows(pos,numRows)
    
  def InsertRows(self,pos,numRows = 1):
    newPos = pos + 1
    grid = self.GetView()
    if grid:
      grid.BeginBatch()
      msg = wx.grid.GridTableMessage(self,wx.grid.GRIDTABLE_NOTIFY_ROWS_INSERTED,newPos,numRows)
      grid.ProcessTableMessage(msg)
      grid.EndBatch()
      grid.SetCellEditor(pos,1,wx.grid.GridCellChoiceEditor(self.likelihoodChoices))
    return newPos

  def DeleteRows(self,pos,numRows = 1):
    del self.data[(pos,0)]
    del self.data[(pos,1)]
    grid = self.GetView()
    if grid:
      grid.BeginBatch()
      msg = wx.grid.GridTableMessage(self,wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED,pos,numRows)
      grid.ProcessTableMessage(msg)
      grid.EndBatch()


class ThreatGrid(wx.grid.Grid):
  def __init__(self,parent,threats):
    wx.grid.Grid.__init__(self,parent,ENVIRONMENT_GRIDTHREATS_ID)
    self.SetTable(ThreatTable(threats))
    self.SetRowLabelSize(0)
    for x in range(self.GetNumberRows()):
      self.SetReadOnly(x,0)
      self.SetCellEditor(x,1,wx.grid.GridCellChoiceEditor(self.likelihoodChoices))
    self.SetColSize(0,200)
    self.SetColSize(1,200)



  def addThreat(self,threatName):
    grid = self.GetTable()
    grid.addThreat(threatName)


  def threats(self):
    grid = self.GetTable()
    threatList = []
    for x in range(0,self.GetNumberRows()):
      threatList.append( (grid.GetValue(x,0), grid.GetValue(x,1) ) )
    return threatList 

  def deleteThreat(self):
    currentRowIndex = self.GetGridCursorRow()
    self.DeleteRows(currentRowIndex)
 
  def load(self,threats):
    grid = self.GetTable()
    grid.load(threats)
    for x in range(self.GetNumberRows()):
      self.SetReadOnly(x,0)
      self.SetCellEditor(x,1,wx.grid.GridCellChoiceEditor(grid.likelihoodChoices))
