#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/EnvironmentDialog.py $ $Id: EnvironmentDialog.py 523 2011-11-04 18:07:01Z shaf $
import wx
import armid
from EnvironmentPanel import EnvironmentPanel
from EnvironmentParameters import EnvironmentParameters

class EnvironmentDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,parameters.id(),parameters.label(),style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(750,400))
    self.theEnvironmentId = -1
    self.environmentName = ''
    self.environmentShortCode = ''
    self.environmentDescription = ''
    self.theEnvironments = []
    self.theDuplicateProperty = ''
    self.theOverridingEnvironment = ''
    self.theTensions = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    self.buildControls(parameters)
    self.theCommitVerb = 'Create'

  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = EnvironmentPanel(self)
    self.panel.buildControls(parameters.createFlag())
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.ENVIRONMENT_BUTTONCOMMIT_ID,self.onCommit)

  def load(self,environment):
    self.theEnvironmentId = environment.id()
    self.panel.loadControls(environment)
    self.theCommitVerb = 'Edit'

  def onCommit(self,evt):
    nameCtrl = self.FindWindowById(armid.ENVIRONMENT_TEXTNAME_ID)
    shortCodeCtrl = self.FindWindowById(armid.ENVIRONMENT_TEXTSHORTCODE_ID)
    valueCtrl = self.FindWindowById(armid.ENVIRONMENT_TEXTDESCRIPTION_ID)
    environmentCtrl = self.FindWindowById(armid.ENVIRONMENT_PANELENVIRONMENTPROPERTIES_ID)
    tensionsCtrl = self.FindWindowById(armid.ENVIRONMENT_GRIDVALUETENSIONS_ID)

    self.environmentName = nameCtrl.GetValue()
    self.environmentShortCode = shortCodeCtrl.GetValue()
    self.environmentDescription = valueCtrl.GetValue()
    self.theEnvironments = environmentCtrl.environments()
    self.theTensions = tensionsCtrl.tensions()
    commitLabel = self.theCommitVerb + ' environment'

    if len(self.environmentName) == 0:
      dlg = wx.MessageDialog(self,'Environment name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.environmentShortCode) == 0):
      dlg = wx.MessageDialog(self,'Environment short code cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.environmentDescription) == 0):
      dlg = wx.MessageDialog(self,'Environment description cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theEnvironments) > 0):
      self.theDuplicateProperty = environmentCtrl.duplicateProperty()
      self.theOverridingEnvironment = environmentCtrl.overridingEnvironment()
      if (self.theDuplicateProperty == 'Override') and (len(self.theOverridingEnvironment) == 0):
        dlg = wx.MessageDialog(self,'An overriding environment has not been selected',commitLabel,wx.OK) 
        dlg.ShowModal()
        dlg.Destroy()
        return 
    
    self.EndModal(armid.ENVIRONMENT_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = EnvironmentParameters(self.environmentName,self.environmentShortCode,self.environmentDescription,self.theEnvironments,self.theDuplicateProperty,self.theOverridingEnvironment,self.theTensions)
    parameters.setId(self.theEnvironmentId)
    return parameters

