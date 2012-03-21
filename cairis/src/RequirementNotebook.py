#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/RequirementNotebook.py $ $Id: RequirementNotebook.py 564 2012-03-12 17:53:00Z shaf $
import wx
import armid

class MLTextPage(wx.Panel):
  def __init__(self,parent,winId):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    narrativeBox = wx.StaticBox(self,-1)
    narrativeBoxSizer = wx.StaticBoxSizer(narrativeBox,wx.HORIZONTAL)
    topSizer.Add(narrativeBoxSizer,1,wx.EXPAND)
    self.narrativeCtrl = wx.TextCtrl(self,winId,'None',style=wx.TE_MULTILINE)
    narrativeBoxSizer.Add(self.narrativeCtrl,1,wx.EXPAND)
    self.SetSizer(topSizer)

class SummaryPage(wx.Panel):
  def __init__(self,parent,assets):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    nameBox = wx.StaticBox(self,-1,'Name')
    nameBoxSizer = wx.StaticBoxSizer(nameBox,wx.HORIZONTAL)
    topSizer.Add(nameBoxSizer,0,wx.EXPAND)
    self.nameCtrl = wx.TextCtrl(self,armid.PATTERNREQUIREMENT_TEXTNAME_ID,'')
    nameBoxSizer.Add(self.nameCtrl,1,wx.EXPAND)

    assetBox = wx.StaticBox(self,-1,'Asset')
    assetBoxSizer = wx.StaticBoxSizer(assetBox,wx.HORIZONTAL)
    topSizer.Add(assetBoxSizer,0,wx.EXPAND)
    self.assetCtrl = wx.ComboBox(self,armid.PATTERNREQUIREMENT_COMBOASSET_ID,choices=assets,size=wx.DefaultSize,style=wx.CB_READONLY)
    assetBoxSizer.Add(self.assetCtrl,1,wx.EXPAND)

    typeBox = wx.StaticBox(self,-1,'Type')
    typeBoxSizer = wx.StaticBoxSizer(typeBox,wx.HORIZONTAL)
    topSizer.Add(typeBoxSizer,0,wx.EXPAND)
    typeChoices = ['Functional','Data','Look and Feel','Usability','Performance','Operational','Maintainability','Portability','Security','Cultural and Political','Legal','Privacy']
    self.typeCtrl = wx.ComboBox(self,armid.PATTERNREQUIREMENT_COMBOTYPE_ID,choices=typeChoices,size=wx.DefaultSize,style=wx.CB_READONLY)
    typeBoxSizer.Add(self.typeCtrl,1,wx.EXPAND)

    descBox = wx.StaticBox(self,-1,'Description')
    descBoxSizer = wx.StaticBoxSizer(descBox,wx.HORIZONTAL)
    topSizer.Add(descBoxSizer,1,wx.EXPAND)
    self.descriptionCtrl = wx.TextCtrl(self,armid.PATTERNREQUIREMENT_TEXTDESCRIPTION_ID,'',style=wx.TE_MULTILINE)
    descBoxSizer.Add(self.descriptionCtrl,1,wx.EXPAND)

    self.SetSizer(topSizer)

class RequirementNotebook(wx.Notebook):
  def __init__(self,parent,assets):
    wx.Notebook.__init__(self,parent,armid.SECURITYPATTERN_NOTEBOOKPATTERN_ID)
    p1 = SummaryPage(self,assets)
    p2 = MLTextPage(self,armid.PATTERNREQUIREMENT_TEXTRATIONALE_ID)
    p3 = MLTextPage(self,armid.PATTERNREQUIREMENT_TEXTFITCRITERION_ID)
    self.AddPage(p1,'Summary')
    self.AddPage(p2,'Rationale')
    self.AddPage(p3,'Fit Criterion')
