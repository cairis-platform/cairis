#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/MisuseCasePanel.py $ $Id: MisuseCasePanel.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
import WidgetFactory
from MisuseCaseEnvironmentPanel import MisuseCaseEnvironmentPanel

class MisuseCasePanel(wx.Panel):
  def __init__(self,parent,dp):
    wx.Panel.__init__(self,parent,armid.MISUSECASE_ID)
    self.dbProxy = dp
 
  def buildControls(self,isCreate = True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Name',(87,30),armid.MISUSECASE_TEXTNAME_ID,isReadOnly=True),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Risk',(87,30),armid.MISUSECASE_TEXTRISK_ID,isReadOnly=True),0,wx.EXPAND)
    thrSizer = wx.BoxSizer(wx.HORIZONTAL)

    self.environmentPanel = MisuseCaseEnvironmentPanel(self,self.dbProxy)
    mainSizer.Add(self.environmentPanel,1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildCommitButtonSizer(self,armid.MISUSECASE_BUTTONCOMMIT_ID,isCreate),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

    self.nameCtrl = self.FindWindowById(armid.MISUSECASE_TEXTNAME_ID)
    self.riskCtrl = self.FindWindowById(armid.MISUSECASE_TEXTRISK_ID)

  def loadMisuseCase(self,mc):
    self.nameCtrl.SetValue(mc.name())
    self.riskCtrl.SetValue(mc.risk())
    self.environmentPanel.loadMisuseCase(mc)

  def loadRiskComponents(self,riskName,threatName,vulName):
    mcName = 'Exploit ' + riskName
    self.nameCtrl.SetValue(mcName)
    self.riskCtrl.SetValue(riskName)
    self.environmentPanel.loadRiskComponents(threatName,vulName)
