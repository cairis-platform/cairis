#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ObstaclePanel.py $ $Id: ObstaclePanel.py 499 2011-10-27 15:43:45Z shaf $
import wx
import armid
import WidgetFactory
import Goal
from Borg import Borg
from ObstacleEnvironmentPanel import ObstacleEnvironmentPanel

class ObstaclePanel(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,armid.OBSTACLE_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    
  def buildControls(self,isCreate,isUpdateable=True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Name',(87,30),armid.OBSTACLE_TEXTNAME_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Originator',(87,30),armid.OBSTACLE_TEXTORIGINATOR_ID),0,wx.EXPAND)
    self.environmentPanel = ObstacleEnvironmentPanel(self,self.dbProxy)
    mainSizer.Add(self.environmentPanel,1,wx.EXPAND)
    if (isUpdateable):
      mainSizer.Add(WidgetFactory.buildCommitButtonSizer(self,armid.OBSTACLE_BUTTONCOMMIT_ID,isCreate),0,wx.CENTER)
    self.SetSizer(mainSizer)

  def loadControls(self,obstacle,isReadOnly=False):
    self.theObstacleId = obstacle.id()
    self.theObstacleOriginator = obstacle.originator()
    nameCtrl = self.FindWindowById(armid.OBSTACLE_TEXTNAME_ID)
    origCtrl = self.FindWindowById(armid.OBSTACLE_TEXTORIGINATOR_ID)
    environmentCtrl = self.FindWindowById(armid.OBSTACLE_PANELENVIRONMENT_ID)
    nameCtrl.SetValue(obstacle.name())
    origCtrl.SetValue(obstacle.originator())
    environmentCtrl.loadControls(obstacle)
