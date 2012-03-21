#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/SingleGoalPanel.py $ $Id: SingleGoalPanel.py 368 2010-12-15 17:04:13Z shaf $
import wx
import armid
import WidgetFactory
import Obstacle
from Borg import Borg
from ObstacleEnvironmentNotebook import ObstacleEnvironmentNotebook

class SingleObstaclePanel(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,armid.OBSTACLE_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Name',(87,30),armid.OBSTACLE_TEXTNAME_ID),0,wx.EXPAND)
    self.nameCtrl = self.FindWindowById(armid.OBSTACLE_TEXTNAME_ID)
    self.notebook = ObstacleEnvironmentNotebook(self,self.dbProxy)

    mainSizer.Add(self.notebook,1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildCommitButtonSizer(self,armid.OBSTACLE_BUTTONCOMMIT_ID,True),0,wx.CENTER)
    self.definitionCtrl = self.notebook.FindWindowById(armid.OBSTACLE_TEXTDEFINITION_ID)
    self.categoryCtrl = self.notebook.FindWindowById(armid.OBSTACLE_COMBOCATEGORY_ID)
    self.goalAssociationCtrl = self.notebook.FindWindowById(armid.OBSTACLE_LISTGOALS_ID)
    self.subGoalAssociationCtrl = self.notebook.FindWindowById(armid.OBSTACLE_LISTSUBGOALS_ID)
    self.cCtrl = self.notebook.FindWindowById(armid.OBSTACLE_LISTCONCERNS_ID)
    self.SetSizer(mainSizer)
