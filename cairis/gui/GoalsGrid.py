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
from cairis.core.GoalManager import GoalManager
import cairis.core.Requirement
from cairis.core.ARM import *
from cairis.core.armid import *
from cairis.core.Borg import Borg
from EnvironmentGrid import EnvironmentGrid
from DimensionNameDialog import DimensionNameDialog
from datetime import datetime

priorityChoices = ['Low','Medium','High']
catChoices = ['Maintain','Achieve','Avoid','Improve','Increase','Maximise','Minimise','Accept','Transfer','Mitigate','Deter','Prevent','Detect','React']
NAME_POS = 0
DEFINITION_POS = 1
CATEGORY_POS = 2
PRIORITY_POS = 3
FITCRITERION_POS = 4
ISSUE_POS = 5
ORIGINATOR_POS = 6

class GoalsTable(wx.grid.PyGridTableBase):

  def __init__(self,goalCombo,envCombo):
    wx.grid.PyGridTableBase.__init__(self)
    self.dimension = 'goal'
    self.colLabels = ['Name','Definition','Category','Priority','Fit Criterion','Issue','Originator']
    self.om = GoalManager(goalCombo,envCombo)
    self.goalName = goalCombo.GetValue()
    self.envName = envCombo.GetValue()

  def object(self):
    return self.goalName

  def GetNumberRows(self):
    return self.om.size()

  def GetNumberCols(self):
    return len(self.colLabels)

  def GetColLabelValue(self,col):
    return self.colLabels[col]

  def GetRowLabelValue(self,row):
    return self.om.goals[row].label(self.envName)

  def IsEmptyCell(self,row,col):
    return False

  def GetValue(self,row,col):
    if (col == NAME_POS):
      return self.om.goals[row].name()
    elif (col == DEFINITION_POS):
      return self.om.goals[row].definition(self.envName)
    elif (col == CATEGORY_POS):
      return self.om.goals[row].category(self.envName)
    elif (col == PRIORITY_POS):
      return self.om.goals[row].priority(self.envName)
    elif (col == FITCRITERION_POS):
      return self.om.goals[row].fitCriterion(self.envName)
    elif (col == ISSUE_POS):
      return self.om.goals[row].issue(self.envName)
    elif (col == ORIGINATOR_POS):
      return self.om.goals[row].originator()

  def SetValue(self,row,col,value):
    if (col == NAME_POS):
      self.om.goals[row].setName(value)
    elif (col == DEFINITION_POS):
      self.om.goals[row].setDefinition(self.envName,value)
    elif (col == CATEGORY_POS):
      self.om.goals[row].setCategory(self.envName,value)
    elif (col == PRIORITY_POS):
      self.om.goals[row].setPriority(self.envName,value)
    elif (col == FITCRITERION_POS):
      self.om.goals[row].setFitCriterion(self.envName,value)
    elif (col == ISSUE_POS):
      self.om.goals[row].setIssue(self.envName,value)
    elif (col == ORIGINATOR_POS):
      self.om.goals[row].setOriginator(value)

   
  def AppendRows(self,numRows=1):
    pos = self.om.size() - 1
    self.InsertRows(pos,numRows)

  def InsertRows(self,pos,numRows=1):
    gnDlg = wx.TextEntryDialog(None,'Enter goal name','New Goal','',style=wx.OK|wx.CANCEL)
    if (gnDlg.ShowModal() == wx.ID_OK): 
      goalName = gnDlg.GetValue()
      if (goalName != ''):  
        if (pos == -1):
          pos = 0
        newPos = pos + 1
        try:
          self.om.add(newPos,goalName)
        except ARMException,errorText:
          dlg = wx.MessageDialog(self.GetView(),str(errorText),'Add Goal',wx.OK | wx.ICON_ERROR)
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
        grid.SetCellEditor(newPos,PRIORITY_POS,wx.grid.GridCellChoiceEditor(priorityChoices))
        grid.SetCellEditor(newPos,FITCRITERION_POS,wx.grid.GridCellAutoWrapStringEditor())
        grid.SetCellRenderer(newPos,FITCRITERION_POS,wx.grid.GridCellAutoWrapStringRenderer())
        grid.SetCellEditor(newPos,ISSUE_POS,wx.grid.GridCellAutoWrapStringEditor())
        grid.SetCellRenderer(newPos,ISSUE_POS,wx.grid.GridCellAutoWrapStringRenderer())
        grid.SetCellEditor(newPos,ORIGINATOR_POS,wx.grid.GridCellAutoWrapStringEditor())
        grid.SetCellRenderer(newPos,ORIGINATOR_POS,wx.grid.GridCellAutoWrapStringRenderer())
    gnDlg.Destroy()
    return True

  def DeleteRows(self,pos,numRows=1):
    try:
      deletedNoGoals = self.om.delete(pos)
      self.deleteFromView(pos,deletedNoGoals)
      return True
    except ARMException,errorText:
      dlg = wx.MessageDialog(self.GetView(),str(errorText),'Delete Goal',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def ClearRows(self,numRows):
    try:
      self.deleteFromView(0,numRows)
      return True
    except ARMException,errorText:
      dlg = wx.MessageDialog(self.GetView(),str(errorText),'Delete Goal',wx.OK | wx.ICON_ERROR)
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
      oldGoal = self.om.goals[frm]
      del self.om.goals[frm]
      if (to > frm):
        self.om.goals.insert(to-1,oldGoal)
      else:
        self.om.goals.insert(to,oldGoal)
      self.om.commitChanges()
      grid.BeginBatch()
      msg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_NOTIFY_ROWS_INSERTED,to,1)
      grid.ProcessTableMessage(msg)
      msg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED,frm,1)
      grid.ProcessTableMessage(msg)
      grid.EndBatch()
    

#derived goals cell editor from GridCellAutoWrapStringEditor and override handle return

class GoalsCellEditor(wx.grid.GridCellAutoWrapStringEditor):
  def __init__(self):
    wx.grid.GridCellAutoWrapStringEditor.__init__(self)

 
class GoalsGrid(wx.grid.Grid,EnvironmentGrid):
  def __init__(self,parent,goalCombo,envCombo):
    wx.grid.Grid.__init__(self,parent,ID_REQGRID)
    EnvironmentGrid.__init__(self)
    self.thePanel = parent
    wx.lib.gridmovers.GridRowMover(self)
    self.goalCombo = goalCombo
    self.envCombo = envCombo
    self.Bind(wx.lib.gridmovers.EVT_GRID_ROW_MOVE, self.OnRowMove, self)
    self.editIndicator = False
    self.setTable(self.goalCombo,self.envCombo)

    
  def setTable(self,goalCombo,envCombo):
    self.SetTable(GoalsTable(goalCombo,envCombo))
    self.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
    objtTable = self.GetTable()
    objtManager = objtTable.om
    for x in range(self.GetNumberRows()):
      self.SetCellEditor(x,NAME_POS,wx.grid.GridCellAutoWrapStringEditor())
      self.SetCellRenderer(x,NAME_POS,wx.grid.GridCellAutoWrapStringRenderer())
      self.SetCellEditor(x,DEFINITION_POS,wx.grid.GridCellAutoWrapStringEditor())
      self.SetCellRenderer(x,DEFINITION_POS,wx.grid.GridCellAutoWrapStringRenderer())
      self.SetCellEditor(x,CATEGORY_POS,wx.grid.GridCellChoiceEditor(catChoices))
      self.SetCellEditor(x,PRIORITY_POS,wx.grid.GridCellChoiceEditor(priorityChoices))
      self.SetCellEditor(x,FITCRITERION_POS,wx.grid.GridCellAutoWrapStringEditor())
      self.SetCellRenderer(x,FITCRITERION_POS,wx.grid.GridCellAutoWrapStringRenderer())
      self.SetCellEditor(x,ISSUE_POS,wx.grid.GridCellAutoWrapStringEditor())
      self.SetCellRenderer(x,ISSUE_POS,wx.grid.GridCellAutoWrapStringRenderer())
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
    self.thePanel.statusBar.SetStatusText(str(datetime.now())[:19] + ' : goal changes committed')

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
    self.setTable(self.goalCombo,self.envCombo)

  def reloadView(self):
    table = self.GetTable()
    table.ClearRows(self.GetNumberRows())
    self.setTable(self.goalCombo,self.envCombo)
