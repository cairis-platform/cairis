#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/SecurityPatternNotebook.py $ $Id: SecurityPatternNotebook.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
from PatternStructureListCtrl import PatternStructureListCtrl
from RequirementListCtrl import RequirementListCtrl

class MLTextPage(wx.Panel):
  def __init__(self,parent,winId):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    narrativeBox = wx.StaticBox(self,-1)
    narrativeBoxSizer = wx.StaticBoxSizer(narrativeBox,wx.HORIZONTAL)
    topSizer.Add(narrativeBoxSizer,1,wx.EXPAND)
    self.narrativeCtrl = wx.TextCtrl(self,winId,'',style=wx.TE_MULTILINE)
    narrativeBoxSizer.Add(self.narrativeCtrl,1,wx.EXPAND)
    self.SetSizer(topSizer)

class StructurePage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)
    asBox = wx.StaticBox(self,-1)
    asBoxSizer = wx.StaticBoxSizer(asBox,wx.HORIZONTAL)
    topSizer.Add(asBoxSizer,1,wx.EXPAND)
    self.associationList = PatternStructureListCtrl(self)
    asBoxSizer.Add(self.associationList,1,wx.EXPAND)
    self.SetSizer(topSizer)

class RequirementsPage(wx.Panel):
  def __init__(self,parent,structPage):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)
    asBox = wx.StaticBox(self,-1)
    asBoxSizer = wx.StaticBoxSizer(asBox,wx.HORIZONTAL)
    topSizer.Add(asBoxSizer,1,wx.EXPAND)
    self.requirementList = RequirementListCtrl(self,structPage.associationList)
    asBoxSizer.Add(self.requirementList,1,wx.EXPAND)
    self.SetSizer(topSizer)

class SecurityPatternNotebook(wx.Notebook):
  def __init__(self,parent):
    wx.Notebook.__init__(self,parent,armid.SECURITYPATTERN_NOTEBOOKPATTERN_ID)
    p1 = MLTextPage(self,armid.SECURITYPATTERN_TEXTCONTEXT_ID)
    p2 = MLTextPage(self,armid.SECURITYPATTERN_TEXTPROBLEM_ID)
    p3 = MLTextPage(self,armid.SECURITYPATTERN_TEXTSOLUTION_ID)
    p4 = StructurePage(self)
    p5 = RequirementsPage(self,p4)
    self.AddPage(p1,'Context')
    self.AddPage(p2,'Problem')
    self.AddPage(p3,'Solution')
    self.AddPage(p4,'Structure')
    self.AddPage(p5,'Requirements')
