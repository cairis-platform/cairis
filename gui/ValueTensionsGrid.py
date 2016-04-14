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


#$URL$ $Id: StepGrid.py 391 2011-01-04 17:00:43Z shaf $
import wx
import wx.grid
from ARM import *
import armid
from Borg import Borg

AN_POS = 0
PAN_POS = 1
UNL_POS = 2
UNO_POS = 3

C_POS = 0
I_POS = 1
UNL_POS = 2
UNO_POS = 3

class ValueTensionsTable(wx.grid.PyGridTableBase):

  def __init__(self,s = None):
    wx.grid.PyGridTableBase.__init__(self)
    self.colLabels = ['Anonymity','Pseudonymity','Unlinkability','Unobservability']
    self.rowLabels = ['Confidentiality','Integrity','Availability','Accountability']
    if (s != None):
      self.theRows = s
    else:
      self.theRows = {}
      self.theRows[(0,4)] = (0,'None')
      self.theRows[(0,5)] = (0,'None')
      self.theRows[(0,6)] = (0,'None')
      self.theRows[(0,7)] = (0,'None')
      self.theRows[(1,4)] = (0,'None')
      self.theRows[(1,5)] = (0,'None')
      self.theRows[(1,6)] = (0,'None')
      self.theRows[(1,7)] = (0,'None')
      self.theRows[(2,4)] = (0,'None')
      self.theRows[(2,5)] = (0,'None')
      self.theRows[(2,6)] = (0,'None')
      self.theRows[(2,7)] = (0,'None')
      self.theRows[(3,4)] = (0,'None')
      self.theRows[(3,5)] = (0,'None')
      self.theRows[(3,6)] = (0,'None')
      self.theRows[(3,7)] = (0,'None')

  def GetNumberRows(self):
    return 4

  def GetNumberCols(self):
    return 4

  def GetColLabelValue(self,col):
    return self.colLabels[col]

  def GetRowLabelValue(self,col):
    return self.rowLabels[col]

  def IsEmptyCell(self,row,col):
    return False

  def GetValue(self,row,col):
    value,vRationale = self.theRows[(row,col+4)]
    if value == 1:
      return '+'
    elif value == -1:
      return '-'
    else:
      return ' '

  def SetValue(self,row,col,value):
    grid = self.GetView()
    tRationale = grid.rationaleCtrl.GetValue()
    if value == '+':
      self.theRows[(row,col+4)] = (1,tRationale)
    elif value == '-': 
      self.theRows[(row,col+4)] = (-1,tRationale)
    else: 
      self.theRows[(row,col+4)] = (0,tRationale)
   
class ValueTensionsGrid(wx.grid.Grid):
  def __init__(self,parent):
    wx.grid.Grid.__init__(self,parent,armid.ENVIRONMENT_GRIDVALUETENSIONS_ID,wx.DefaultPosition,wx.Size(150,135))
    b = Borg()
    self.dbProxy = b.dbProxy
    self.rationaleCtrl = None
    self.thePanel = parent
    self.setTable()

  def setRationaleCtrl(self,rCtrl):
    self.rationaleCtrl = rCtrl

  def tensions(self):
    table = self.GetTable()
    return table.theRows

  def rationale(self,rowNo,colNo):
    table = self.GetTable()
    tValue,tRationale = table.theRows[(rowNo,colNo + 4)]
    return tRationale

  def setRationale(self,rowNo,colNo,tRationale):
    table = self.GetTable()
    tValue,oldRationale = table.theRows[(rowNo,colNo + 4)]
    table.theRows[(rowNo,colNo + 4)] = (tValue,tRationale)
    
  def setTable(self,rows = None):
    self.SetTable(ValueTensionsTable(rows))
    tChoices = [' ','+','-']
    for x in range(self.GetNumberRows()):
      self.SetCellEditor(x,AN_POS,wx.grid.GridCellChoiceEditor(tChoices))
      self.SetCellEditor(x,PAN_POS,wx.grid.GridCellChoiceEditor(tChoices))
      self.SetCellEditor(x,UNL_POS,wx.grid.GridCellChoiceEditor(tChoices))
      self.SetCellEditor(x,UNO_POS,wx.grid.GridCellChoiceEditor(tChoices))
    self.SetRowLabelSize(130)
    self.SetColSize(0,130)
    self.SetColSize(1,130)
    self.SetColSize(2,130)
    self.SetColSize(3,130)
