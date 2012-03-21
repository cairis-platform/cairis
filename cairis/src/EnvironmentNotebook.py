#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/GoalEnvironmentNotebook.py $ $Id: GoalEnvironmentNotebook.py 368 2010-12-15 17:04:13Z shaf $
import wx
import armid
import WidgetFactory
from EnvironmentPropertiesPanel import EnvironmentPropertiesPanel
from ValueTensionsGrid import ValueTensionsGrid

class SummaryPage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,armid.GOAL_PANELSUMMARY_ID)
    topSizer = wx.BoxSizer(wx.VERTICAL)
    topSizer.Add(WidgetFactory.buildTextSizer(self,'Short Code',(87,30),armid.ENVIRONMENT_TEXTSHORTCODE_ID,'Code which prefixes requirements which are specific to this environment'),0,wx.EXPAND)
    topSizer.Add(WidgetFactory.buildMLTextSizer(self,'Description',(87,30),armid.ENVIRONMENT_TEXTDESCRIPTION_ID),1,wx.EXPAND)
    self.SetSizer(topSizer)

class CompositePage(wx.Panel):
  def __init__(self,parent,dp):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)
    cBox = wx.StaticBox(self,-1)
    cBoxSizer = wx.StaticBoxSizer(cBox,wx.HORIZONTAL)
    topSizer.Add(cBoxSizer,1,wx.EXPAND)
    self.compositeCtrl = EnvironmentPropertiesPanel(self,dp)
    cBoxSizer.Add(self.compositeCtrl,1,wx.EXPAND)
    self.SetSizer(topSizer)

class TensionsPage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent)
    self.thePrevRow = -1
    self.thePrevCol = -1
    topSizer = wx.BoxSizer(wx.VERTICAL)
    cBox = wx.StaticBox(self,-1)
    cBoxSizer = wx.StaticBoxSizer(cBox,wx.HORIZONTAL)
    topSizer.Add(cBoxSizer,1,wx.EXPAND)
    self.tensionsCtrl = ValueTensionsGrid(self)
    self.tensionsCtrl.Bind(wx.grid.EVT_GRID_SELECT_CELL,self.onSelectRationale)
    cBoxSizer.Add(self.tensionsCtrl,1,wx.EXPAND)

    rBox = wx.StaticBox(self,-1,'Rationale')
    rBoxSizer = wx.StaticBoxSizer(rBox,wx.VERTICAL)
    topSizer.Add(rBoxSizer,1,wx.EXPAND)
    self.rationaleCtrl = wx.TextCtrl(self,armid.ENVIRONMENT_TEXTTENSIONRATIONALE_ID,"",size=(200,100),style=wx.TE_MULTILINE)
    rBoxSizer.Add(self.rationaleCtrl,0,wx.EXPAND)
    self.tensionsCtrl.setRationaleCtrl(self.rationaleCtrl)
    self.SetSizer(topSizer)

  def onSelectRationale(self,evt):
    if (self.thePrevRow != -1 or self.thePrevCol != -1):
      lastRationale = self.rationaleCtrl.GetValue()
      self.tensionsCtrl.setRationale(self.thePrevRow,self.thePrevCol,lastRationale)
    currentRow = evt.GetRow()
    currentCol = evt.GetCol()
    tRat = self.tensionsCtrl.rationale(currentRow,currentCol)
    self.rationaleCtrl.SetValue(tRat)
    self.thePrevRow = currentRow
    self.thePrevCol = currentCol
    evt.Skip()
    

class EnvironmentNotebook(wx.Notebook):
  def __init__(self,parent,dp):
    wx.Notebook.__init__(self,parent,armid.ENVIRONMENT_NOTEBOOKENVIRONMENT_ID)
    p1 = SummaryPage(self)
    p2 = CompositePage(self,dp)
    p3 = TensionsPage(self)
    self.AddPage(p1,'Summary')
    self.AddPage(p2,'Composite')
    self.AddPage(p3,'Tensions')
