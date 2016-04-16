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
import wx.lib.gridmovers as gridmovers
from cairis.core.ObstacleManager import ObstacleManager
from cairis.core.ARM import *
from cairis.core.armid import *
from cairis.core.Borg import Borg
from EnvironmentGrid import EnvironmentGrid
from DimensionNameDialog import DimensionNameDialog
from datetime import datetime

catChoices = ['Confidentiality Threat','Integrity Threat','Availability Threat','Accountability Threat','Vulnerability','Duration','Frequency','Demands','Goal Support','Anonymity Threat','Pseudonymity Threat','Unlinkability Threat','Unobservability Threat']
NAME_POS = 0
DEFINITION_POS = 1
CATEGORY_POS = 2
ORIGINATOR_POS = 3

class ObstaclesTable(wx.grid.PyGridTableBase):

  def __init__(self,obsCombo,envCombo):
    wx.grid.PyGridTableBase.__init__(self)
    self.dimension = 'obstacle'
    self.colLabels = ['Name','Definition','Category','Originator']
    self.om = ObstacleManager(obsCombo,envCombo)
    self.obsName = obsCombo.GetValue()
    self.envName = envCombo.GetValue()

  def object(self):
    return self.obsName

  def GetNumberRows(self):
    return self.om.size()

  def GetNumberCols(self):
    return len(self.colLabels)

  def GetColLabelValue(self,col):
    return self.colLabels[col]

  def GetRowLabelValue(self,row):
    return self.om.obstacles[row].label(self.envName)

  def IsEmptyCell(self,row,col):
    return False

  def GetValue(self,row,col):
    if (col == NAME_POS):
      return self.om.obstacles[row].name()
    elif (col == DEFINITION_POS):
      return self.om.obstacles[row].definition(self.envName)
    elif (col == CATEGORY_POS):
      return self.om.obstacles[row].category(self.envName)
    elif (col == ORIGINATOR_POS):
      return self.om.obstacles[row].originator()

  def SetValue(self,row,col,value):
    if (col == NAME_POS):
      self.om.obstacles[row].setName(value)
    elif (col == DEFINITION_POS):
      self.om.obstacles[row].setDefinition(self.envName,value)
    elif (col == CATEGORY_POS):
      self.om.obstacles[row].setCategory(self.envName,value)
    elif (col == ORIGINATOR_POS):
      self.om.obstacles[row].setOriginator(value)

   
  def AppendRows(self,numRows=1):
    pos = self.om.size() - 1
    self.InsertRows(pos,numRows)

  def InsertRows(self,pos,numRows=1):
    onDlg = wx.TextEntryDialog(None,'Enter obstacle name','New Obstacle','',style=wx.OK|wx.CANCEL)
    if (onDlg.ShowModal() == wx.ID_OK): 
      obsName = onDlg.GetValue()
      if (obsName != ''):  
        if (pos == -1):
          pos = 0
        newPos = pos + 1
        try:
          self.om.add(newPos,obsName)
        except ARMException,errorText:
          dlg = wx.MessageDialog(self.GetView(),str(errorText),'Add Obstacle',wx.OK | wx.ICON_ERROR)
          dlg.ShowModal()
          dlg.Destroy()
          return

        self.addToView(newPos)
        grid = self.GetView()
        grid.SetCellEditor(newPos,NAME_POS,wx.grid.GridCellAutoWrapStringEditor())
        grid.SetCellRenderer(newPos,NAME_POS,wx.grid.GridCellAutoWrapStringRenderer())
        grid.SetCellEditor(newPos,DEFINITION_POS,wx.grid.GridCellAutoWrapStringEditor())
        grid.SetCellRenderer(newPos,DEFINITION_POS,wx.grid.GridCellAutoWrapStringRenderer())
        grid.SetCellEditor(newPos,CATEGORY_POS,wx.grid.GridCellChoiceEditor(catChoices))
        grid.SetCellEditor(newPos,ORIGINATOR_POS,wx.grid.GridCellAutoWrapStringEditor())
        grid.SetCellRenderer(newPos,ORIGINATOR_POS,wx.grid.GridCellAutoWrapStringRenderer())
    onDlg.Destroy()
    return True

  def DeleteRows(self,pos,numRows=1):
    try:
      deletedNoObs = self.om.delete(pos)
      self.deleteFromView(pos,deletedNoObs)
      return True
    except ARMException,errorText:
      dlg = wx.MessageDialog(self.GetView(),str(errorText),'Delete Obstacle',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def ClearRows(self,numRows):
    try:
      self.deleteFromView(0,numRows)
      return True
    except ARMException,errorText:
      dlg = wx.MessageDialog(self.GetView(),str(errorText),'Delete Obstacle',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return
    
  def addToView(self,pos):
    grid = self.GetView()
    if grid:
      grid.BeginBatch()
      msg = wx.grid.GridTableMessage(self,wx.grid.GRIDTABLE_NOTIFY_ROWS_INSERTED,pos,1)
      grid.ProcessTableMessage(msg)
      grid.EndBatch() 

  def updateView(self):
    grid = self.GetView()
    if grid:
      grid.BeginBatch()
      msg = wx.grid.GridTableMessage(self,wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
      grid.ProcessTableMessage(msg)
      grid.EndBatch() 

  def deleteFromView(self,pos,noOfRows=1):
    grid = self.GetView()
    if grid:
      grid.EnableCellEditControl(False)
      grid.BeginBatch()
      msg = wx.grid.GridTableMessage(self,wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED,pos,noOfRows)
      grid.ProcessTableMessage(msg)
      grid.EndBatch() 

  def commitChanges(self):
    self.om.commitChanges()

  def MoveRow(self,frm,to):
    grid = self.GetView()
    if grid:
      oldObs = self.om.obstacles[frm]
      del self.om.obstacles[frm]
      if (to > frm):
        self.om.obstacles.insert(to-1,oldObs)
      else:
        self.om.obstacles.insert(to,oldGoal)
      self.om.commitChanges()
      grid.BeginBatch()
      msg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_NOTIFY_ROWS_INSERTED,to,1)
      grid.ProcessTableMessage(msg)
      msg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED,frm,1)
      grid.ProcessTableMessage(msg)
      grid.EndBatch()
    

#derived obstacles cell editor from GridCellAutoWrapStringEditor and override handle return

class ObstaclesCellEditor(wx.grid.GridCellAutoWrapStringEditor):
  def __init__(self):
    wx.grid.GridCellAutoWrapStringEditor.__init__(self)

 
class ObstaclesGrid(wx.grid.Grid,EnvironmentGrid):
  def __init__(self,parent,obsCombo,envCombo):
    wx.grid.Grid.__init__(self,parent,ID_REQGRID)
    EnvironmentGrid.__init__(self)
    self.thePanel = parent
    wx.lib.gridmovers.GridRowMover(self)
    self.obsCombo = obsCombo
    self.envCombo = envCombo
    self.Bind(wx.lib.gridmovers.EVT_GRID_ROW_MOVE, self.OnRowMove, self)
    self.editIndicator = False
    self.setTable(self.obsCombo,self.envCombo)

    
  def setTable(self,obsCombo,envCombo):
    self.SetTable(ObstaclesTable(obsCombo,envCombo))
    self.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
    objtTable = self.GetTable()
    objtManager = objtTable.om
    for x in range(self.GetNumberRows()):
      self.SetCellEditor(x,NAME_POS,wx.grid.GridCellAutoWrapStringEditor())
      self.SetCellRenderer(x,NAME_POS,wx.grid.GridCellAutoWrapStringRenderer())
      self.SetCellEditor(x,DEFINITION_POS,wx.grid.GridCellAutoWrapStringEditor())
      self.SetCellRenderer(x,DEFINITION_POS,wx.grid.GridCellAutoWrapStringRenderer())
      self.SetCellEditor(x,CATEGORY_POS,wx.grid.GridCellChoiceEditor(catChoices))
      self.SetCellEditor(x,ORIGINATOR_POS,wx.grid.GridCellAutoWrapStringEditor())
      self.SetCellRenderer(x,ORIGINATOR_POS,wx.grid.GridCellAutoWrapStringRenderer())
      objt = objtManager[x]
      if objt.refinements(objtTable.envName) == True:
        self.SetCellBackgroundColour(x,NAME_POS,"pale green")
    self.lastRow = 0

  def OnRowMove(self,evt):
    frm = evt.GetMoveRow()
    to = evt.GetBeforeRow()
    self.GetTable().MoveRow(frm,to)

  def commitChanges(self):
    table = self.GetTable()
    table.commitChanges()
    self.thePanel.statusBar.SetStatusText(str(datetime.now())[:19] + ' : obstacle changes committed')

  def onKeyDown(self,evt):
    keyCode = evt.GetKeyCode()
    if (keyCode != wx.WXK_RETURN) and (keyCode != wx.WXK_DELETE):
      evt.Skip()
      return
    currentRowIndex = self.GetGridCursorRow()
    if (keyCode == wx.WXK_RETURN):
      if self.IsCellEditControlEnabled() == False:
        self.InsertRows(currentRowIndex,1)
      else:
        evt.Skip()
        return

  def reload(self):
    self.DeleteRows(0,self.GetNumberRows())
    self.setTable(self.obsCombo,self.envCombo)

  def reloadView(self):
    table = self.GetTable()
    table.ClearRows(self.GetNumberRows())
    self.setTable(self.obsCombo,self.envCombo)
