#$URL$ $Id: StepGrid.py 469 2011-05-14 22:36:20Z shaf $
import wx
import wx.grid
import wx.lib.gridmovers as gridmovers
from ARM import *
import armid
from Steps import Steps
from Step import Step
from Borg import Borg
from ExceptionDialog import ExceptionDialog
from SingleGoalDialog import SingleGoalDialog
from SingleObstacleDialog import SingleObstacleDialog
from SingleRequirementDialog import SingleRequirementDialog
from StepSynopsisDialog import StepSynopsisDialog
from GoalAssociationParameters import GoalAssociationParameters
import RequirementFactory

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

class StepTable(wx.grid.PyGridTableBase):

  def __init__(self,s = None):
    wx.grid.PyGridTableBase.__init__(self)
    self.colLabels = ['Step']
    if (s != None):
      self.steps = s
    else:
      self.steps = Steps()

  def GetNumberRows(self):
    return (self.steps).size()

  def GetNumberCols(self):
    return 1

  def GetColLabelValue(self,col):
    return 'Step'

  def IsEmptyCell(self,row,col):
    return False

  def GetValue(self,row,col):
    return (self.steps[row]).text()

  def SetValue(self,row,col,value):
    self.steps[row].setText(value)
   
  def AppendRows(self,numRows=1):
    pos = self.steps.size() - 1
    self.InsertRows(pos,numRows)

  def InsertRows(self,pos,numRows=1):
    if (pos == -1):
      pos = 0
    newPos = pos + 1
    if (self.steps.size() == 0):
      lastLabel = 0
    else:
      lastLabel = pos
    newLabel = lastLabel + 1
    try:
      self.steps.append(Step())
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self.GetView(),str(errorText),'Add Step',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

    self.addToView(newLabel)
    grid = self.GetView()
    grid.SetCellEditor(newPos,0,wx.grid.GridCellAutoWrapStringEditor())
    grid.SetCellRenderer(newPos,0,wx.grid.GridCellAutoWrapStringRenderer())
    return True

  def DeleteRows(self,pos,numRows=1):
    try:
      if self.steps.size() > 0:
        self.steps.remove(pos)
        self.deleteFromView(pos,1)
      return True
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self.GetView(),str(errorText),'Delete Step',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def ClearRows(self,numRows):
    try:
      self.deleteFromView(0,numRows)
      return True
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self.GetView(),str(errorText),'Delete Steps',wx.OK | wx.ICON_ERROR)
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

  def MoveRow(self,frm,to):
    grid = self.GetView()
    if grid:
      oldLabel = frm
      oldStep = self.steps[frm]
      self.steps.remove(frm)
      if (to > frm):
        self.steps.insert(to-1,oldStep)
      else:
        self.steps.insert(to,oldStep)
      grid.BeginBatch()
      msg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_NOTIFY_ROWS_INSERTED,to,1)
      grid.ProcessTableMessage(msg)
      msg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED,frm,1)
      grid.ProcessTableMessage(msg)
      grid.EndBatch()
    

class StepCellEditor(wx.grid.GridCellAutoWrapStringEditor):
  def __init__(self):
    wx.grid.GridCellAutoWrapStringEditor.__init__(self)

 
# should mark attrs dirty in the cell when these change instead of relying on pressing return in the cell

class StepGrid(wx.grid.Grid):
  def __init__(self,parent,envName):
    wx.grid.Grid.__init__(self,parent,armid.USECASE_GRIDFLOW_ID,wx.DefaultPosition,wx.Size(300,200))
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theEnvironmentName = envName
    self.theUseCase = ''
    self.theMenu = wx.Menu()
    self.theMenu.Append(armid.STEPGRID_MENUDELETE_ID,'Delete')
    self.theMenu.Append(armid.STEPGRID_MENUGOAL_ID,'Refining Goal')
    self.theMenu.Append(armid.STEPGRID_MENUOBSTACLE_ID,'Refining Obstacle')
    self.theMenu.Append(armid.STEPGRID_MENUREQUIREMENT_ID,'Refining Requirement')
    self.theMenu.Append(armid.STEPGRID_MENUSYNOPSIS_ID,'Synopsis')

    self.thePanel = parent
    wx.lib.gridmovers.GridRowMover(self)
    self.Bind(wx.lib.gridmovers.EVT_GRID_ROW_MOVE, self.OnRowMove, self)
    self.editIndicator = False
    self.setTable()
    wx.EVT_MENU(self,armid.STEPGRID_MENUDELETE_ID,self.onDeleteStep)
    wx.EVT_MENU(self,armid.STEPGRID_MENUGOAL_ID,self.onGoal)
    wx.EVT_MENU(self,armid.STEPGRID_MENUOBSTACLE_ID,self.onObstacle)
    wx.EVT_MENU(self,armid.STEPGRID_MENUREQUIREMENT_ID,self.onRequirement)
    wx.EVT_MENU(self,armid.STEPGRID_MENUSYNOPSIS_ID,self.onSynopsis)
    self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.onRightClick)
    self.goalItem = self.theMenu.FindItemById(armid.STEPGRID_MENUREQUIREMENT_ID)
    self.goalItem.Enable(False)
    self.reqItem = self.theMenu.FindItemById(armid.STEPGRID_MENUREQUIREMENT_ID)
    self.reqItem.Enable(False)
    self.obsItem = self.theMenu.FindItemById(armid.STEPGRID_MENUOBSTACLE_ID)
    self.obsItem.Enable(False)
    self.synItem = self.theMenu.FindItemById(armid.STEPGRID_MENUSYNOPSIS_ID)
    self.synItem.Enable(False)

  def steps(self):
    table = self.GetTable()
    return table.steps
    
  def setEnvironment(self,envName):
    self.theEnvironmentName = envName

  def setUseCase(self,ucName):
    self.theUseCase = ucName
    if (self.theUseCase != ''):
      self.goalItem.Enable()
      self.reqItem.Enable()
      self.obsItem.Enable()
      self.synItem.Enable()
    else:
      self.goalItem.Enable(False)
      self.reqItem.Enable(False)
      self.obsItem.Enable(False)
      self.synItem.Enable(False)


  def onRightClick(self,evt):
    self.PopupMenu(self.theMenu)

  def setTable(self,steps = None):
    self.SetTable(StepTable(steps))
    self.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
    self.Bind(wx.grid.EVT_GRID_EDITOR_SHOWN, self.onUpdateCell, self)
    for x in range(self.GetNumberRows()):
      self.SetCellEditor(x,0,wx.grid.GridCellAutoWrapStringEditor())
      self.SetCellRenderer(x,0,wx.grid.GridCellAutoWrapStringRenderer())
    self.lastRow = 0
    self.SetColSize(0,500)

  def OnRowMove(self,evt):
    frm = evt.GetMoveRow()
    to = evt.GetBeforeRow()
    self.GetTable().MoveRow(frm,to)

  def commitChanges(self):
    table = self.GetTable()
    table.commitChanges()

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

  def AppendStep(self,stepText):
    self.AppendRows()
    table = self.GetTable()
    pos = table.steps.size() - 1
    table.SetValue(pos,0,stepText)
    stepId = pos + 1
    return stepId

  def UpdateRequirement(self,pos,stepText):
    table = self.GetTable()
    table.SetValue(pos,0,stepText)
    table.updateView()

  def onUpdateCell(self,evt):
    currentRowIndex = self.GetGridCursorRow()
    grid = self.GetTable()
    r = grid.steps[currentRowIndex]

  def reloadSteps(self,steps = None):
    self.DeleteRows(0,self.GetNumberRows())
    self.setTable(steps)

  def reloadView(self):
    table = self.GetTable()
    table.ClearRows(self.GetNumberRows())
    self.setTable()

  def onDeleteStep(self,evt):
    currentRowIndex = self.GetGridCursorRow()
    self.DeleteRows(currentRowIndex,1)

  def stepExceptions(self,pos): 
    table = self.GetTable()
    currentStep = table.steps[pos]
    return currentStep.exceptions()

  def stepException(self,excName):
    pos = self.GetGridCursorRow()
    table = self.GetTable()
    currentStep = table.steps[pos]
    return currentStep.exception(excName)

  def setStepException(self,pos,oldExcName,exc):
    table = self.GetTable()
    currentStep = table.steps[pos]
    currentStep.setException(oldExcName,exc)
    table.steps[pos] = currentStep

  def onAddException(self,evt):
    dlg = ExceptionDialog(self,self.theEnvironmentName) 
    if (dlg.ShowModal() == armid.EXCEPTION_BUTTONCOMMIT_ID):
      pos = self.GetGridCursorRow()
      table = self.GetTable()
      currentStep = table.steps[pos]
      exc = dlg.parameters() 
      currentStep.addException(exc)

  def onGoal(self,evt):
    try:
      dlg = SingleGoalDialog(self,self.theEnvironmentName)
      if (dlg.ShowModal() == armid.GOAL_BUTTONCOMMIT_ID):
        gp = dlg.parameters()
        self.dbProxy.addGoal(gp)
        gap = GoalAssociationParameters(self.theEnvironmentName,gp.name(),'goal',dlg.theContributionType,self.theUseCase,'usecase',0,'')
        self.dbProxy.addGoalAssociation(gap)
        ackDlg = wx.MessageDialog(self,'Added goal ' + gp.name(),'Refining goal',wx.OK)
        ackDlg.ShowModal()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Refining goal',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()

  def onObstacle(self,evt):
    try:
      dlg = SingleObstacleDialog(self,self.theEnvironmentName)
      if (dlg.ShowModal() == armid.OBSTACLE_BUTTONCOMMIT_ID):
        op = dlg.parameters()
        self.dbProxy.addObstacle(op)
        gap = GoalAssociationParameters(self.theEnvironmentName,op.name(),'obstacle','and',self.theUseCase,'usecase',0,'')
        self.dbProxy.addGoalAssociation(gap)
        ackDlg = wx.MessageDialog(self,'Added obstacle ' + op.name(),'Refining goal',wx.OK)
        ackDlg.ShowModal()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Refining obstacle',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()


  def onRequirement(self,evt):
    try:
      ucId = self.dbProxy.getDimensionId(self.theUseCase,'usecase')
      dlg = SingleRequirementDialog(self)
      if (dlg.ShowModal() == armid.SINGLEREQUIREMENT_BUTTONCOMMIT_ID):
        refName = dlg.referrer()
        completeReqLabel = self.dbProxy.lastRequirementLabel(refName)
        referrer,reqLabel = completeReqLabel.split('-')
        reqId = self.dbProxy.newId()
        reqLabel = int(reqLabel)
        reqLabel += 1
        r = RequirementFactory.build(reqId,reqLabel,dlg.description(),dlg.priority(),dlg.rationale(),dlg.fitCriterion(),dlg.originator(),dlg.type(),refName)
        isAsset = True
        if (dlg.referrerType() == 'environment'):
          isAsset = False
        self.dbProxy.addRequirement(r,refName,isAsset)
        self.dbProxy.addTrace('requirement_usecase',reqId,ucId)
        completeReqLabel = self.dbProxy.lastRequirementLabel(refName)
        ackDlg = wx.MessageDialog(self,'Added requirement ' + completeReqLabel,'Refining requirement',wx.OK)
        ackDlg.ShowModal()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Refining requirement',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()

  def onSynopsis(self,evt):
    table = self.GetTable()
    pos = self.GetGridCursorRow()
    currentStep = table.steps[pos]
    dlg = StepSynopsisDialog(self,currentStep.synopsis(),currentStep.actor(),currentStep.actorType())
    if (dlg.ShowModal() == armid.STEPSYNOPSIS_BUTTONCOMMIT_ID):
      currentStep.setSynopsis(dlg.synopsis())
      currentStep.setActor(dlg.actor())
      currentStep.setActorType(dlg.actorType())
      table.steps[pos] = currentStep
    dlg.Destroy()
