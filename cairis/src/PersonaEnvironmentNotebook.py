#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/PersonaEnvironmentNotebook.py $ $Id: PersonaEnvironmentNotebook.py 265 2010-06-21 22:20:07Z shaf $
import wx
import armid
from DimensionListCtrl import DimensionListCtrl
from BVNarrativeTextCtrl import BVNarrativeTextCtrl

class SummaryPage(wx.Panel):
  def __init__(self,parent,dp):
    wx.Panel.__init__(self,parent)
    self.dbProxy = dp
    topSizer = wx.BoxSizer(wx.VERTICAL)

    directBox = wx.StaticBox(self,-1,'Direct/Indirect Persona')
    directSizer = wx.StaticBoxSizer(directBox,wx.HORIZONTAL)
    topSizer.Add(directSizer,0,wx.EXPAND)
    self.directCtrl = wx.CheckBox(self,armid.PERSONA_CHECKDIRECT_ID)
    self.directCtrl.SetValue(True)
    directSizer.Add(self.directCtrl,0,wx.EXPAND)

    roleBox = wx.StaticBox(self)
    roleSizer = wx.StaticBoxSizer(roleBox,wx.HORIZONTAL)
    topSizer.Add(roleSizer,1,wx.EXPAND)
    self.roleList = DimensionListCtrl(self,armid.PERSONA_LISTROLES_ID,wx.DefaultSize,'Role','role',self.dbProxy)
    roleSizer.Add(self.roleList,1,wx.EXPAND)

    self.SetSizer(topSizer)

class NarrativePage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    narrativeBox = wx.StaticBox(self,-1)
    narrativeBoxSizer = wx.StaticBoxSizer(narrativeBox,wx.HORIZONTAL)
    topSizer.Add(narrativeBoxSizer,1,wx.EXPAND)
    self.narrativeCtrl = BVNarrativeTextCtrl(self,armid.PERSONA_TEXTNARRATIVE_ID)
    narrativeBoxSizer.Add(self.narrativeCtrl,1,wx.EXPAND)

    self.SetSizer(topSizer)

class PersonaEnvironmentNotebook(wx.Notebook):
  def __init__(self,parent,dp):
    wx.Notebook.__init__(self,parent,armid.PERSONA_NOTEBOOKENVIRONMENT_ID)
    p1 = SummaryPage(self,dp)
    p2 = NarrativePage(self)
    self.AddPage(p1,'Summary')
    self.AddPage(p2,'Narrative')
