#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/SingleGoalPanel.py $ $Id: SingleGoalPanel.py 408 2011-01-13 10:20:46Z shaf $
import wx
import armid
import WidgetFactory
import Goal
from Borg import Borg
from GoalEnvironmentNotebook import GoalEnvironmentNotebook

class SingleGoalPanel(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,armid.GOAL_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Name',(87,30),armid.GOAL_TEXTNAME_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Originator',(87,30),armid.GOAL_TEXTORIGINATOR_ID),0,wx.EXPAND)
    self.nameCtrl = self.FindWindowById(armid.GOAL_TEXTNAME_ID)
    self.notebook = GoalEnvironmentNotebook(self,self.dbProxy,True)

    mainSizer.Add(self.notebook,1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildCommitButtonSizer(self,armid.GOAL_BUTTONCOMMIT_ID,True),0,wx.CENTER)
    self.definitionCtrl = self.notebook.FindWindowById(armid.GOAL_TEXTDEFINITION_ID)
    self.categoryCtrl = self.notebook.FindWindowById(armid.GOAL_COMBOCATEGORY_ID)
    self.priorityCtrl = self.notebook.FindWindowById(armid.GOAL_COMBOPRIORITY_ID)
    self.fitCriterionCtrl = self.notebook.FindWindowById(armid.GOAL_TEXTFITCRITERION_ID)
    self.issueCtrl = self.notebook.FindWindowById(armid.GOAL_TEXTISSUE_ID)
    self.goalAssociationCtrl = self.notebook.FindWindowById(armid.GOAL_LISTGOALREFINEMENTS_ID)
    self.subGoalAssociationCtrl = self.notebook.FindWindowById(armid.GOAL_LISTSUBGOALREFINEMENTS_ID)
    self.cCtrl = self.notebook.FindWindowById(armid.GOAL_LISTCONCERNS_ID)
    self.caCtrl = self.notebook.FindWindowById(armid.GOAL_LISTCONCERNASSOCIATIONS_ID)
    self.ctCtrl = self.notebook.FindWindowById(armid.GOAL_COMBOCONTRIBUTIONTYPE_ID)
    self.SetSizer(mainSizer)
