#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ExposedCountermeasurePanel.py $ $Id: ExposedCountermeasurePanel.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
import WidgetFactory
from Borg import Borg

class ExposedCountermeasurePanel(wx.Panel):
  def __init__(self,parent,exposedCMs):
    wx.Panel.__init__(self,parent,-1)
    b = Borg()
    self.dbProxy = b.dbProxy
    eValues = ['Low','Medium','High']
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    cmSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(cmSizer,1,wx.EXPAND)
    isFirst = True
    self.cmAssets = {}
    for envName,cmName,assetName,cmEffectiveness in exposedCMs:
      cmKey = envName + '/' + cmName + ' (' + assetName + ')'
      self.cmAssets[cmKey] = assetName
      ecBox = wx.StaticBox(self,-1,cmKey)
      ecBoxSizer = wx.StaticBoxSizer(ecBox,wx.HORIZONTAL)
      cmSizer.Add(ecBoxSizer,0,wx.EXPAND)
      for eValue in eValues:
        if (isFirst == True):
          rb = wx.RadioButton(self,-1,eValue,pos=wx.DefaultPosition,style=wx.RB_GROUP)
          isFirst = False
        else:
          rb = wx.RadioButton(self,-1,eValue)
        ecBoxSizer.Add(rb,0,wx.EXPAND)
        if (eValue == cmEffectiveness):
          rb.SetValue(True)
        else:
          rb.SetValue(False)
          isFirst = False
      isFirst = True
    mainSizer.Add(WidgetFactory.buildCommitButtonSizer(self,armid.EXPOSEDCOUNTERMEASURE_BUTTONCOMMIT_ID,True),0,wx.CENTER)
    self.SetSizer(mainSizer)

  def countermeasureEffectiveness(self):
    mainSizer = self.GetSizer()
    mainChildren = mainSizer.GetChildren()
    cmSizerItem = mainChildren[0]
    ceSizer = cmSizerItem.GetSizer()
    cmEffectivenessList = []
    for ceItem in ceSizer.GetChildren():
      rowSizer = ceItem.GetSizer()
      envCmName = rowSizer.GetStaticBox().GetLabel()
      assetName = self.cmAssets[envCmName]
      ecTxt = envCmName[0:envCmName.find('(')]
      envName,cmName = ecTxt.split('/')
      for colItem in rowSizer.GetChildren():
        rBox = colItem.GetWindow()
        if (rBox.GetValue() == True):
          cmEffectiveness = rBox.GetLabel()
      cmEffectivenessList.append((envName,cmName,assetName,cmEffectiveness))
    return cmEffectivenessList
