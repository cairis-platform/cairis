#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/AttackerDialog.py $ $Id: AttackerDialog.py 330 2010-10-31 15:01:28Z shaf $
import wx
import armid
import os
import ARM
from Borg import Borg
from AttackerPanel import AttackerPanel
from AttackerParameters import AttackerParameters

class AttackerDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,parameters.id(),parameters.label(),style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(600,600))

    self.theAttackerId = -1
    self.theAttackerName = ''
    self.theAttackerDescription = ''
    self.theAttackerImage = ''
    self.theEnvironmentProperties = []
    self.panel = 0
    self.buildControls(parameters)
    self.theCommitVerb = 'Create'
 
  def load(self,attacker):
    self.theAttackerId = attacker.id()
    imageFile = attacker.image()
    if ((imageFile != None) and (imageFile != '')):
      if (os.path.exists(imageFile) == False):
        attacker.theImage = ''
        errorText = 'Attacker image ' + imageFile + ' does not exist.'
        dlg = wx.MessageDialog(self,errorText,'Load Attacker Image',wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
    self.panel.loadControls(attacker)
    self.theCommitVerb = 'Edit'

  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = AttackerPanel(self)
    self.panel.buildControls(parameters.createFlag())
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.ATTACKER_BUTTONCOMMIT_ID,self.onCommit)


  def onCommit(self,evt):
    nameCtrl = self.FindWindowById(armid.ATTACKER_TEXTNAME_ID)
    descriptionCtrl = self.FindWindowById(armid.ATTACKER_TEXTDESCRIPTION_ID)
    imageCtrl = self.FindWindowById(armid.ATTACKER_IMAGEATTACKERIMAGE_ID)
    environmentCtrl = self.FindWindowById(armid.ATTACKER_PANELENVIRONMENT_ID)

    self.theAttackerName = nameCtrl.GetValue()
    if (self.theCommitVerb == 'Create'):
      b = Borg()
      try:
        b.dbProxy.nameCheck(self.theAttackerName,'attacker')
      except ARM.ARMException,errorText:
        dlg = wx.MessageDialog(self,str(errorText),'Add attacker',wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
        return

    self.theAttackerDescription = descriptionCtrl.GetValue()
    self.theAttackerImage = imageCtrl.personaImage()
    self.theEnvironmentProperties = environmentCtrl.environmentProperties()

    commitLabel = self.theCommitVerb + ' attacker'
    if len(self.theAttackerName) == 0:
      dlg = wx.MessageDialog(self,'Attacker name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theEnvironmentProperties) == 0):
      dlg = wx.MessageDialog(self,'No environments have been associated with this attacker',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      for environmentProperties in self.theEnvironmentProperties:
        if len(environmentProperties.roles()) == 0:
          errorTxt = 'No roles associated with environment ' + environmentProperties.name()
          dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK) 
          dlg.ShowModal()
          dlg.Destroy()
          return
        if len(environmentProperties.motives()) == 0:
          errorTxt = 'No motives associated with environment ' + environmentProperties.name()
          dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK) 
          dlg.ShowModal()
          dlg.Destroy()
          return
        if len(environmentProperties.capabilities()) == 0:
          errorTxt = 'No capabilities associated with environment ' + environmentProperties.name()
          dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK) 
          dlg.ShowModal()
          dlg.Destroy()
          return
      self.EndModal(armid.ATTACKER_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = AttackerParameters(self.theAttackerName,self.theAttackerDescription,self.theAttackerImage,self.theEnvironmentProperties)
    parameters.setId(self.theAttackerId)
    return parameters
