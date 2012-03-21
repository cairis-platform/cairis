import wx
import armid
from ARM import *
from Borg import Borg
from SingleGoalDialog import SingleGoalDialog
from SingleObstacleDialog import SingleObstacleDialog
from SingleRequirementDialog import SingleRequirementDialog
from GoalAssociationParameters import GoalAssociationParameters
import RequirementFactory


class NarrativeCtrl(wx.TextCtrl):
  def __init__(self,parent,winId):
    wx.TextCtrl.__init__(self,parent,winId,'',style=wx.TE_MULTILINE)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theTaskName = ''
    self.theEnvironmentName = ''

    self.theDimMenu = wx.Menu()
    self.theDimMenu.Append(armid.NARCTRL_MENUGOAL_ID,'Refining Goal')
    self.theDimMenu.Append(armid.NARCTRL_MENUOBSTACLE_ID,'Refining Obstacle')
    self.theDimMenu.Append(armid.NARCTRL_MENUREQUIREMENT_ID,'Refining Requirement')
    self.Bind(wx.EVT_RIGHT_DOWN,self.OnRightDown)
    wx.EVT_MENU(self.theDimMenu,armid.NARCTRL_MENUGOAL_ID,self.onGoal)
    wx.EVT_MENU(self.theDimMenu,armid.NARCTRL_MENUOBSTACLE_ID,self.onObstacle)
    wx.EVT_MENU(self.theDimMenu,armid.NARCTRL_MENUREQUIREMENT_ID,self.onRequirement)
    self.goalItem = self.theDimMenu.FindItemById(armid.NARCTRL_MENUGOAL_ID)
    self.goalItem.Enable(False)
    self.reqItem = self.theDimMenu.FindItemById(armid.NARCTRL_MENUREQUIREMENT_ID)
    self.reqItem.Enable(False)
    self.obsItem = self.theDimMenu.FindItemById(armid.NARCTRL_MENUOBSTACLE_ID)
    self.obsItem.Enable(False)

  def setTask(self,tName):
    self.theTaskName = tName
    if (self.theTaskName != ''):
      self.goalItem.Enable()
      self.reqItem.Enable()
      self.obsItem.Enable()
    else:
      self.goalItem.Enable(False)
      self.reqItem.Enable(False)
      self.obsItem.Enable(False)

  def setEnvironment(self,envName):
    self.theEnvironmentName = envName

  def OnRightDown(self,evt):
    self.PopupMenu(self.theDimMenu)

  def onGoal(self,evt):
    try:
      dlg = SingleGoalDialog(self,self.theEnvironmentName)
      if (dlg.ShowModal() == armid.GOAL_BUTTONCOMMIT_ID):
        gp = dlg.parameters()
        self.dbProxy.addGoal(gp)
        gap = GoalAssociationParameters(self.theEnvironmentName,gp.name(),'goal',dlg.theContributionType,self.theTaskName,'task',0,'')
        self.dbProxy.addGoalAssociation(gap)
        ackDlg = wx.MessageDialog(self,'Added goal ' + gp.name(),'Refining goal',wx.OK)
        ackDlg.ShowModal()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Refining goal',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()

  def onObstacle(self,evt):
    try:
      dlg = SingleObstacleDialog(self,self.theEnvironmentName)
      if (dlg.ShowModal() == armid.OBSTACLE_BUTTONCOMMIT_ID):
        op = dlg.parameters()
        self.dbProxy.addObstacle(op)
        gap = GoalAssociationParameters(self.theEnvironmentName,op.name(),'obstacle','and',self.theTaskName,'task',0,'')
        self.dbProxy.addGoalAssociation(gap)
        ackDlg = wx.MessageDialog(self,'Added obstacle ' + op.name(),'Refining goal',wx.OK)
        ackDlg.ShowModal()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Refining obstacle',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()


  def onRequirement(self,evt):
    try:
      taskId = self.dbProxy.getDimensionId(self.theTaskName,'task')
      dlg = SingleRequirementDialog(self)
      if (dlg.ShowModal() == armid.SINGLEREQUIREMENT_BUTTONCOMMIT_ID):
        refName = dlg.referrer()
        completeReqLabel = self.dbProxy.lastRequirementLabel(refName)
        referrer,reqLabel = completeReqLabel.split('-')
        reqId = self.dbProxy.newId()
        reqLabel = int(reqLabel)
        reqLabel += 1
        r = RequirementFactory.build(reqId,reqLabel,dlg.description(),dlg.priority(),dlg.rationale(),dlg.fitCriterion(),dlg.originator(),dlg.type(),refName)
        isAsset = True
        if (dlg.referrerType() == 'environment'):
          isAsset = False
        self.dbProxy.addRequirement(r,refName,isAsset)
        self.dbProxy.addTrace('requirement_task',reqId,taskId)
        completeReqLabel = self.dbProxy.lastRequirementLabel(refName)
        ackDlg = wx.MessageDialog(self,'Added requirement ' + completeReqLabel,'Refining requirement',wx.OK)
        ackDlg.ShowModal()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Refining requirement',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
