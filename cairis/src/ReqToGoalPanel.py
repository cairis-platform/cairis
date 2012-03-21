#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ReqToGoalPanel.py $ $Id: ReqToGoalPanel.py 564 2012-03-12 17:53:00Z shaf $
import wx
import armid
from BasePanel import BasePanel
import Goal
from Borg import Borg
from ReqToGoalEnvironmentPanel import ReqToGoalEnvironmentPanel

class ReqToGoalPanel(BasePanel):
  def __init__(self,parent,goalName,goalDef,goalCat,goalPri,goalFc,goalIssue,goalOrig,goalAssets,envName):
    BasePanel.__init__(self,parent,armid.GOAL_ID)
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(self.buildTextSizer('Name',(87,30),armid.GOAL_TEXTNAME_ID),0,wx.EXPAND)
    mainSizer.Add(self.buildTextSizer('Originator',(87,30),armid.GOAL_TEXTORIGINATOR_ID),0,wx.EXPAND)
    self.environmentPanel = ReqToGoalEnvironmentPanel(self,goalDef,goalCat,goalPri,goalFc,goalIssue,goalAssets,envName)
    mainSizer.Add(self.environmentPanel,1,wx.EXPAND)
    mainSizer.Add(self.buildCommitButtonSizer(armid.GOAL_BUTTONCOMMIT_ID,True),0,wx.CENTER)
    origCtrl = self.FindWindowById(armid.GOAL_TEXTORIGINATOR_ID)
    origCtrl.SetValue(goalOrig)
    self.SetSizer(mainSizer)
