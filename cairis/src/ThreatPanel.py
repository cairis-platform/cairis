#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ThreatPanel.py $ $Id: ThreatPanel.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
import WidgetFactory
from Borg import Borg
from ThreatEnvironmentPanel import ThreatEnvironmentPanel

class ThreatPanel(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,armid.THREAT_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theLikelihoods = self.dbProxy.getDimensionNames('likelihood')
    

  def buildControls(self,isCreate,isUpdateable=True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Name',(87,30),armid.THREAT_TEXTNAME_ID),0,wx.EXPAND)
    threatTypes = self.dbProxy.getDimensionNames('threat_type')
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Type',(87,30),armid.THREAT_THREATTYPE_ID,threatTypes),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildMLTextSizer(self,'Method',(87,60),armid.THREAT_TEXTMETHOD_ID),0,wx.EXPAND)
    mainSizer.Add(ThreatEnvironmentPanel(self,self.dbProxy),1,wx.EXPAND)

    if (isUpdateable):
      mainSizer.Add(WidgetFactory.buildCommitButtonSizer(self,armid.THREAT_BUTTONCOMMIT_ID,isCreate),0,wx.ALIGN_CENTRE)
    self.SetSizer(mainSizer)

  def loadControls(self,threat,isReadOnly = False):
    nameCtrl = self.FindWindowById(armid.THREAT_TEXTNAME_ID)
    typeCtrl = self.FindWindowById(armid.THREAT_THREATTYPE_ID)
    methodCtrl = self.FindWindowById(armid.THREAT_TEXTMETHOD_ID)
    environmentCtrl = self.FindWindowById(armid.THREAT_PANELENVIRONMENT_ID)
    nameCtrl.SetValue(threat.name())
    typeCtrl.SetValue(threat.type())
    methodCtrl.SetValue(threat.method())
    environmentCtrl.loadControls(threat)
