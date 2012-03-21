#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/RiskDialog.py $ $Id: RiskDialog.py 287 2010-07-03 19:03:03Z shaf $
import wx
import armid
import WidgetFactory
import ObjectFactory
import ARM
from Borg import Borg
from DialogClassParameters import DialogClassParameters
from RiskParameters import RiskParameters
from RiskDialogParameters import RiskDialogParameters
from RiskPanel import RiskPanel
from MisuseCaseDialog import MisuseCaseDialog

class RiskDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,parameters.id(),parameters.label(),style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,450))

    self.theRiskId = -1
    self.theMisuseCase = None
    self.theThreatName = ''
    self.theVulnerabilityName = ''
    self.panel = 0
    self.buildControls(parameters)
    self.commitVerb = 'Create'
 
  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = RiskPanel(self)
    self.panel.buildControls(parameters.createFlag())
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.RISK_BUTTONCOMMIT_ID,self.onCommit)
    wx.EVT_BUTTON(self,armid.RISK_BUTTONMISUSECASE_ID,self.onMisuseCase)

  def load(self,risk):
    self.theRiskId = risk.id()
    self.theMisuseCase = risk.misuseCase()
    self.panel.loadControls(risk)
    self.commitVerb = 'Edit'
    if (self.theMisuseCase != None):
      mcButton = self.FindWindowById(armid.RISK_BUTTONMISUSECASE_ID)
      mcButton.SetLabel('Edit Misuse Case')
    

  def onMisuseCase(self,evt):
    nameCtrl = self.FindWindowById(armid.RISK_TEXTNAME_ID)
    threatCtrl = self.FindWindowById(armid.RISK_COMBOTHREAT_ID)
    vulCtrl = self.FindWindowById(armid.RISK_COMBOVULNERABILITY_ID)

    riskName = nameCtrl.GetValue() 
    if (self.commitVerb == 'Create'):
      b = Borg()
      try:
        b.dbProxy.nameCheck(riskName,'risk')
      except ARM.ARMException,errorText:
        dlg = wx.MessageDialog(self,str(errorText),'Add Misuse Case',wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
        return

    threatName = threatCtrl.GetStringSelection()
    vulnerabilityName = vulCtrl.GetStringSelection()

    commitLabel = self.commitVerb + ' risk'
    if len(riskName) == 0:
      dlg = wx.MessageDialog(self,'No risk name entered',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(threatName) == 0:
      dlg = wx.MessageDialog(self,'No threat selected',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(vulnerabilityName) == 0):
      dlg = wx.MessageDialog(self,'No vulnerability selected',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return

    isCreate = False
    if (self.theMisuseCase == None):
      isCreate = True
    dlg = MisuseCaseDialog(self,isCreate)
    if (self.theMisuseCase != None):
      self.theMisuseCase.theThreatName = threatName
      self.theMisuseCase.theVulnerabilityName = vulnerabilityName
      dlg.loadMisuseCase(self.theMisuseCase)
    else:
      dlg.loadRiskComponents(riskName,threatName,vulnerabilityName)
    if (dlg.ShowModal() == armid.MISUSECASE_BUTTONCOMMIT_ID):
      if (self.theMisuseCase != None):
        self.theMisuseCase = ObjectFactory.build(self.theMisuseCase.id(),dlg.parameters())
      else:
        self.theMisuseCase = ObjectFactory.build(-1,dlg.parameters())
      mcButton = self.FindWindowById(armid.RISK_BUTTONMISUSECASE_ID)
      mcButton.SetLabel('Edit Misuse Case')

  def onCommit(self,evt):
    nameCtrl = self.FindWindowById(armid.RISK_TEXTNAME_ID)
    threatCtrl = self.FindWindowById(armid.RISK_COMBOTHREAT_ID)
    vulCtrl = self.FindWindowById(armid.RISK_COMBOVULNERABILITY_ID)

    commitLabel = self.commitVerb + ' risk'
    self.theRiskName = nameCtrl.GetValue() 
    b = Borg()
    if (self.commitVerb == 'Create'):
      try:
        b.dbProxy.nameCheck(self.theRiskName,'risk')
      except ARM.ARMException,errorText:
        dlg = wx.MessageDialog(self,str(errorText),commitLabel,wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
        return

    self.theThreatName = threatCtrl.GetStringSelection()
    self.theVulnerabilityName = vulCtrl.GetStringSelection()

    if len(self.theRiskName) == 0:
      dlg = wx.MessageDialog(self,'No risk name entered',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theThreatName) == 0:
      dlg = wx.MessageDialog(self,'No threat selected',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theVulnerabilityName) == 0):
      dlg = wx.MessageDialog(self,'No vulnerability selected',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (self.theMisuseCase == None):
      dlg = wx.MessageDialog(self,'No Misuse Case defined',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(armid.RISK_BUTTONCOMMIT_ID)

  def parameters(self): 
    parameters = RiskParameters(self.theRiskName,self.theThreatName,self.theVulnerabilityName,self.theMisuseCase)
    parameters.setId(self.theRiskId)
    return parameters
