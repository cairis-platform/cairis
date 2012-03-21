#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/GoalDialog.py $ $Id: GoalDialog.py 406 2011-01-13 00:25:07Z shaf $
import wx
import armid
import ARM
from Borg import Borg
from GoalPanel import GoalPanel
from GoalParameters import GoalParameters
import DialogClassParameters

class GoalDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,parameters.id(),parameters.label(),style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(600,400))
    self.theGoalId = -1
    self.theGoalName = ''
    self.theGoalOriginator = ''
    self.theEnvironmentProperties = []
    self.panel = 0
    self.buildControls(parameters)
    self.commitVerb = 'Add'
    
  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = GoalPanel(self)
    self.panel.buildControls(parameters.createFlag())
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.GOAL_BUTTONCOMMIT_ID,self.onCommit)

  def load(self,goal):
    self.theGoalId = goal.id()
    self.panel.loadControls(goal)
    self.commitVerb = 'Edit'

  def onCommit(self,evt):
    nameCtrl = self.FindWindowById(armid.GOAL_TEXTNAME_ID)
    origCtrl = self.FindWindowById(armid.GOAL_TEXTORIGINATOR_ID)
    environmentCtrl = self.FindWindowById(armid.GOAL_PANELENVIRONMENT_ID)

    self.theGoalName = nameCtrl.GetValue()
    self.theGoalOriginator = origCtrl.GetValue()

    if (self.commitVerb == 'Add'):
      b = Borg()
      try:
        b.dbProxy.nameCheck(self.theGoalName,'goal')
      except ARM.ARMException,errorText:
        dlg = wx.MessageDialog(self,str(errorText),'Add goal',wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
        return
    self.theEnvironmentProperties = environmentCtrl.environmentProperties()

    commitLabel = self.commitVerb + ' goal'
    if len(self.theGoalName) == 0:
      dlg = wx.MessageDialog(self,'Goal name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theGoalOriginator) == 0:
      dlg = wx.MessageDialog(self,'Goal originator cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theEnvironmentProperties) == 0):
      dlg = wx.MessageDialog(self,'No environments have been associated with this goal',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      for environmentProperties in self.theEnvironmentProperties:
        if len(environmentProperties.definition()) == 0:
          errorTxt = 'No definition associated with environment ' + environmentProperties.name()
          dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK)
          dlg.ShowModal()
          dlg.Destroy()
          return
        if len(environmentProperties.category()) == 0:
          errorTxt = 'No category associated with environment ' + environmentProperties.name()
          dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK)
          dlg.ShowModal()
          dlg.Destroy()
          return
        if len(environmentProperties.priority()) == 0:
          errorTxt = 'No priority associated with environment ' + environmentProperties.name()
          dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK)
          dlg.ShowModal()
          dlg.Destroy()
          return
        if len(environmentProperties.fitCriterion()) == 0:
          errorTxt = 'No fit criterion associated with environment ' + environmentProperties.name()
          dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK)
          dlg.ShowModal()
          dlg.Destroy()
          return
        if len(environmentProperties.issue()) == 0:
          errorTxt = 'No issues associated with environment ' + environmentProperties.name()
          dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK)
          dlg.ShowModal()
          dlg.Destroy()
          return
      self.EndModal(armid.GOAL_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = GoalParameters(self.theGoalName,self.theGoalOriginator,self.theEnvironmentProperties)
    parameters.setId(self.theGoalId)
    return parameters
