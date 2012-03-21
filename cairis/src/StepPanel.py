import armid
import wx
from StepGrid import StepGrid
from ExceptionDialog import ExceptionDialog
from ExceptionListCtrl import ExceptionListCtrl

class StepPanel(wx.Panel):
  def __init__(self,parent,envName):
    wx.Panel.__init__(self,parent,armid.USECASE_PANELFLOW_ID)
    self.theEnvironmentName = envName
    self.theUseCase = ''
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    flowBox = wx.StaticBox(self,-1,'Flow')
    flowSizer = wx.StaticBoxSizer(flowBox,wx.VERTICAL)
    mainSizer.Add(flowSizer,1,wx.EXPAND)
    self.stepGrid = StepGrid(self,self.theEnvironmentName)
    flowSizer.Add(self.stepGrid,1,wx.EXPAND)

    excBox = wx.StaticBox(self,-1)
    excSizer = wx.StaticBoxSizer(excBox,wx.VERTICAL)
    mainSizer.Add(excSizer,0,wx.EXPAND)
    self.exList = ExceptionListCtrl(self,self.theEnvironmentName,self.stepGrid)
    excSizer.Add(self.exList,0,wx.EXPAND)
    self.SetSizerAndFit(mainSizer)
    self.stepGrid.Bind(wx.grid.EVT_GRID_SELECT_CELL,self.onSelectStep)

  def setUseCase(self,ucName):
    self.theUseCase = ucName
    self.stepGrid.setUseCase(self.theUseCase)

  def onSelectStep(self,evt):
    exceptions = self.stepGrid.stepExceptions(evt.GetRow())
    self.exList.load(exceptions)
    evt.Skip()

  def setEnvironment(self,envName):
    self.stepGrid.setEnvironment(envName)
    self.exList.setEnvironment(envName)

  def Disable(self):
    self.stepGrid.Disable()
    self.exList.Disable()

  def Enable(self):
    self.stepGrid.Enable()
    self.exList.Enable()

  def reloadSteps(self,s):
    self.stepGrid.reloadSteps(s)
    if (s != None and s.size() > 0):
      firstStep = s[0]
      self.exList.load(firstStep.exceptions())

  def steps(self):
    return self.stepGrid.steps()

  def clear(self):
    self.stepGrid.setTable()
    self.exList.DeleteAllItems()
