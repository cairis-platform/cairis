#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/SingleRequirementDialog.py $ $Id: SingleRequirementDialog.py 368 2010-12-15 17:04:13Z shaf $
import wx
import armid
import WidgetFactory
from SingleRequirementNotebook import SingleRequirementNotebook

class SingleRequirementDialog(wx.Dialog):
  def __init__(self,parent):
    wx.Dialog.__init__(self,parent,armid.SINGLEREQUIREMENT_ID,'Add Requirement',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,475))
    self.theType = ''
    self.theReferrerType = 'asset'
    self.theReferrer = ''
    self.thePriority = '1'
    self.theDescription = ''
    self.theRationale = ''
    self.theFitCriterion = ''
    self.theOriginator = ''
    self.theContributionType = 'and'
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    
    mainSizer.Add(SingleRequirementNotebook(self),1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildAddCancelButtonSizer(self,armid.SINGLEREQUIREMENT_BUTTONCOMMIT_ID),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

    wx.EVT_BUTTON(self,armid.SINGLEREQUIREMENT_BUTTONCOMMIT_ID,self.onCommit)
    self.commitLabel = 'Add'
      

  def onCommit(self,evt):
    typeCtrl = self.FindWindowById(armid.SINGLEREQUIREMENT_COMBOTYPE_ID)
    assetCtrl = self.FindWindowById(armid.SINGLEREQUIREMENT_RADIOASSET_ID)
    envCtrl = self.FindWindowById(armid.SINGLEREQUIREMENT_RADIOENVIRONMENT_ID)
    refCtrl = self.FindWindowById(armid.SINGLEREQUIREMENT_COMBOREFERRER_ID)
    priCtrl = self.FindWindowById(armid.SINGLEREQUIREMENT_COMBOPRIORITY_ID)
    descCtrl = self.FindWindowById(armid.SINGLEREQUIREMENT_TEXTDESCRIPTION_ID)
    ctCtrl = self.FindWindowById(armid.SINGLEREQUIREMENT_COMBOCONTRIBUTIONTYPE_ID)
    rationaleCtrl = self.FindWindowById(armid.SINGLEREQUIREMENT_TEXTRATIONALE_ID)
    fcCtrl = self.FindWindowById(armid.SINGLEREQUIREMENT_TEXTFITCRITERION_ID)
    originatorCtrl = self.FindWindowById(armid.SINGLEREQUIREMENT_TEXTORIGINATOR_ID)


    self.theType = typeCtrl.GetStringSelection()
    if (assetCtrl.GetValue() == True):
      self.theReferrerType = 'asset'
    else:
      self.theReferrerType = 'environment'

    if (ctCtrl.GetValue() == 'Obstructs'):
      self.theContributionType = 'obstruct'

    self.theReferrer = refCtrl.GetStringSelection()
    self.thePriority = priCtrl.GetStringSelection()
    self.theDescription = descCtrl.GetValue()
    self.theRationale = rationaleCtrl.GetValue()
    self.theFitCriterion = fcCtrl.GetValue()
    self.theOriginator = originatorCtrl.GetValue()

    if (len(self.theType) == 0):
      dlg = wx.MessageDialog(self,'No type selected',self.commitLabel + ' Requirement',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theReferrer) == 0):
      dlg = wx.MessageDialog(self,'No referrer selected',self.commitLabel + ' Requirement',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.thePriority) == 0):
      dlg = wx.MessageDialog(self,'No priority selected',self.commitLabel + ' Requirement',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theDescription) == 0):
      dlg = wx.MessageDialog(self,'No description entered',self.commitLabel + ' Requirement',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theRationale) == 0):
      dlg = wx.MessageDialog(self,'No rationale entered',self.commitLabel + ' Requirement',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theFitCriterion) == 0):
      dlg = wx.MessageDialog(self,'No fit criterion entered',self.commitLabel + ' Requirement',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theOriginator) == 0):
      dlg = wx.MessageDialog(self,'No originator entered',self.commitLabel + ' Requirement',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(armid.SINGLEREQUIREMENT_BUTTONCOMMIT_ID)

  def type(self): return self.theType
  def referrerType(self): return self.theReferrerType
  def referrer(self): return self.theReferrer
  def priority(self): return self.thePriority
  def description(self): return self.theDescription
  def rationale(self): return self.theRationale
  def fitCriterion(self): return self.theFitCriterion
  def originator(self): return self.theOriginator
