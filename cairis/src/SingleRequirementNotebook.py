#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/SingleRequirementNotebook.py $ $Id: SingleRequirementNotebook.py 406 2011-01-13 00:25:07Z shaf $
import wx
import armid
from Borg import Borg

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
  def __init__(self,parent):
    wx.Panel.__init__(self,parent)
    b = Borg()
    self.dbProxy = b.dbProxy
    topSizer = wx.BoxSizer(wx.VERTICAL)

    typeBox = wx.StaticBox(self,-1,'Type')
    typeBoxSizer = wx.StaticBoxSizer(typeBox,wx.HORIZONTAL)
    topSizer.Add(typeBoxSizer,0,wx.EXPAND)
    typeChoices = ['Functional','Data','Look and Feel','Usability','Performance','Operational','Maintainability','Portability','Security','Cultural and Political','Legal','Privacy']
    self.typeCtrl = wx.ComboBox(self,armid.SINGLEREQUIREMENT_COMBOTYPE_ID,choices=typeChoices,size=wx.DefaultSize,style=wx.CB_READONLY)
    typeBoxSizer.Add(self.typeCtrl,1,wx.EXPAND)

    radioBox = wx.StaticBox(self,-1,'Referrer')
    radioSizer = wx.StaticBoxSizer(radioBox,wx.HORIZONTAL)
    topSizer.Add(radioSizer,0,wx.EXPAND)
    radioSizer.Add(wx.RadioButton(self,armid.SINGLEREQUIREMENT_RADIOASSET_ID,'Asset',style=wx.RB_GROUP))
    radioSizer.Add(wx.RadioButton(self,armid.SINGLEREQUIREMENT_RADIOENVIRONMENT_ID,'Environment',style=0))
    self.refCtrl = wx.ComboBox(self,armid.SINGLEREQUIREMENT_COMBOREFERRER_ID,choices=self.dbProxy.getDimensionNames('asset'),size=wx.DefaultSize,style=wx.CB_READONLY)
    radioSizer.Add(self.refCtrl,1,wx.EXPAND)
    wx.EVT_RADIOBUTTON(self,armid.SINGLEREQUIREMENT_RADIOASSET_ID,self.onAssetSelected)
    wx.EVT_RADIOBUTTON(self,armid.SINGLEREQUIREMENT_RADIOENVIRONMENT_ID,self.onEnvironmentSelected)
    

    priBox = wx.StaticBox(self,-1,'Priority')
    priBoxSizer = wx.StaticBoxSizer(priBox,wx.HORIZONTAL)
    topSizer.Add(priBoxSizer,0,wx.EXPAND)
    self.priorityCtrl = wx.ComboBox(self,armid.SINGLEREQUIREMENT_COMBOPRIORITY_ID,choices=['1','2','3'],size=wx.DefaultSize,style=wx.CB_READONLY)
    priBoxSizer.Add(self.priorityCtrl,1,wx.EXPAND)
   
    descBox = wx.StaticBox(self,-1,'Description')
    descBoxSizer = wx.StaticBoxSizer(descBox,wx.HORIZONTAL)
    topSizer.Add(descBoxSizer,1,wx.EXPAND)
    self.descriptionCtrl = wx.TextCtrl(self,armid.SINGLEREQUIREMENT_TEXTDESCRIPTION_ID,'',style=wx.TE_MULTILINE)
    descBoxSizer.Add(self.descriptionCtrl,1,wx.EXPAND)

    ctBox = wx.StaticBox(self,-1,'Contribution Type')
    ctBoxSizer = wx.StaticBoxSizer(ctBox,wx.HORIZONTAL)
    topSizer.Add(ctBoxSizer,0,wx.EXPAND)
    self.ctCtrl = wx.ComboBox(self,armid.SINGLEREQUIREMENT_COMBOCONTRIBUTIONTYPE_ID,choices=['Operationalises','Obstructs'],size=wx.DefaultSize,style=wx.CB_READONLY)
    self.ctCtrl.SetSelection(0)
    ctBoxSizer.Add(self.ctCtrl,1,wx.EXPAND)

    self.SetSizer(topSizer)

  def onAssetSelected(self,evt):
    self.refCtrl.SetItems(self.dbProxy.getDimensionNames('asset'))
    self.refCtrl.SetValue('')

  def onEnvironmentSelected(self,evt):
    self.refCtrl.SetItems(self.dbProxy.getDimensionNames('environment'))
    self.refCtrl.SetValue('')

class SingleRequirementNotebook(wx.Notebook):
  def __init__(self,parent):
    wx.Notebook.__init__(self,parent,armid.SINGLEREQUIREMENT_NOTEBOOKREQUIREMENT_ID)
    p1 = SummaryPage(self)
    p2 = MLTextPage(self,armid.SINGLEREQUIREMENT_TEXTRATIONALE_ID)
    p3 = MLTextPage(self,armid.SINGLEREQUIREMENT_TEXTFITCRITERION_ID)
    p4 = MLTextPage(self,armid.SINGLEREQUIREMENT_TEXTORIGINATOR_ID)
    self.AddPage(p1,'Definition')
    self.AddPage(p2,'Rationale')
    self.AddPage(p3,'Fit Criterion')
    self.AddPage(p4,'Originator')
