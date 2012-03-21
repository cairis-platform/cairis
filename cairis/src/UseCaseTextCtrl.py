import wx
import armid
from ARM import *
from Borg import Borg
from SingleGoalDialog import SingleGoalDialog
from GoalAssociationParameters import GoalAssociationParameters
from SingleRequirementDialog import SingleRequirementDialog
import RequirementFactory


class UseCaseTextCtrl(wx.TextCtrl):
  def __init__(self,parent,winId):
    wx.TextCtrl.__init__(self,parent,winId,'',style=wx.TE_MULTILINE)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theUseCaseName = ''
    self.theEnvironmentName = ''

    self.theDimMenu = wx.Menu()
    self.theDimMenu.Append(armid.UCTCTRL_MENUGOAL_ID,'Refining Goal')
    self.theDimMenu.Append(armid.UCTCTRL_MENUREQUIREMENT_ID,'Refining Requirement')
    self.Bind(wx.EVT_RIGHT_DOWN,self.OnRightDown)
    wx.EVT_MENU(self.theDimMenu,armid.UCTCTRL_MENUGOAL_ID,self.onGoal)
    wx.EVT_MENU(self.theDimMenu,armid.UCTCTRL_MENUREQUIREMENT_ID,self.onRequirement)
    self.goalItem = self.theDimMenu.FindItemById(armid.UCTCTRL_MENUGOAL_ID)
    self.goalItem.Enable(False)
    self.reqItem = self.theDimMenu.FindItemById(armid.UCTCTRL_MENUREQUIREMENT_ID)
    self.reqItem.Enable(False)

  def setUseCase(self,ucName):
    self.theUseCaseName = ucName
    if (self.theUseCaseName != ''):
      self.goalItem.Enable()
      self.reqItem.Enable()
    else:
      self.goalItem.Enable(False)
      self.reqItem.Enable(False)

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
        gap = GoalAssociationParameters(self.theEnvironmentName,gp.name(),'goal','and',self.theUseCaseName,'usecase',0,'')
        self.dbProxy.addGoalAssociation(gap)
        ackDlg = wx.MessageDialog(self,'Added goal ' + gp.name(),'Refining goal',wx.OK)
        ackDlg.ShowModal()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Refining goal',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()

  def onRequirement(self,evt):
    try:
      ucId = self.dbProxy.getDimensionId(self.theUseCaseName,'usecase')
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
        self.dbProxy.addTrace('requirement_usecase',reqId,ucId,dlg.theContributionType)
        completeReqLabel = self.dbProxy.lastRequirementLabel(refName)
        ackDlg = wx.MessageDialog(self,'Added requirement ' + completeReqLabel,'Refining requirement',wx.OK)
        ackDlg.ShowModal()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Refining requirement',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
