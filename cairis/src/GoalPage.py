#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/GoalPage.py $ $Id: GoalPage.py 329 2010-10-31 14:59:16Z shaf $

import wx
from GoalAssociationListCtrl import GoalAssociationListCtrl

class GoalPage(wx.Panel):
  def __init__(self,parent,winId,isGoal,dp):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    sgBox = wx.StaticBox(self,-1)
    sgBoxSizer = wx.StaticBoxSizer(sgBox,wx.HORIZONTAL)
    topSizer.Add(sgBoxSizer,1,wx.EXPAND)
    self.subGoalList = GoalAssociationListCtrl(self,winId,dp,isGoal)
    sgBoxSizer.Add(self.subGoalList,1,wx.EXPAND)
    self.SetSizer(topSizer)
