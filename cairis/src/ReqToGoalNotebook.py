#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ReqToGoalNotebook.py $ $Id: ReqToGoalNotebook.py 303 2010-07-18 16:17:17Z shaf $
import wx
import armid
from GoalPage import GoalPage

class ReqToGoalNotebook(wx.Notebook):
  def __init__(self,parent,dp):
    wx.Notebook.__init__(self,parent,armid.GOAL_NOTEBOOKENVIRONMENT_ID)
    p1 = GoalPage(self,armid.GOAL_LISTGOALREFINEMENTS_ID,True,dp)
    p2 = GoalPage(self,armid.GOAL_LISTSUBGOALREFINEMENTS_ID,False,dp)
    self.AddPage(p1,'Goals')
    self.AddPage(p2,'Sub-Goals')
