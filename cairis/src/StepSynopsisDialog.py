#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/RoleDialog.py $ $Id: RoleDialog.py 395 2011-01-06 01:17:45Z shaf $
import wx
import armid
import WidgetFactory
import ARM
from Borg import Borg
from StepSynopsisPanel import StepSynopsisPanel

class StepSynopsisDialog(wx.Dialog):
  def __init__(self,parent,stepSyn,stepActor,stepActorType):
    wx.Dialog.__init__(self,parent,-1,'Edit Step Synopsis',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX,size=(475,150))
    self.theSynopsis = ''
    self.theActorType = ''
    self.theActor = ''
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = StepSynopsisPanel(self)
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.STEPSYNOPSIS_BUTTONCOMMIT_ID,self.onCommit)

    if (self.theSynopsis == ''):
      self.SetLabel = 'Create Step Synopsis'
    self.panel.load(stepSyn,stepActor,stepActorType)
   

  def onCommit(self,evt):
    synCtrl = self.FindWindowById(armid.STEPSYNOPSIS_TEXTSYNOPSIS_ID)
    atCtrl = self.FindWindowById(armid.STEPSYNOPSIS_COMBOACTORTYPE_ID)
    actorCtrl = self.FindWindowById(armid.STEPSYNOPSIS_COMBOACTORNAME_ID)

    self.theSynopsis = synCtrl.GetValue()
    self.theActorType = atCtrl.GetValue()
    self.theActor = actorCtrl.GetValue()

    self.EndModal(armid.STEPSYNOPSIS_BUTTONCOMMIT_ID)

  def synopsis(self):
    return self.theSynopsis

  def actor(self):
    return self.theActor

  def actorType(self):
    return self.theActorType
