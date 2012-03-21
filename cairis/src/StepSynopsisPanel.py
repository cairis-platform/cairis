#$URL$
import wx
import armid
import WidgetFactory
from Borg import Borg

class StepSynopsisPanel(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,armid.STEPSYNOPSIS_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Synopsis',(87,30),armid.STEPSYNOPSIS_TEXTSYNOPSIS_ID),0,wx.EXPAND)
    actorSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(actorSizer,0,wx.EXPAND)
    actorSizer.Add(WidgetFactory.buildComboSizerList(self,'Actor Type',(87,30),armid.STEPSYNOPSIS_COMBOACTORTYPE_ID,['asset','role']),1,wx.EXPAND)
    actorSizer.Add(WidgetFactory.buildComboSizerList(self,'Actor',(87,30),armid.STEPSYNOPSIS_COMBOACTORNAME_ID,['']),1,wx.EXPAND)
    mainSizer.Add(wx.StaticText(self,-1,''),1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildCommitButtonSizer(self,armid.STEPSYNOPSIS_BUTTONCOMMIT_ID,True),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)
    wx.EVT_COMBOBOX(self,armid.STEPSYNOPSIS_COMBOACTORTYPE_ID,self.onActorType)


  def load(self,stepSyn,stepActor,stepActorType):
    synCtrl = self.FindWindowById(armid.STEPSYNOPSIS_TEXTSYNOPSIS_ID)
    actorTypeCtrl = self.FindWindowById(armid.STEPSYNOPSIS_COMBOACTORTYPE_ID)
    actorCtrl = self.FindWindowById(armid.STEPSYNOPSIS_COMBOACTORNAME_ID)
    synCtrl.SetValue(stepSyn)
    actorTypeCtrl.SetValue(stepActorType)
    if stepActor != '':
      self.setActorNames(stepActorType)
    actorCtrl.SetValue(stepActor)

  def onActorType(self,evt):
    self.setActorNames(evt.GetString())

  def setActorNames(self,actorType):
    aNames = self.dbProxy.getDimensionNames(actorType)
    actorCtrl = self.FindWindowById(armid.STEPSYNOPSIS_COMBOACTORNAME_ID)
    actorCtrl.SetItems(aNames)
    actorCtrl.SetValue('')
