#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/SingleEnvironmentPanel.py $ $Id: SingleEnvironmentPanel.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
import WidgetFactory
from Borg import Borg

class SingleEnvironmentPanel(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,armid.ENVIRONMENT_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.environmentName = ''
    self.environmentDescription = ''

  def buildControls(self):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Name',(87,30),armid.ENVIRONMENT_TEXTNAME_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Short Code',(87,30),armid.ENVIRONMENT_TEXTSHORTCODE_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildMLTextSizer(self,'Description',(87,30),armid.ENVIRONMENT_TEXTDESCRIPTION_ID),1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildCommitButtonSizer(self,armid.ENVIRONMENT_BUTTONCOMMIT_ID,True))
    self.SetSizer(mainSizer)


  def loadControls(self,environment,isReadOnly=False):
    nameCtrl = self.FindWindowById(armid.ENVIRONMENT_TEXTNAME_ID)
    shortCode = self.FindWindowById(armid.ENVIRONMENT_TEXTSHORTCODE_ID)
    valueCtrl = self.FindWindowById(armid.ENVIRONMENT_TEXTDESCRIPTION_ID)
    nameCtrl.SetValue(environment.name())
    shortCodeCtrl.SetValue(environment.shortCode())
    valueCtrl.SetValue(environment.description())
