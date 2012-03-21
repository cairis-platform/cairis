#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/SecurityPatternEnvironmentDialog.py $ $Id: SecurityPatternEnvironmentDialog.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
from SecurityPatternEnvironmentPanel import SecurityPatternEnvironmentPanel

class SecurityPatternEnvironmentDialog(wx.Dialog):
  def __init__(self,parent,patternId,cmEnvs = []):
    wx.Dialog.__init__(self,parent,armid.SPENVIRONMENT_ID,'Situate pattern',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,500))
    
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.assetEnvs = []
    self.panel = SecurityPatternEnvironmentPanel(self,patternId,cmEnvs)
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizerAndFit(mainSizer)
    wx.EVT_BUTTON(self,armid.SPENVIRONMENT_BUTTONCOMMIT_ID,self.onCommit)


  def onCommit(self,evt):
    self.assetEnvs = self.panel.assetEnvironments()
    for assetName,envs in self.assetEnvs.iteritems():
      if (len(envs) == 0):
        dlg = wx.MessageDialog(self,'Must situate ' + assetName + ' in at least one environment.','Situate Pattern',wx.OK)
        dlg.ShowModal() 
        dlg.Destroy()
        return
    self.EndModal(armid.SPENVIRONMENT_BUTTONCOMMIT_ID)

  def assetEnvironments(self): return self.assetEnvs
