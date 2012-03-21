#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/TargetDialog.py $ $Id: TargetDialog.py 551 2012-02-03 20:18:59Z shaf $
import wx
import armid
import WidgetFactory
from Borg import Borg

class TargetDialog(wx.Dialog):
  def __init__(self,parent,reqList,setTargets,envName):
    wx.Dialog.__init__(self,parent,armid.PROPERTY_ID,'Add Target',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,250))
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theTarget = ''
    self.theEffectiveness = ''
    self.theRationale = ''
    self.commitLabel = 'Add'
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.theTargetDictionary = self.dbProxy.targetNames(reqList,envName)
    defaultTargets = set(self.theTargetDictionary.keys())
    targetList = list(defaultTargets.difference(setTargets))
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Target',(87,30),armid.TARGET_COMBOTARGET_ID,targetList),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Effectiveness',(87,30),armid.TARGET_COMBOEFFECTIVENESS_ID,['None','Low','Medium','High']),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildMLTextSizer(self,'Rationale',(87,60),armid.TARGET_TEXTRATIONALE_ID),1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildAddCancelButtonSizer(self,armid.TARGET_BUTTONCOMMIT_ID),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.TARGET_BUTTONCOMMIT_ID,self.onCommit)

  def load(self,tName,eValue,tRationale):
    targetCtrl = self.FindWindowById(armid.TARGET_COMBOTARGET_ID)
    effectivenessCtrl = self.FindWindowById(armid.TARGET_COMBOEFFECTIVENESS_ID)
    ratCtrl = self.FindWindowById(armid.TARGET_TEXTRATIONALE_ID)
    commitCtrl = self.FindWindowById(armid.TARGET_BUTTONCOMMIT_ID)
    commitCtrl.SetLabel('Edit')
    targetCtrl.SetValue(tName)
    effectivenessCtrl.SetValue(eValue)
    ratCtrl.SetValue(tRationale)
    self.commitLabel = 'Edit'


  def onCommit(self,evt):
    targetCtrl = self.FindWindowById(armid.TARGET_COMBOTARGET_ID)
    effectivenessCtrl = self.FindWindowById(armid.TARGET_COMBOEFFECTIVENESS_ID)
    ratCtrl = self.FindWindowById(armid.TARGET_TEXTRATIONALE_ID)
    self.theTarget = targetCtrl.GetValue()
    self.theEffectiveness = effectivenessCtrl.GetValue()
    self.theRationale = ratCtrl.GetValue()

    labelTxt = self.commitLabel + ' mitigation target'
    if len(self.theTarget) == 0:
      dlg = wx.MessageDialog(self,'No target selected',labelTxt,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theEffectiveness) == 0):
      dlg = wx.MessageDialog(self,'No value selected',labelTxt,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theRationale) == 0):
      dlg = wx.MessageDialog(self,'No rationale provided',labelTxt,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(armid.TARGET_BUTTONCOMMIT_ID)

#  def target(self): return (self.theTarget,self.theTargetDictionary[self.theTarget])
  def target(self): return self.theTarget
  def effectiveness(self): return self.theEffectiveness
  def rationale(self): return self.theRationale
