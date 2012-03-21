#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/EnvironmentPanel.py $ $Id: EnvironmentPanel.py 529 2011-11-16 16:56:25Z shaf $
import wx
import armid
from BasePanel import BasePanel
from Borg import Borg
from EnvironmentNotebook import EnvironmentNotebook

class EnvironmentPanel(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,armid.ENVIRONMENT_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.environmentName = ''
    self.environmentDescription = ''

  def buildControls(self,isCreate,isUpdateable=True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(self.buildTextSizer('Name',(87,30),armid.ENVIRONMENT_TEXTNAME_ID),0,wx.EXPAND)
    self.envNotebook = EnvironmentNotebook(self,self.dbProxy)
    mainSizer.Add(self.envNotebook,1,wx.EXPAND)
    mainSizer.Add(self.buildCommitButtonSizer(armid.ENVIRONMENT_BUTTONCOMMIT_ID,isCreate),0,wx.CENTER)
    self.SetSizer(mainSizer)


  def loadControls(self,environment):
    nameCtrl = self.FindWindowById(armid.ENVIRONMENT_TEXTNAME_ID)
    shortCodeCtrl = self.envNotebook.FindWindowById(armid.ENVIRONMENT_TEXTSHORTCODE_ID)
    valueCtrl = self.envNotebook.FindWindowById(armid.ENVIRONMENT_TEXTDESCRIPTION_ID)
    environmentCtrl = self.envNotebook.FindWindowById(armid.ENVIRONMENT_PANELENVIRONMENTPROPERTIES_ID)
    tensionCtrl = self.envNotebook.FindWindowById(armid.ENVIRONMENT_GRIDVALUETENSIONS_ID)
    nameCtrl.SetValue(environment.name())
    shortCodeCtrl.SetValue(environment.shortCode())
    valueCtrl.SetValue(environment.description())
    environmentCtrl.load(environment)
    tensionCtrl.setTable(environment.tensions())
