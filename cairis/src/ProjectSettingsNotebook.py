#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ProjectSettingsNotebook.py $ $Id: ProjectSettingsNotebook.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
from DictionaryListCtrl import DictionaryListCtrl
from ContributorListCtrl import ContributorListCtrl
from RevisionListCtrl import RevisionListCtrl
from DomainListCtrl import DomainListCtrl
from PersonalImageView import PersonalImageView

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

class BackgroundPage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    nameBox = wx.StaticBox(self,-1,'Project Name')
    nameBoxSizer = wx.StaticBoxSizer(nameBox,wx.HORIZONTAL)
    topSizer.Add(nameBoxSizer,0,wx.EXPAND)
    self.nameCtrl = wx.TextCtrl(self,armid.PROJECTSETTINGS_TEXTPROJECTNAME_ID,'')
    nameBoxSizer.Add(self.nameCtrl,1,wx.EXPAND)

    narrativeBox = wx.StaticBox(self,-1,'Project Background')
    narrativeBoxSizer = wx.StaticBoxSizer(narrativeBox,wx.HORIZONTAL)
    topSizer.Add(narrativeBoxSizer,1,wx.EXPAND)
    self.narrativeCtrl = wx.TextCtrl(self,armid.PROJECTSETTINGS_TEXTBACKGROUND_ID,'',style=wx.TE_MULTILINE)
    narrativeBoxSizer.Add(self.narrativeCtrl,1,wx.EXPAND)

    self.SetSizer(topSizer)

class DictionaryPage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    dBox = wx.StaticBox(self,-1)
    dBoxSizer = wx.StaticBoxSizer(dBox,wx.HORIZONTAL)
    topSizer.Add(dBoxSizer,1,wx.EXPAND)
    self.dictionaryCtrl = DictionaryListCtrl(self)
    dBoxSizer.Add(self.dictionaryCtrl,1,wx.EXPAND)
    self.SetSizer(topSizer)

class RichPicturePage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    iBox = wx.StaticBox(self,-1)
    iSizer = wx.StaticBoxSizer(iBox,wx.HORIZONTAL)
    topSizer.Add(iSizer,1,wx.EXPAND)
    imagePanel = PersonalImageView(self,armid.PROJECTSETTINGS_IMAGERICHPICTURE_ID)
    iSizer.Add(imagePanel,1,wx.EXPAND)

    self.SetSizer(topSizer)

class ContributorPage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    dBox = wx.StaticBox(self,-1)
    dBoxSizer = wx.StaticBoxSizer(dBox,wx.HORIZONTAL)
    topSizer.Add(dBoxSizer,1,wx.EXPAND)
    self.contributorCtrl = ContributorListCtrl(self)
    dBoxSizer.Add(self.contributorCtrl,1,wx.EXPAND)
    self.SetSizer(topSizer)

class RevisionPage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    dBox = wx.StaticBox(self,-1)
    dBoxSizer = wx.StaticBoxSizer(dBox,wx.HORIZONTAL)
    topSizer.Add(dBoxSizer,1,wx.EXPAND)
    self.revisionCtrl = RevisionListCtrl(self)
    dBoxSizer.Add(self.revisionCtrl,1,wx.EXPAND)
    self.SetSizer(topSizer)

class ProjectSettingsNotebook(wx.Notebook):
  def __init__(self,parent):
    wx.Notebook.__init__(self,parent,armid.PROJECTSETTINGS_NOTEBOOKSETTINGS_ID)
    p1 = BackgroundPage(self)
    p2 = MLTextPage(self,armid.PROJECTSETTINGS_TEXTGOALS_ID)
    p3 = MLTextPage(self,armid.PROJECTSETTINGS_TEXTSCOPE_ID)
    p4 = RichPicturePage(self)
    p5 = DictionaryPage(self)
    p6 = ContributorPage(self)
    p7 = RevisionPage(self)
    self.AddPage(p1,'Background')
    self.AddPage(p2,'Goals')
    self.AddPage(p3,'Scope')
    self.AddPage(p4,'Rich Picture')
    self.AddPage(p5,'Naming Conventions')
    self.AddPage(p6,'Contributors')
    self.AddPage(p7,'Revisions')
