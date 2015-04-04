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
from RequirementManager import RequirementManager
import Requirement
from ARM import *
import armid
from Borg import Borg
from Traceable import Traceable
from DimensionNameDialog import DimensionNameDialog
from ReqToGoalDialog import ReqToGoalDialog
from RequirementHistoryDialog import RequirementHistoryDialog

priorityChoices = ['1','2','3']
typeChoices = ['Functional','Data','Look and Feel','Usability','Performance','Operational','Maintainability','Portability','Security','Cultural and Political','Legal','Privacy']
NAME_POS = 0
DESCRIPTION_POS = 1
PRIORITY_POS = 2
RATIONALE_POS = 3
FITCRITERION_POS = 4
ORIGINATOR_POS = 5
TYPE_POS = 6

def increment(inStr):
  stringInput = str(inStr)
  inTokens = stringInput.split('.')
  stringLength = len(stringInput)
  tokensLength = len(inTokens)
  if (tokensLength == 1):
    return str( int(stringInput) + 1)
  else:
    inTokens[tokensLength - 1] = str(int(inTokens[tokensLength-1]) + 1)
    outTokens = ""
    for c in inTokens:
      outTokens += c + '.'
    return outTokens[0:len(outTokens)-1]

def grain(inStr):
  return len(inStr.split('.'))

class RequirementsTable(wx.grid.PyGridTableBase):

  def __init__(self,modCombo,envCombo):
    wx.grid.PyGridTableBase.__init__(self)
    self.dimension = 'requirement'
    self.colLabels = ['Name','Description','Priority','Rationale','Fit Criterion','Originator','Type']
    if (modCombo.GetValue() != ''):
      self.om = RequirementManager(modCombo)
    else:
      self.om = RequirementManager(envCombo,False)

  def GetNumberRows(self):
    return self.om.size()

  def GetNumberCols(self):
    return len(self.colLabels)

  def GetColLabelValue(self,col):
    return self.colLabels[col]

  def GetRowLabelValue(self,row):
    return self.om.reqs[row].label()

  def IsEmptyCell(self,row,col):
    return False

  def GetValue(self,row,col):
    if (col == NAME_POS):
      return self.om.reqs[row].name()
    elif (col == DESCRIPTION_POS):
      return self.om.reqs[row].description()
    elif (col == PRIORITY_POS):
      return self.om.reqs[row].priority()
    elif (col == RATIONALE_POS):
      return self.om.reqs[row].rationale()
    elif (col == FITCRITERION_POS):
      return self.om.reqs[row].fitCriterion()
    elif (col == ORIGINATOR_POS):
      return self.om.reqs[row].originator()
    elif (col == TYPE_POS):
      return self.om.reqs[row].type()

  def SetValue(self,row,col,value):
    label = self.GetRowLabelValue(row)
    if (col == NAME_POS):
      self.om.update(label,'name',value)
    elif (col == DESCRIPTION_POS):
      self.om.update(label,'description',value)
    elif (col == PRIORITY_POS):
      self.om.update(label,'priority',value)
    elif (col == RATIONALE_POS):
      self.om.update(label,'rationale',value)
    elif (col == FITCRITERION_POS):
      self.om.update(label,'fitCriterion',value)
    elif (col == ORIGINATOR_POS):
      self.om.update(label,'originator',value)
    elif (col == TYPE_POS):
      self.om.update(label,'type',value)

   
  def AppendRows(self,numRows=1):
    pos = self.om.size() - 1
    self.InsertRows(pos,numRows)

  def InsertRows(self,pos,numRows=1):
    try:
      if (pos == -1):
        pos = 0
      newPos = pos + 1
      if (self.om.size() == 0):
        lastLabel = 0
      else:
        lastGridLabel = self.om.reqs[pos].label()
        if (len(str(lastGridLabel).split('-')) > 1):
          raise ARMException('Asset or Environment must be specified')  
        lastLabel = int(lastGridLabel)
      newLabel = lastLabel + 1
      self.om.add(newLabel,newPos)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self.GetView(),str(errorText),'Add Requirement',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

    newReqPos,newReq = self.om.requirementByLabel(newLabel)
    self.addToView(newReqPos)
    grid = self.GetView()
    grid.SetCellEditor(newPos,NAME_POS,wx.grid.GridCellAutoWrapStringEditor())
    grid.SetCellRenderer(newPos,NAME_POS,wx.grid.GridCellAutoWrapStringRenderer())
    grid.SetCellEditor(newPos,DESCRIPTION_POS,wx.grid.GridCellAutoWrapStringEditor())
    grid.SetCellRenderer(newPos,DESCRIPTION_POS,wx.grid.GridCellAutoWrapStringRenderer())
    grid.SetCellEditor(newPos,PRIORITY_POS,wx.grid.GridCellChoiceEditor(priorityChoices))
    grid.SetCellEditor(newPos,RATIONALE_POS,wx.grid.GridCellAutoWrapStringEditor())
    grid.SetCellRenderer(newPos,RATIONALE_POS,wx.grid.GridCellAutoWrapStringRenderer())
    grid.SetCellEditor(newPos,FITCRITERION_POS,wx.grid.GridCellAutoWrapStringEditor())
    grid.SetCellRenderer(newPos,FITCRITERION_POS,wx.grid.GridCellAutoWrapStringRenderer())
    grid.SetCellEditor(newPos,ORIGINATOR_POS,wx.grid.GridCellAutoWrapStringEditor())
    grid.SetCellRenderer(newPos,ORIGINATOR_POS,wx.grid.GridCellAutoWrapStringRenderer())
    grid.SetCellEditor(newPos,TYPE_POS,wx.grid.GridCellChoiceEditor(typeChoices))
    return True

  def InsertChildRows(self,pos):
    newPos = pos + 1
    lastLabel = self.om.reqs[pos].label()
    newLabel = lastLabel + '.1'

    # guess the parent - can get req based on current pos and use this I guess
    parentReq = self.om.reqs[pos]
    self.om.addChild(childLabel=newLabel,childIdx=newPos,parent=parentReq)
    self.om.sort() 
    self.addToView(newPos)
    grid = self.GetView()
    grid.SetCellEditor(newPos,NAME_POS,wx.grid.GridCellAutoWrapStringEditor())
    grid.SetCellRenderer(newPos,NAME_POS,wx.grid.GridCellAutoWrapStringRenderer())
    grid.SetCellEditor(newPos,DESCRIPTION_POS,wx.grid.GridCellAutoWrapStringEditor())
    grid.SetCellRenderer(newPos,DESCRIPTION_POS,wx.grid.GridCellAutoWrapStringRenderer())
    grid.SetCellEditor(newPos,PRIORITY_POS,wx.grid.GridCellChoiceEditor(priorityChoices))
    grid.SetCellEditor(newPos,RATIONALE_POS,wx.grid.GridCellAutoWrapStringEditor())
    grid.SetCellRenderer(newPos,RATIONALE_POS,wx.grid.GridCellAutoWrapStringRenderer())
    grid.SetCellEditor(newPos,FITCRITERION_POS,wx.grid.GridCellAutoWrapStringEditor())
    grid.SetCellRenderer(newPos,FITCRITERION_POS,wx.grid.GridCellAutoWrapStringRenderer())
    grid.SetCellEditor(newPos,ORIGINATOR_POS,wx.grid.GridCellAutoWrapStringEditor())
    grid.SetCellRenderer(newPos,ORIGINATOR_POS,wx.grid.GridCellAutoWrapStringRenderer())
    grid.SetCellEditor(newPos,TYPE_POS,wx.grid.GridCellChoiceEditor(typeChoices))
 
  def DeleteRows(self,pos,numRows=1):
    try:
      lastGridLabel = self.om.reqs[pos].label()
      if (len(str(lastGridLabel).split('-')) > 1):
        raise ARMException('Asset or Environment must be specified')  
      deletedNoReqs = self.om.delete(pos)
      self.deleteFromView(pos,deletedNoReqs)
      return True
    except ARMException,errorText:
      dlg = wx.MessageDialog(self.GetView(),str(errorText),'Delete Requirement',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def ClearRows(self,numRows):
    try:
      self.deleteFromView(0,numRows)
      return True
    except ARMException,errorText:
      dlg = wx.MessageDialog(self.GetView(),str(errorText),'Delete Requirement',wx.OK | wx.ICON_ERROR)
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
    try:
      grid = self.GetView()
      pos = grid.GetGridCursorRow() 
      if (pos >= 0):
        lastGridLabel = self.om.reqs[pos].label()
        if (len(str(lastGridLabel).split('-')) > 1):
          l_str_errorText = ['Asset or Environment must be specified.']
          if self.om.reqs[pos].attrs['asset'] != '':
            l_str_errorText.append('\n\nRecommended asset filter: ')
            l_str_errorText.append(self.om.reqs[pos].attrs['asset'])
          
          errorText = ''.join(l_str_errorText)
          raise ARMException(errorText)  
      self.om.commitChanges()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self.GetView(),errorText.value,'Commit changes',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def MoveRow(self,frm,to):
    grid = self.GetView()
    if grid:
      oldLabel = self.om.reqs[frm].label()
      oldReq = self.om.reqs[frm]
      del self.om.reqs[frm]
      if (to > frm):
        self.om.reqs.insert(to-1,oldReq)
      else:
        self.om.reqs.insert(to,oldReq)
      self.om.relabel()
      self.om.commitChanges()
      grid.BeginBatch()
      msg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_NOTIFY_ROWS_INSERTED,to,1)
      grid.ProcessTableMessage(msg)
      msg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED,frm,1)
      grid.ProcessTableMessage(msg)
      grid.EndBatch()
    

#derived requirements cell editor from GridCellAutoWrapStringEditor and override handle return

class RequirementsCellEditor(wx.grid.GridCellAutoWrapStringEditor):
  def __init__(self):
    wx.grid.GridCellAutoWrapStringEditor.__init__(self)

 
# should mark attrs dirty in the cell when these change instead of relying on pressing return in the cell

class RequirementsGrid(wx.grid.Grid,Traceable):
  def __init__(self,parent,modCombo,envCombo):
    wx.grid.Grid.__init__(self,parent,armid.ID_REQGRID)
    Traceable.__init__(self)
    self.theTraceMenu.Append(armid.TRACE_MENUTRACE_HISTORY_ID,'History')
    self.theTraceMenu.Append(armid.TRACE_MENUTRACE_REASSOCIATE_ID,'Asset re-association')
    self.theTraceMenu.Append(armid.TRACE_MENUTRACE_TURNTOGOAL_ID,'Turn to goal')
    self.thePanel = parent
    wx.lib.gridmovers.GridRowMover(self)
    self.modCombo = modCombo
    self.envCombo = envCombo
    self.Bind(wx.lib.gridmovers.EVT_GRID_ROW_MOVE, self.OnRowMove, self)
    self.editIndicator = False
    self.setTable(self.modCombo,self.envCombo)
    wx.EVT_MENU(self,armid.TRACE_MENUTRACE_REASSOCIATE_ID,self.onReassociate)
    wx.EVT_MENU(self,armid.TRACE_MENUTRACE_TURNTOGOAL_ID,self.onTurnToGoal)
    wx.EVT_MENU(self,armid.TRACE_MENUTRACE_HISTORY_ID,self.onHistory)
    self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.onRightClick)


    
  def setTable(self,modCombo,envCombo):
    self.SetTable(RequirementsTable(modCombo,envCombo))
    self.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
    self.Bind(wx.grid.EVT_GRID_EDITOR_SHOWN, self.onUpdateCell, self)
    for x in range(self.GetNumberRows()):
      self.SetCellEditor(x,NAME_POS,wx.grid.GridCellAutoWrapStringEditor())
      self.SetCellRenderer(x,NAME_POS,wx.grid.GridCellAutoWrapStringRenderer())
      self.SetCellEditor(x,DESCRIPTION_POS,wx.grid.GridCellAutoWrapStringEditor())
      self.SetCellRenderer(x,DESCRIPTION_POS,wx.grid.GridCellAutoWrapStringRenderer())
      self.SetCellEditor(x,PRIORITY_POS,wx.grid.GridCellChoiceEditor(priorityChoices))
      self.SetCellEditor(x,RATIONALE_POS,wx.grid.GridCellAutoWrapStringEditor())
      self.SetCellRenderer(x,RATIONALE_POS,wx.grid.GridCellAutoWrapStringRenderer())
      self.SetCellEditor(x,FITCRITERION_POS,wx.grid.GridCellAutoWrapStringEditor())
      self.SetCellRenderer(x,FITCRITERION_POS,wx.grid.GridCellAutoWrapStringRenderer())
      self.SetCellEditor(x,ORIGINATOR_POS,wx.grid.GridCellAutoWrapStringEditor())
      self.SetCellRenderer(x,ORIGINATOR_POS,wx.grid.GridCellAutoWrapStringRenderer())
      self.SetCellEditor(x,TYPE_POS,wx.grid.GridCellChoiceEditor(typeChoices))
    self.lastRow = 0

  def OnRowMove(self,evt):
    frm = evt.GetMoveRow()
    to = evt.GetBeforeRow()
    self.GetTable().MoveRow(frm,to)

  def commitChanges(self):
    table = self.GetTable()
    table.commitChanges()

  def InsertChildRows(self,pos):
    table = self.GetTable()
    table.InsertChildRows(pos)

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

  def AppendRequirement(self,reqName,reqText,priority,rationale,fitCriterion,originatorName,reqType):
    self.AppendRows()
    table = self.GetTable()
    pos = table.om.size() - 1
    table.SetValue(pos,NAME_POS,reqName)
    table.SetValue(pos,DESCRIPTION_POS,reqText)
    table.SetValue(pos,PRIORITY_POS,priority)
    table.SetValue(pos,RATIONALE_POS,rationale)
    table.SetValue(pos,FITCRITERION_POS,fitCriterion)
    table.SetValue(pos,ORIGINATOR_POS,originatorName)
    table.SetValue(pos,TYPE_POS,reqType)
    self.commitChanges()
    reqId = (table.om.reqs[pos]).id()
    return reqId

  def UpdateRequirement(self,pos,reqText):
    table = self.GetTable()
    table.SetValue(pos,DESCRIPTION_POS,reqText)
    self.commitChanges()
    table.updateView()

  def InsertRequirement(self,reqId,reqName,reqText,originatorName):
    table = self.GetTable()
    pos = table.om.posByRequirement(reqId)
    self.InsertChildRows(pos)
    newPos = pos + 1
    table.SetValue(newPos,NAME_POS,reqName)
    table.SetValue(newPos,DESCRIPTION_POS,reqText)
    table.SetValue(newPos,ORIGINATOR_POS,originatorName)
    self.commitChanges()
    reqId = (table.om.reqs[pos]).id()
    return reqId


  def onUpdateCell(self,evt):
    currentRowIndex = self.GetGridCursorRow()
    grid = self.GetTable()
    r = grid.om.reqs[currentRowIndex]

  def reload(self):
    self.DeleteRows(0,self.GetNumberRows())
    self.setTable(self.modCombo,self.envCombo)

  def reloadView(self):
    table = self.GetTable()
    table.ClearRows(self.GetNumberRows())
    self.setTable(self.modCombo,self.envCombo)

  def onReassociate(self,evt):
    b = Borg()
    p = b.dbProxy
    dimensions = p.getDimensionNames('asset')
    dlg = DimensionNameDialog(self,'asset',dimensions,'Select')
    if (dlg.ShowModal() == armid.DIMNAME_BUTTONACTION_ID):
      selectedAsset = dlg.dimensionName()
      reqTable = self.GetTable()
      selectedReq = reqTable.om.reqs[self.GetGridCursorRow()]
      p.reassociateAsset(selectedAsset,self.envCombo.GetValue(),selectedReq.id())
      self.modCombo.SetStringSelection(selectedAsset)
    dlg.Destroy()
    self.envCombo.SetValue('')
    self.setTable(self.modCombo,self.envCombo)
    self.thePanel.refresh()

  def onTurnToGoal(self,evt):
    b = Borg()
    p = b.dbProxy
    environments = p.getDimensionNames('environment',False)
    cDlg = DimensionNameDialog(self,'environment',environments,'Select')
    if (cDlg.ShowModal() == armid.DIMNAME_BUTTONACTION_ID):
      environmentName = cDlg.dimensionName()
      pos = self.GetGridCursorRow() 
      table = self.GetTable()
      goalName = table.GetValue(pos,NAME_POS)
      goalDef = table.GetValue(pos,DESCRIPTION_POS)
      goalCat = 'Maintain'
      goalPri = table.GetValue(pos,PRIORITY_POS)
      goalFc = table.GetValue(pos,FITCRITERION_POS)
      goalIssue = table.GetValue(pos,RATIONALE_POS)
      goalOrig = table.GetValue(pos,ORIGINATOR_POS)
      goalAssets = [self.modCombo.GetValue()]
      dlg = ReqToGoalDialog(self,goalName,goalDef,goalCat,goalPri,goalFc,goalIssue,goalOrig,goalAssets,environmentName)
      if (dlg.ShowModal() == armid.GOAL_BUTTONCOMMIT_ID):
        b = Borg()
        p = b.dbProxy
        p.addGoal(dlg.parameters())
        self.DeleteRows(pos)
      dlg.Destroy()

  def onAddSupportLink(self,evt):
    try:
      reqTable = self.GetTable()
      selectedReq = (reqTable.om.objects())[self.GetGridCursorRow()]
      self.onTraceTo(reqTable.dimension,selectedReq.id())
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add support link',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return


  def onAddContributionLink(self,evt):
    try:
      reqTable = self.GetTable()
      selectedReq = (reqTable.om.objects())[self.GetGridCursorRow()]
      self.onTraceFrom(reqTable.dimension,selectedReq.id())
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add contribution link',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onDisplaySupport(self,evt):
    reqTable = self.GetTable()
    selectedReq = (reqTable.om.objects())[self.GetGridCursorRow()]
    self.displaySupportBy(reqTable.dimension,selectedReq.id())

  def onDisplayContribution(self,evt):
    reqTable = self.GetTable()
    selectedReq = reqTable.rm.reqs[self.GetGridCursorRow()]
    self.displayContributionTo(reqTable.dimension,selectedReq.id())

  def onHistory(self,evt):
    reqTable = self.GetTable()
    selectedReq = (reqTable.om.objects())[self.GetGridCursorRow()]
    b = Borg()
    p = b.dbProxy
    reqHistory = p.getRequirementVersions(selectedReq.id())
    dlg = RequirementHistoryDialog(self,reqHistory)
    dlg.ShowModal()

