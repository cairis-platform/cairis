#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ResponsePanel.py $ $Id: ResponsePanel.py 380 2010-12-27 23:33:41Z shaf $
import wx
import ARM
import armid
import WidgetFactory
from Borg import Borg
from ResponseParameters import ResponseParameters
from AcceptEnvironmentPanel import AcceptEnvironmentPanel
from TransferEnvironmentPanel import TransferEnvironmentPanel
from MitigateEnvironmentPanel import MitigateEnvironmentPanel

class ResponsePanel(wx.Panel):
  def __init__(self,parent,responseType,panel):
    wx.Panel.__init__(self,parent,armid.RESPONSE_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theResponseName = ''
    self.theRiskName = ''
    self.theCommitVerb = 'Create'
    self.environmentPanel = panel(self,self.dbProxy)
    self.theEnvironmentProperties = []
    self.theResponseVerb = responseType

  def buildControls(self,isCreate,isUpdateable = True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Name',(87,60),armid.RESPONSE_TEXTNAME_ID,isReadOnly=True),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Risk',(87,30),armid.RESPONSE_COMBORISK_ID,self.dbProxy.getDimensionNames('risk')),0,wx.EXPAND)
    mainSizer.Add(self.environmentPanel,1,wx.EXPAND)
    if (isUpdateable):
      mainSizer.Add(WidgetFactory.buildCommitButtonSizer(self,armid.RESPONSE_BUTTONCOMMIT_ID,isCreate),0,wx.ALIGN_CENTRE)
    self.SetSizer(mainSizer)
    self.nameCtrl = self.FindWindowById(armid.RESPONSE_TEXTNAME_ID)
    self.nameCtrl.Disable()
    self.riskCtrl = self.FindWindowById(armid.RESPONSE_COMBORISK_ID)
    self.riskCtrl.Bind(wx.EVT_COMBOBOX,self.onRiskChange)

  def onRiskChange(self,evt):
    riskName = self.riskCtrl.GetValue()
    if (riskName != ''):
      if (self.environmentPanel.__class__.__name__ != 'MitigateEnvironmentPanel'):
        nameLabel = self.theResponseVerb + ' ' + riskName
        self.nameCtrl.SetValue(nameLabel)
      else:
        mitTypeCombo = self.environmentPanel.FindWindowById(armid.MITIGATE_COMBOTYPE_ID)
        mitType = mitTypeCombo.GetValue()
        if (mitType != ''):
          nameLabel = 'Mitigate' + ' ' + riskName 
          self.nameCtrl.SetValue(nameLabel)
    else:
      self.nameCtrl.SetValue('')


  def loadControls(self,response,isReadOnly = False):
    self.nameCtrl.SetValue(response.name())
    self.riskCtrl.SetStringSelection(response.risk())
    self.environmentPanel.loadControls(response)
    self.theCommitVerb = 'Edit'

  def commit(self):
    self.theResponseName = self.nameCtrl.GetValue()
    commitLabel = self.theCommitVerb + ' response'
    if (self.theCommitVerb == 'Create'):
      b = Borg()
      try:
        b.dbProxy.nameCheck(self.theResponseName,'response')
      except ARM.ARMException,errorText:
        dlg = wx.MessageDialog(self,str(errorText),commitLabel,wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
        return

    self.theRiskName = self.riskCtrl.GetStringSelection()
    try:
      self.theEnvironmentProperties = self.environmentPanel.environmentProperties()
    except ARM.EnvironmentValidationError, errorText:
      dlg = wx.MessageDialog(self,str(errorText),commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return -1
    
    commitLabel = self.theCommitVerb + ' response'

    if (len(self.theResponseName) == 0):
      dlg = wx.MessageDialog(self,'No risk selected',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return -1
    elif (len(self.theRiskName) == 0):
      dlg = wx.MessageDialog(self,'No risk selected',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return -1
    elif (len(self.theEnvironmentProperties) == 0):
      dlg = wx.MessageDialog(self,'No environment specific properties set',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return -1
    else:
      return 0

  def parameters(self):
    return ResponseParameters(self.theResponseName,self.theRiskName,self.theEnvironmentProperties,self.theResponseVerb)
