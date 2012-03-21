#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/RolePanel.py $ $Id: RolePanel.py 395 2011-01-06 01:17:45Z shaf $
import wx
import armid
import WidgetFactory
from Borg import Borg
from RoleEnvironmentPanel import RoleEnvironmentPanel

class RolePanel(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,armid.ROLE_ID)
    b = Borg()
    self.dbProxy = b.dbProxy

  def buildControls(self,isCreate):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Name',(87,30),armid.ROLE_TEXTNAME_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Short Code',(87,30),armid.ROLE_TEXTSHORTCODE_ID),0,wx.EXPAND)
    roleTypes = self.dbProxy.getDimensionNames('role_type')
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Type',(87,30),armid.ROLE_COMBOTYPE_ID,roleTypes),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildMLTextSizer(self,'Description',(87,80),armid.ROLE_TEXTDESCRIPTION_ID),0,wx.EXPAND)
    mainSizer.Add(RoleEnvironmentPanel(self,self.dbProxy),1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildCommitButtonSizer(self,armid.ROLE_BUTTONCOMMIT_ID,isCreate),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

  def loadControls(self,role):
    nameCtrl = self.FindWindowById(armid.ROLE_TEXTNAME_ID)
    scCtrl = self.FindWindowById(armid.ROLE_TEXTSHORTCODE_ID)
    typeCtrl = self.FindWindowById(armid.ROLE_COMBOTYPE_ID)
    descCtrl = self.FindWindowById(armid.ROLE_TEXTDESCRIPTION_ID)
    environmentCtrl = self.FindWindowById(armid.ROLE_PANELENVIRONMENT_ID)
    nameCtrl.SetValue(role.name())
    scCtrl.SetValue(role.shortCode())
    typeCtrl.SetValue(role.type())
    descCtrl.SetValue(role.description())
    environmentCtrl.loadControls(role)
