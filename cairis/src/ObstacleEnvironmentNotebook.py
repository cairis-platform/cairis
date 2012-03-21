#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ObstacleEnvironmentNotebook.py $ $Id: ObstacleEnvironmentNotebook.py 509 2011-10-30 14:27:19Z shaf $
import wx
import armid
from DimensionListCtrl import DimensionListCtrl
from GoalAssociationListCtrl import GoalAssociationListCtrl

class SummaryPage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    topRowSizer = wx.BoxSizer(wx.HORIZONTAL)
    topSizer.Add(topRowSizer,0,wx.EXPAND)

    lblBox = wx.StaticBox(self,-1,'Label')
    lblBoxSizer = wx.StaticBoxSizer(lblBox,wx.VERTICAL)
    topRowSizer.Add(lblBoxSizer,0,wx.EXPAND)
    self.labelCtrl = wx.TextCtrl(self,armid.OBSTACLE_TEXTLABEL_ID,"",pos=wx.DefaultPosition,size=wx.Size(150,30),style=wx.TE_READONLY)
    self.labelCtrl.Disable()
    lblBoxSizer.Add(self.labelCtrl,1,wx.EXPAND)

    
    catBox = wx.StaticBox(self,-1,'Category')
    catBoxSizer = wx.StaticBoxSizer(catBox,wx.VERTICAL)
    topRowSizer.Add(catBoxSizer,0,wx.EXPAND)
    catList = ['Confidentiality Threat','Integrity Threat','Availability Threat','Accountability Threat','Anonymity Threat','Pseudonymity Threat','Unlinkability Threat','Unobservability Threat','Vulnerability','Duration','Frequency','Demands','Goal Support']
    self.categoryCtrl = wx.ComboBox(self,armid.OBSTACLE_COMBOCATEGORY_ID,choices=catList,size=wx.DefaultSize,style= wx.CB_READONLY)
    catBoxSizer.Add(self.categoryCtrl,1,wx.EXPAND)

    defBox = wx.StaticBox(self,-1,'Definition')
    defBoxSizer = wx.StaticBoxSizer(defBox,wx.VERTICAL)
    topSizer.Add(defBoxSizer,1,wx.EXPAND)
    self.definitionCtrl = wx.TextCtrl(self,armid.OBSTACLE_TEXTDEFINITION_ID,'',style= wx.TE_MULTILINE)
    defBoxSizer.Add(self.definitionCtrl,1,wx.EXPAND)

    self.SetSizer(topSizer)

class GoalPage(wx.Panel):
  def __init__(self,parent,winId,isGoal,dp):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    sgBox = wx.StaticBox(self,-1)
    sgBoxSizer = wx.StaticBoxSizer(sgBox,wx.HORIZONTAL)
    topSizer.Add(sgBoxSizer,1,wx.EXPAND)
    self.goalList = GoalAssociationListCtrl(self,winId,dp,isGoal)
    sgBoxSizer.Add(self.goalList,1,wx.EXPAND)
    self.SetSizer(topSizer)

class ConcernPage(wx.Panel):
  def __init__(self,parent,winId,dp):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    sgBox = wx.StaticBox(self,-1)
    sgBoxSizer = wx.StaticBoxSizer(sgBox,wx.HORIZONTAL)
    topSizer.Add(sgBoxSizer,1,wx.EXPAND)
    self.concernList = DimensionListCtrl(self,winId,wx.DefaultSize,'Concern','asset',dp)
    sgBoxSizer.Add(self.concernList,1,wx.EXPAND)
    self.SetSizer(topSizer)

class ObstacleEnvironmentNotebook(wx.Notebook):
  def __init__(self,parent,dp):
    wx.Notebook.__init__(self,parent,armid.OBSTACLE_NOTEBOOKENVIRONMENT_ID)
    p1 = SummaryPage(self)
    p2 = GoalPage(self,armid.OBSTACLE_LISTGOALS_ID,True,dp)
    p3 = GoalPage(self,armid.OBSTACLE_LISTSUBGOALS_ID,False,dp)
    p4 = ConcernPage(self,armid.OBSTACLE_LISTCONCERNS_ID,dp)
    self.AddPage(p1,'Definition')
    self.AddPage(p2,'Goals')
    self.AddPage(p3,'Sub-Goals')
    self.AddPage(p4,'Concerns')
