#$URL$
import wx
import armid
from BasePanel import BasePanel
from Borg import Borg

class ReferenceSynopsisPanel(BasePanel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,armid.REFERENCESYNOPSIS_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(self.buildTextSizer('Reference',(87,30),armid.REFERENCESYNOPSIS_TEXTREFNAME_ID),0,wx.EXPAND)
    mainSizer.Add(self.buildTextSizer('Synopsis',(87,30),armid.REFERENCESYNOPSIS_TEXTSYNOPSIS_ID),0,wx.EXPAND)
    dimTypes = self.dbProxy.getDimensionNames('trace_dimension')
    mainSizer.Add(self.buildComboSizerList('Dimension',(87,30),armid.REFERENCESYNOPSIS_COMBODIMENSION_ID,dimTypes),0,wx.EXPAND)

    actorSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(actorSizer,0,wx.EXPAND)
    actorSizer.Add(self.buildComboSizerList('Actor Type',(87,30),armid.REFERENCESYNOPSIS_COMBOACTORTYPE_ID,['asset','persona']),1,wx.EXPAND)
    actorSizer.Add(self.buildComboSizerList('Actor',(87,30),armid.REFERENCESYNOPSIS_COMBOACTORNAME_ID,['']),1,wx.EXPAND)
    mainSizer.Add(wx.StaticText(self,-1,''),1,wx.EXPAND)
    mainSizer.Add(self.buildCommitButtonSizer(armid.REFERENCESYNOPSIS_BUTTONCOMMIT_ID,True),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)
    wx.EVT_COMBOBOX(self,armid.REFERENCESYNOPSIS_COMBOACTORTYPE_ID,self.onActorType)


  def load(self,refsyn,charDetails = None):
    refCtrl = self.FindWindowById(armid.REFERENCESYNOPSIS_TEXTREFNAME_ID)
    synCtrl = self.FindWindowById(armid.REFERENCESYNOPSIS_TEXTSYNOPSIS_ID)
    dimCtrl = self.FindWindowById(armid.REFERENCESYNOPSIS_COMBODIMENSION_ID)
    actorTypeCtrl = self.FindWindowById(armid.REFERENCESYNOPSIS_COMBOACTORTYPE_ID)
    actorCtrl = self.FindWindowById(armid.REFERENCESYNOPSIS_COMBOACTORNAME_ID)
    refCtrl.SetValue(refsyn.reference())
    synCtrl.SetValue(refsyn.synopsis())
    dimCtrl.SetValue(refsyn.dimension())
    actorType = refsyn.actorType()
    actorTypeCtrl.SetValue(actorType)
    if actorType != '':
      self.setActorNames(actorType)
    actorCtrl.SetValue(refsyn.actor())
    refCtrl.Disable()

    if charDetails != None:
      charType = charDetails[0]
      if charType == 'persona':
        actorTypeCtrl.Disable()
        actorCtrl.Disable()

  def onActorType(self,evt):
    self.setActorNames(evt.GetString())

  def setActorNames(self,actorType):
    aNames = self.dbProxy.getDimensionNames(actorType)
    actorCtrl = self.FindWindowById(armid.REFERENCESYNOPSIS_COMBOACTORNAME_ID)
    actorCtrl.SetItems(aNames)
