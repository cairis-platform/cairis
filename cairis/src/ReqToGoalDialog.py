#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ReqToGoalDialog.py $ $Id: ReqToGoalDialog.py 564 2012-03-12 17:53:00Z shaf $
import wx
import armid
import ARM
from Borg import Borg
from ReqToGoalPanel import ReqToGoalPanel
from GoalParameters import GoalParameters

class ReqToGoalDialog(wx.Dialog):
  def __init__(self,parent,goalName,goalDef,goalCat,goalPri,goalFc,goalIssue,goalOrig,goalAssets,envName):
    wx.Dialog.__init__(self,parent,armid.GOAL_ID,'Convert Requirement to Goal',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(600,400))
    self.theGoalId = -1
    self.theGoalName = goalName
    self.theGoalOriginator = goalOrig
    self.theEnvironmentProperties = []
    self.panel = 0
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    if (goalPri == '1'):
      goalPri = 'Low'
    elif (goalPri == '2'):
      goalPri = 'Medium'
    else:
      goalPri = 'High'

    self.panel = ReqToGoalPanel(self,goalName,goalDef,goalCat,goalPri,goalFc,goalIssue,goalOrig,goalAssets,envName)
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.GOAL_BUTTONCOMMIT_ID,self.onCommit)

  def onCommit(self,evt):
    nameCtrl = self.FindWindowById(armid.GOAL_TEXTNAME_ID)
    origCtrl = self.FindWindowById(armid.GOAL_TEXTORIGINATOR_ID)
    environmentCtrl = self.FindWindowById(armid.GOAL_PANELENVIRONMENT_ID)

    self.theGoalName = nameCtrl.GetValue()
    self.theGoalOriginator = origCtrl.GetValue()

    b = Borg()
    try:
      b.dbProxy.nameCheck(self.theGoalName,'goal')
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add goal',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return
    self.theEnvironmentProperties = environmentCtrl.environmentProperties()

    commitLabel = 'Convert requirement to goal'
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
      self.EndModal(armid.GOAL_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = GoalParameters(self.theGoalName,self.theGoalOriginator,self.theEnvironmentProperties)
    parameters.setId(self.theGoalId)
    return parameters
