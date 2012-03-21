#$URL$

import wx
import armid
import ARM
from Borg import Borg
from ReferenceContribution import ReferenceContribution
from UseCaseContributionPanel import UseCaseContributionPanel

class UseCaseContributionDialog(wx.Dialog):
  def __init__(self,parent,objt,rType):
    wx.Dialog.__init__(self,parent,-1,'Edit Use Case Contribution',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX,size=(475,300))
    self.theSource = objt.source()
    self.theDestination = objt.destination()
    self.theMeansEnd = objt.meansEnd()
    self.theContribution = objt.contribution()
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = UseCaseContributionPanel(self)
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.REFERENCECONTRIBUTION_BUTTONCOMMIT_ID,self.onCommit)

    if (objt.meansEnd() != ''):
      self.theCommitVerb = 'Create'
      self.SetLabel = 'Create Reference Contribution'
    else:
      self.theCommitVerb = 'Edit'
    self.panel.load(objt,rType)
   

  def onCommit(self,evt):
    charCtrl = self.FindWindowById(armid.REFERENCECONTRIBUTION_COMBOSOURCE_ID)
    refCtrl = self.FindWindowById(armid.REFERENCECONTRIBUTION_COMBODESTINATION_ID)
    meCtrl = self.FindWindowById(armid.REFERENCECONTRIBUTION_COMBOMEANSEND_ID)
    contCtrl = self.FindWindowById(armid.REFERENCECONTRIBUTION_COMBOCONTRIBUTION_ID)

    self.theSource = charCtrl.GetValue()
    self.theDestination = refCtrl.GetValue()
    self.theMeansEnd = meCtrl.GetValue()
    self.theContribution = contCtrl.GetValue()


    commitLabel = self.theCommitVerb + ' Use Case Contribution'

    if len(self.theSource) == 0:
      dlg = wx.MessageDialog(self,'Characteristic cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theDestination) == 0:
      dlg = wx.MessageDialog(self,'Reference cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theMeansEnd) == 0:
      dlg = wx.MessageDialog(self,'Means/End cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif len(self.theContribution) == 0:
      dlg = wx.MessageDialog(self,'Contribution cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(armid.REFERENCECONTRIBUTION_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = ReferenceContribution(self.theSource,self.theDestination,self.theMeansEnd,self.theContribution)
    return parameters
