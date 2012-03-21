#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/MisuseCaseNotebook.py $ $Id: MisuseCaseNotebook.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid

class SummaryPage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    objectiveBox = wx.StaticBox(self,-1,'Objective')
    objectiveBoxSizer = wx.StaticBoxSizer(objectiveBox,wx.VERTICAL)
    topSizer.Add(objectiveBoxSizer,0,wx.EXPAND)
    self.objectiveCtrl = wx.TextCtrl(self,armid.MISUSECASE_TEXTOBJECTIVE_ID,'',style=wx.TE_READONLY | wx.TE_MULTILINE)
    objectiveBoxSizer.Add(self.objectiveCtrl,1,wx.EXPAND)

    aaSizer = wx.BoxSizer(wx.HORIZONTAL)
    topSizer.Add(aaSizer,0,wx.EXPAND)
    attackerBox = wx.StaticBox(self)
    attackerBoxSizer = wx.StaticBoxSizer(attackerBox,wx.HORIZONTAL)
    self.attackerList = wx.ListCtrl(self,armid.MISUSECASE_LISTATTACKERS_ID,style=wx.LC_REPORT)
    self.attackerList.InsertColumn(0,'Attacker')
    self.attackerList.SetColumnWidth(0,200)
    attackerBoxSizer.Add(self.attackerList,1,wx.EXPAND)
    aaSizer.Add(attackerBoxSizer,1,wx.EXPAND)
    assetBox = wx.StaticBox(self)
    assetBoxSizer = wx.StaticBoxSizer(assetBox,wx.HORIZONTAL)
    self.assetList = wx.ListCtrl(self,armid.MISUSECASE_LISTASSETS_ID,style=wx.LC_REPORT)
    self.assetList.InsertColumn(0,'Asset')
    self.assetList.SetColumnWidth(0,200)
    assetBoxSizer.Add(self.assetList,1,wx.EXPAND)
    aaSizer.Add(assetBoxSizer,1,wx.EXPAND)

    thrSizer = wx.BoxSizer(wx.HORIZONTAL)
    topSizer.Add(thrSizer,0,wx.EXPAND)
    threatBox = wx.StaticBox(self,-1,'Threat')
    threatBoxSizer = wx.StaticBoxSizer(threatBox,wx.HORIZONTAL)
    self.threatCtrl = wx.TextCtrl(self,armid.MISUSECASE_TEXTTHREAT_ID,'',style=wx.TE_READONLY)
    threatBoxSizer.Add(self.threatCtrl,1,wx.EXPAND)
    thrSizer.Add(threatBoxSizer,1,wx.EXPAND)
    lhoodBox = wx.StaticBox(self,-1,'Likelihood')
    lhoodBoxSizer = wx.StaticBoxSizer(lhoodBox,wx.HORIZONTAL)
    self.lhoodCtrl = wx.TextCtrl(self,armid.MISUSECASE_TEXTLIKELIHOOD_ID,'',style=wx.TE_READONLY)
    lhoodBoxSizer.Add(self.lhoodCtrl,1,wx.EXPAND)
    thrSizer.Add(lhoodBoxSizer,1,wx.EXPAND)

    vulSizer = wx.BoxSizer(wx.HORIZONTAL)
    topSizer.Add(vulSizer,0,wx.EXPAND)
    vulBox = wx.StaticBox(self,-1,'Vulnerability')
    vulBoxSizer = wx.StaticBoxSizer(vulBox,wx.HORIZONTAL)
    self.vulCtrl = wx.TextCtrl(self,armid.MISUSECASE_TEXTVULNERABILITY_ID,'',style=wx.TE_READONLY)
    vulBoxSizer.Add(self.vulCtrl,1,wx.EXPAND)
    vulSizer.Add(vulBoxSizer,1,wx.EXPAND)
    sevBox = wx.StaticBox(self,-1,'Severity')
    sevBoxSizer = wx.StaticBoxSizer(sevBox,wx.HORIZONTAL)
    self.sevCtrl = wx.TextCtrl(self,armid.MISUSECASE_TEXTSEVERITY_ID,'',style=wx.TE_READONLY)
    sevBoxSizer.Add(self.sevCtrl,1,wx.EXPAND)
    vulSizer.Add(sevBoxSizer,1,wx.EXPAND)

    ratingBox = wx.StaticBox(self,-1,'Risk Rating')
    ratingBoxSizer = wx.StaticBoxSizer(ratingBox,wx.HORIZONTAL)
    topSizer.Add(ratingBoxSizer,0,wx.EXPAND)
    self.ratingCtrl = wx.TextCtrl(self,armid.MISUSECASE_TEXTSCORE_ID,'',style=wx.TE_READONLY)
    ratingBoxSizer.Add(self.ratingCtrl,1,wx.EXPAND)

    self.SetSizer(topSizer)

class NarrativePage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    narrativeBox = wx.StaticBox(self,-1,'Narrative')
    narrativeBoxSizer = wx.StaticBoxSizer(narrativeBox,wx.HORIZONTAL)
    topSizer.Add(narrativeBoxSizer,1,wx.EXPAND)
    self.narrativeCtrl = wx.TextCtrl(self,armid.MISUSECASE_TEXTNARRATIVE_ID,'',style=wx.TE_MULTILINE)
    narrativeBoxSizer.Add(self.narrativeCtrl,1,wx.EXPAND)

    self.SetSizer(topSizer)

class MisuseCaseNotebook(wx.Notebook):
  def __init__(self,parent):
    wx.Notebook.__init__(self,parent,armid.MISUSECASE_NOTEBOOK_ID)
    p1 = SummaryPage(self)
    p2 = NarrativePage(self)
    self.AddPage(p1,'Summary')
    self.AddPage(p2,'Narrative')
