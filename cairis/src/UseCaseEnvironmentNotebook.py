#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/TaskEnvironmentNotebook.py $ $Id: UseCaseEnvironmentNotebook.py 366 2010-12-14 17:30:01Z shaf $
import wx
import armid
from StepPanel import StepPanel
from UseCaseTextCtrl import UseCaseTextCtrl


class TextPage(wx.Panel):
  def __init__(self,parent,winId):
    wx.Panel.__init__(self,parent,-1)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    textBox = wx.StaticBox(self,-1)
    textBoxSizer = wx.StaticBoxSizer(textBox,wx.HORIZONTAL)
    topSizer.Add(textBoxSizer,1,wx.EXPAND)
    self.textCtrl = UseCaseTextCtrl(self,winId)
    textBoxSizer.Add(self.textCtrl,1,wx.EXPAND)
    self.SetSizer(topSizer)

class StepPage(wx.Panel):
  def __init__(self,parent,envName):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    sBox = wx.StaticBox(self,-1)
    sSizer = wx.StaticBoxSizer(sBox,wx.HORIZONTAL)
    topSizer.Add(sSizer,1,wx.EXPAND)
    sSizer.Add(StepPanel(self,envName),1,wx.EXPAND)
    self.SetSizer(topSizer)


class UseCaseEnvironmentNotebook(wx.Notebook):
  def __init__(self,parent,envName):
    wx.Notebook.__init__(self,parent,armid.USECASE_NOTEBOOKENVIRONMENT_ID)
    p1 = TextPage(self,armid.USECASE_TEXTPRECONDITION_ID)
    p2 = StepPage(self,envName)
    p3 = TextPage(self,armid.USECASE_TEXTPOSTCONDITION_ID)
    self.AddPage(p1,'Pre-Conditions')
    self.AddPage(p2,'Flow')
    self.AddPage(p3,'Post-Conditions')
