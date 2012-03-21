#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/GoalPanel.py $ $Id: GoalPanel.py 406 2011-01-13 00:25:07Z shaf $
import wx
import armid
import WidgetFactory
import Goal
from Borg import Borg
from GoalEnvironmentPanel import GoalEnvironmentPanel

class GoalPanel(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,armid.GOAL_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
   
  def buildControls(self,isCreate,isUpdateable=True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Name',(87,30),armid.GOAL_TEXTNAME_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Originator',(87,30),armid.GOAL_TEXTORIGINATOR_ID),0,wx.EXPAND)
    self.environmentPanel = GoalEnvironmentPanel(self,self.dbProxy)
    mainSizer.Add(self.environmentPanel,1,wx.EXPAND)
    if (isUpdateable):
      mainSizer.Add(WidgetFactory.buildCommitButtonSizer(self,armid.GOAL_BUTTONCOMMIT_ID,isCreate),0,wx.CENTER)
    self.SetSizer(mainSizer)

  def loadControls(self,goal,isReadOnly=False):
    self.theGoalId = goal.id()
    nameCtrl = self.FindWindowById(armid.GOAL_TEXTNAME_ID)
    origCtrl = self.FindWindowById(armid.GOAL_TEXTORIGINATOR_ID)
    environmentCtrl = self.FindWindowById(armid.GOAL_PANELENVIRONMENT_ID)
    nameCtrl.SetValue(goal.name())
    origCtrl.SetValue(goal.originator())
    environmentCtrl.loadControls(goal)
