#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/AssetSummaryNotebook.py $ $Id: AssetSummaryNotebook.py 330 2010-10-31 15:01:28Z shaf $
import wx
import armid
from DimensionListCtrl import DimensionListCtrl

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

class CriticalPage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    crBoxSizer = wx.BoxSizer(wx.VERTICAL)
    topSizer.Add(crBoxSizer,0,wx.EXPAND)
    self.criticalCheckCtrl = wx.CheckBox(self,armid.ASSET_CHECKCRITICAL_ID,'Critical Asset')
    self.criticalCheckCtrl.SetValue(False)
    crBoxSizer.Add(self.criticalCheckCtrl,0,wx.EXPAND)
    self.criticalRationaleCtrl = wx.TextCtrl(self,armid.ASSET_TEXTCRITICALRATIONALE_ID,'',style=wx.TE_MULTILINE)
    self.criticalRationaleCtrl.Disable()
    crBoxSizer.Add(self.criticalRationaleCtrl,1,wx.EXPAND)
    self.SetSizer(topSizer)
    wx.EVT_CHECKBOX(self,armid.ASSET_CHECKCRITICAL_ID,self.onCheckCritical)

  def onCheckCritical(self,evt):
    if (self.criticalCheckCtrl.GetValue() == True):
      self.criticalRationaleCtrl.Enable()
    else:
      self.criticalRationaleCtrl.Disable()
      self.criticalRationaleCtrl.Clear()

class AssetSummaryNotebook(wx.Notebook):
  def __init__(self,parent):
    wx.Notebook.__init__(self,parent,armid.ASSET_NOTEBOOKSUMMARY_ID)
    p1 = MLTextPage(self,armid.ASSET_TEXTDESCRIPTION_ID)
    p2 = MLTextPage(self,armid.ASSET_TEXTSIGNIFICANCE_ID)
    p3 = CriticalPage(self)
    self.AddPage(p1,'Description')
    self.AddPage(p2,'Significance')
    self.AddPage(p3,'Criticality')
