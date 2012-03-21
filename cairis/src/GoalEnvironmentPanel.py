#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/GoalEnvironmentPanel.py $ $Id: GoalEnvironmentPanel.py 509 2011-10-30 14:27:19Z shaf $
import wx
import armid
from GoalEnvironmentProperties import GoalEnvironmentProperties
from GoalEnvironmentNotebook import GoalEnvironmentNotebook
from EnvironmentListCtrl import EnvironmentListCtrl

class GoalEnvironmentPanel(wx.Panel):
  def __init__(self,parent,dp):
    wx.Panel.__init__(self,parent,armid.GOAL_PANELENVIRONMENT_ID)
    self.dbProxy = dp
    self.theGoalId = None
    self.theEnvironmentDictionary = {}
    self.theSelectedIdx = -1

    mainSizer = wx.BoxSizer(wx.HORIZONTAL)
    environmentBox = wx.StaticBox(self)
    environmentListSizer = wx.StaticBoxSizer(environmentBox,wx.HORIZONTAL)
    mainSizer.Add(environmentListSizer,0,wx.EXPAND)
    self.environmentList = EnvironmentListCtrl(self,armid.GOAL_LISTENVIRONMENTS_ID,self.dbProxy)
    environmentListSizer.Add(self.environmentList,1,wx.EXPAND)
    environmentDimSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(environmentDimSizer,1,wx.EXPAND)

    nbBox = wx.StaticBox(self,-1)
    nbSizer = wx.StaticBoxSizer(nbBox,wx.VERTICAL)
    environmentDimSizer.Add(nbSizer,1,wx.EXPAND)
    self.notebook = GoalEnvironmentNotebook(self,self.dbProxy)
    nbSizer.Add(self.notebook,1,wx.EXPAND)

    self.SetSizer(mainSizer)

    self.labelCtrl = self.notebook.FindWindowById(armid.GOAL_TEXTLABEL_ID)
    self.definitionCtrl = self.notebook.FindWindowById(armid.GOAL_TEXTDEFINITION_ID)
    self.categoryCtrl = self.notebook.FindWindowById(armid.GOAL_COMBOCATEGORY_ID)
    self.priorityCtrl = self.notebook.FindWindowById(armid.GOAL_COMBOPRIORITY_ID)
    self.fitCriterionCtrl = self.notebook.FindWindowById(armid.GOAL_TEXTFITCRITERION_ID)
    self.issueCtrl = self.notebook.FindWindowById(armid.GOAL_TEXTISSUE_ID)
    self.goalAssociationCtrl = self.notebook.FindWindowById(armid.GOAL_LISTGOALREFINEMENTS_ID)
    self.subGoalAssociationCtrl = self.notebook.FindWindowById(armid.GOAL_LISTSUBGOALREFINEMENTS_ID)
    self.cCtrl = self.notebook.FindWindowById(armid.GOAL_LISTCONCERNS_ID)
    self.caCtrl = self.notebook.FindWindowById(armid.GOAL_LISTCONCERNASSOCIATIONS_ID)

    self.environmentList.Bind(wx.EVT_LIST_INSERT_ITEM,self.OnAddEnvironment)
    self.environmentList.Bind(wx.EVT_LIST_DELETE_ITEM,self.OnDeleteEnvironment)

    self.definitionCtrl.Disable()
    self.categoryCtrl.Disable()
    self.priorityCtrl.Disable()
    self.fitCriterionCtrl.Disable()
    self.issueCtrl.Disable()
    self.goalAssociationCtrl.Disable()
    self.subGoalAssociationCtrl.Disable()
    self.cCtrl.Disable()
    self.caCtrl.Disable()


  def loadControls(self,goal):
    self.environmentList.Unbind(wx.EVT_LIST_ITEM_SELECTED)
    self.environmentList.Unbind(wx.EVT_LIST_ITEM_DESELECTED)
    self.theGoalId = goal.id()
    environmentNames = []
    for cp in goal.environmentProperties():
      environmentNames.append(cp.name())
    self.environmentList.load(environmentNames)

    for cp in goal.environmentProperties():
      environmentName = cp.name()
      self.theEnvironmentDictionary[environmentName] = cp
      environmentNames.append(environmentName) 
    environmentName = environmentNames[0]
    p = self.theEnvironmentDictionary[environmentName]

    self.labelCtrl.SetValue(p.label())
    self.definitionCtrl.SetValue(p.definition())
    self.categoryCtrl.SetValue(p.category())
    self.priorityCtrl.SetValue(p.priority())
    self.fitCriterionCtrl.SetValue(p.fitCriterion())
    self.issueCtrl.SetValue(p.issue())
    self.goalAssociationCtrl.setEnvironment(environmentName)
    self.goalAssociationCtrl.load(p.goalRefinements())
    self.subGoalAssociationCtrl.setEnvironment(environmentName)
    self.subGoalAssociationCtrl.load(p.subGoalRefinements())
    self.cCtrl.setEnvironment(environmentName)
    self.cCtrl.load(p.concerns())
    self.caCtrl.setEnvironment(environmentName)
    self.caCtrl.load(p.concernAssociations())

    self.environmentList.Select(0)
    self.environmentList.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnEnvironmentSelected)
    self.environmentList.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnEnvironmentDeselected)

    self.definitionCtrl.Enable()
    self.categoryCtrl.Enable()
    self.priorityCtrl.Enable()
    self.fitCriterionCtrl.Enable()
    self.issueCtrl.Enable()
    self.goalAssociationCtrl.Enable()
    self.subGoalAssociationCtrl.Enable()
    self.cCtrl.Enable()
    self.caCtrl.Enable()
    self.theSelectedIdx = 0


  def OnEnvironmentSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    p = self.theEnvironmentDictionary[environmentName]

    self.labelCtrl.SetValue(p.label())
    self.definitionCtrl.SetValue(p.definition())
    self.categoryCtrl.SetValue(p.category())
    self.priorityCtrl.SetValue(p.priority())
    self.fitCriterionCtrl.SetValue(p.fitCriterion())
    self.issueCtrl.SetValue(p.issue())
    self.goalAssociationCtrl.setEnvironment(environmentName)
    self.goalAssociationCtrl.load(p.goalRefinements())
    self.subGoalAssociationCtrl.setEnvironment(environmentName)
    self.subGoalAssociationCtrl.load(p.subGoalRefinements())
    self.cCtrl.setEnvironment(environmentName)
    self.cCtrl.load(p.concerns())
    self.caCtrl.setEnvironment(environmentName)
    self.caCtrl.load(p.concernAssociations())
    self.definitionCtrl.Enable()
    self.categoryCtrl.Enable()
    self.priorityCtrl.Enable()
    self.fitCriterionCtrl.Enable()
    self.issueCtrl.Enable()
    self.goalAssociationCtrl.Enable()
    self.subGoalAssociationCtrl.Enable()
    self.cCtrl.Enable()
    self.caCtrl.Enable()

  def OnEnvironmentDeselected(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    self.theEnvironmentDictionary[environmentName] = GoalEnvironmentProperties(environmentName,self.labelCtrl.GetValue(),self.definitionCtrl.GetValue(),self.categoryCtrl.GetValue(),self.priorityCtrl.GetValue(),self.fitCriterionCtrl.GetValue(),self.issueCtrl.GetValue(),self.goalAssociationCtrl.dimensions(),self.subGoalAssociationCtrl.dimensions(),self.cCtrl.dimensions(),self.caCtrl.dimensions())
    self.labelCtrl.SetValue('')
    self.definitionCtrl.SetValue('')
    self.categoryCtrl.SetValue('')
    self.priorityCtrl.SetValue('')
    self.fitCriterionCtrl.SetValue('')
    self.issueCtrl.SetValue('')
    self.goalAssociationCtrl.DeleteAllItems()
    self.goalAssociationCtrl.setEnvironment('')
    self.subGoalAssociationCtrl.DeleteAllItems()
    self.subGoalAssociationCtrl.setEnvironment('')
    self.cCtrl.DeleteAllItems()
    self.caCtrl.DeleteAllItems()
    self.cCtrl.setEnvironment('')
    self.caCtrl.setEnvironment('')
    self.theSelectedIdx = -1
    self.definitionCtrl.Disable()
    self.categoryCtrl.Disable()
    self.priorityCtrl.Disable()
    self.fitCriterionCtrl.Disable()
    self.issueCtrl.Disable()
    self.goalAssociationCtrl.Disable()
    self.subGoalAssociationCtrl.Disable()
    self.cCtrl.Disable()
    self.caCtrl.Disable()

  def OnAddEnvironment(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    self.theEnvironmentDictionary[environmentName] = GoalEnvironmentProperties(environmentName)
    self.environmentList.Select(self.theSelectedIdx)
    self.labelCtrl.SetValue('')
    self.definitionCtrl.SetValue('None')
    self.categoryCtrl.SetValue('')
    self.priorityCtrl.SetValue('')
    self.fitCriterionCtrl.SetValue('None')
    self.issueCtrl.SetValue('None')
    self.goalAssociationCtrl.setEnvironment(environmentName)
    self.goalAssociationCtrl.DeleteAllItems()
    self.subGoalAssociationCtrl.setEnvironment(environmentName)
    self.subGoalAssociationCtrl.DeleteAllItems()
    self.cCtrl.setEnvironment(environmentName)
    self.cCtrl.DeleteAllItems()
    self.caCtrl.setEnvironment(environmentName)
    self.caCtrl.DeleteAllItems()
    self.definitionCtrl.Enable()
    self.categoryCtrl.Enable()
    self.priorityCtrl.Enable()
    self.fitCriterionCtrl.Enable()
    self.issueCtrl.Enable()
    self.goalAssociationCtrl.Enable()
    self.subGoalAssociationCtrl.Enable()
    self.cCtrl.Enable()
    self.caCtrl.Enable()
    inheritedEnv = self.environmentList.inheritedEnvironment()
    if (inheritedEnv != '' and self.theGoalId != None):
      p = self.dbProxy.inheritedGoalProperties(self.theGoalId,inheritedEnv)
      self.theEnvironmentDictionary[environmentName] = p
      self.labelCtrl.SetValue(p.label())
      self.definitionCtrl.SetValue(p.definition())
      self.categoryCtrl.SetValue(p.category())
      self.priorityCtrl.SetValue(p.priority())
      self.fitCriterionCtrl.SetValue(p.fitCriterion())
      self.issueCtrl.SetValue(p.issue())
      self.goalAssociationCtrl.setEnvironment(environmentName)
      self.goalAssociationCtrl.load(p.goalRefinements())
      self.subGoalAssociationCtrl.setEnvironment(environmentName)
      self.subGoalAssociationCtrl.load(p.subGoalRefinements())
      self.cCtrl.setEnvironment(environmentName)
      self.caCtrl.setEnvironment(environmentName)
      self.cCtrl.load(p.concerns())
      self.caCtrl.load(p.concernAssociations())


  def OnDeleteEnvironment(self,evt):
    selectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(selectedIdx)
    del self.theEnvironmentDictionary[environmentName]
    self.theSelectedIdx = -1
    self.labelCtrl.SetValue('')
    self.definitionCtrl.SetValue('')
    self.categoryCtrl.SetValue('')
    self.priorityCtrl.SetValue('')
    self.fitCriterionCtrl.SetValue('')
    self.issueCtrl.SetValue('')
    self.goalAssociationCtrl.DeleteAllItems()
    self.goalAssociationCtrl.setEnvironment('')
    self.subGoalAssociationCtrl.DeleteAllItems()
    self.subGoalAssociationCtrl.setEnvironment('')
    self.cCtrl.DeleteAllItems()
    self.cCtrl.setEnvironment('')
    self.caCtrl.DeleteAllItems()
    self.caCtrl.setEnvironment('')
    self.definitionCtrl.Disable()
    self.categoryCtrl.Disable()
    self.priorityCtrl.Disable()
    self.fitCriterionCtrl.Disable()
    self.issueCtrl.Disable()
    self.goalAssociationCtrl.Disable()
    self.subGoalAssociationCtrl.Disable()
    self.cCtrl.Disable()
    self.caCtrl.Disable()



  def environmentProperties(self):
    if (self.theSelectedIdx != -1):
      environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
      self.theEnvironmentDictionary[environmentName] = GoalEnvironmentProperties(environmentName,self.labelCtrl.GetValue(),self.definitionCtrl.GetValue(),self.categoryCtrl.GetValue(),self.priorityCtrl.GetValue(),self.fitCriterionCtrl.GetValue(),self.issueCtrl.GetValue(),self.goalAssociationCtrl.dimensions(),self.subGoalAssociationCtrl.dimensions(),self.cCtrl.dimensions(),self.caCtrl.dimensions())
    return self.theEnvironmentDictionary.values() 
