#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/RoleDialog.py $ $Id: RoleDialog.py 395 2011-01-06 01:17:45Z shaf $
import wx
import armid
import ARM
from Borg import Borg
from ReferenceSynopsis import ReferenceSynopsis
from ReferenceSynopsisPanel import ReferenceSynopsisPanel

class ReferenceSynopsisDialog(wx.Dialog):
  def __init__(self,parent,objt,charDetails = None):
    wx.Dialog.__init__(self,parent,-1,'Edit Reference Synopsis',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX,size=(475,250))
    self.theReference = objt.reference()
    self.theId = objt.id()
    self.theSynopsis = ''
    self.theDimension = ''
    self.theActorType = ''
    self.theActor = ''
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = ReferenceSynopsisPanel(self)
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.REFERENCESYNOPSIS_BUTTONCOMMIT_ID,self.onCommit)

    if (objt.id() == -1):
      self.theCommitVerb = 'Create'
      if (charDetails != None):
        self.SetLabel = 'Create Characteristic Synopsis'
        charType = charDetails[0]
        tpName = charDetails[1]
        if (charType == 'persona'):
          self.theActorType = 'persona'
          self.theActor = tpName
      else:
        self.SetLabel = 'Create Reference Synopsis'
      objt = ReferenceSynopsis(-1,self.theReference,self.theSynopsis,self.theDimension,self.theActorType,self.theActor)
    else:
      if (charDetails != None):
        self.SetLabel = 'Edit Characteristic Synopsis'

      self.theReference = objt.reference()
      self.theSynopsis = objt.synopsis()
      self.theDimension = objt.dimension()
      self.theActorType = objt.actorType()
      self.theActor = objt.actor()
      self.theCommitVerb = 'Edit'
    self.panel.load(objt,charDetails)
   

  def onCommit(self,evt):
    refCtrl = self.FindWindowById(armid.REFERENCESYNOPSIS_TEXTREFNAME_ID)
    synCtrl = self.FindWindowById(armid.REFERENCESYNOPSIS_TEXTSYNOPSIS_ID)
    dimCtrl = self.FindWindowById(armid.REFERENCESYNOPSIS_COMBODIMENSION_ID)
    atCtrl = self.FindWindowById(armid.REFERENCESYNOPSIS_COMBOACTORTYPE_ID)
    actorCtrl = self.FindWindowById(armid.REFERENCESYNOPSIS_COMBOACTORNAME_ID)

    self.theReference = refCtrl.GetValue()
    self.theSynopsis = synCtrl.GetValue()
    self.theDimension = dimCtrl.GetValue()
    self.theActorType = atCtrl.GetValue()
    self.theActor = actorCtrl.GetValue()


    commitLabel = self.theCommitVerb + ' Reference Synopsis'

    if len(self.theReference) == 0:
      dlg = wx.MessageDialog(self,'Reference cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theSynopsis) == 0:
      dlg = wx.MessageDialog(self,'Synopsis cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theDimension) == 0:
      dlg = wx.MessageDialog(self,'Dimension cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif len(self.theActorType) == 0:
      dlg = wx.MessageDialog(self,'Actor type cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif len(self.theActor) == 0:
      dlg = wx.MessageDialog(self,'Actor cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(armid.REFERENCESYNOPSIS_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = ReferenceSynopsis(self.theId,self.theReference,self.theSynopsis,self.theDimension,self.theActorType,self.theActor)
    return parameters
