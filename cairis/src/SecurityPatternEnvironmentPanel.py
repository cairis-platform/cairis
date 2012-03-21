#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/SecurityPatternEnvironmentPanel.py $ $Id: SecurityPatternEnvironmentPanel.py 523 2011-11-04 18:07:01Z shaf $
import wx
import armid
from Borg import Borg

class SecurityPatternEnvironmentPanel(wx.Panel):
  def __init__(self,parent,patternId,cmEnvs = []):
    wx.Panel.__init__(self,parent,-1)
    b = Borg()
    self.dbProxy = b.dbProxy
    
    if (len(cmEnvs) == 0):
      self.envs = self.dbProxy.getEnvironmentNames()
    else:
      self.envs = cmEnvs
    self.patternAssets = self.dbProxy.patternAssets(patternId)

    mainSizer = wx.BoxSizer(wx.VERTICAL)
    assetSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(assetSizer,1,wx.EXPAND)
    for assetName in self.patternAssets:
      aBox = wx.StaticBox(self,-1,assetName)
      aBoxSizer = wx.StaticBoxSizer(aBox,wx.HORIZONTAL)
      assetSizer.Add(aBoxSizer,0,wx.EXPAND)
      for envName in self.envs:
        cb = wx.CheckBox(self,-1,envName)
        aBoxSizer.Add(cb,0,wx.EXPAND)
      
    buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
    buttonSizer.Add(wx.Button(self,armid.SPENVIRONMENT_BUTTONCOMMIT_ID))
    buttonSizer.Add(wx.Button(parent,wx.ID_CANCEL,"Close"))
    mainSizer.Add(buttonSizer,0,wx.CENTER)
    self.SetSizer(mainSizer)

  def assetEnvironments(self):
    mainSizer = self.GetSizer()
    mainChildren = mainSizer.GetChildren()
    assetSizerItem = mainChildren[0]
    assetSizer = assetSizerItem.GetSizer()
    assetEnvs = {}
    for aItem in assetSizer.GetChildren():
      rowSizer = aItem.GetSizer()
      assetName = rowSizer.GetStaticBox().GetLabel()
      envs = []
      for colItem in rowSizer.GetChildren():
        checkBox = colItem.GetWindow()
        if (checkBox.GetValue() == True):
          envs.append(checkBox.GetLabel())
      assetEnvs[assetName] = envs
    return assetEnvs
