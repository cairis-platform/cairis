import wx
import armid
from ARM import *
from BehaviouralCharacteristicsDialog import BehaviouralCharacteristicsDialog
from Borg import Borg
from AssumptionTaskModel import AssumptionTaskModel
from ATModelViewer import ATModelViewer

class TCNarrativeTextCtrl(wx.TextCtrl):
  def __init__(self, parent, winId):
    wx.TextCtrl.__init__(self,parent,winId,size=(150,100),style=wx.TE_MULTILINE)
    self.ctrlMenu = wx.Menu()
    self.cmItem = self.ctrlMenu.Append(armid.TCNTC_LISTCHARACTERISTICS_ID,'Characteristics')
    self.viItem = self.ctrlMenu.Append(armid.TCNTC_VISCHARACTERISTICS_ID,'Visualise')
    wx.EVT_MENU(self,armid.TCNTC_LISTCHARACTERISTICS_ID,self.onListCharacteristics)
    wx.EVT_MENU(self,armid.TCNTC_VISCHARACTERISTICS_ID,self.onVisualiseCharacteristics)
    self.Bind(wx.EVT_RIGHT_DOWN, self.onRightClick)

    self.theTaskName = ''

    self.cmItem.Enable(False)
    self.viItem.Enable(False)

  def onRightClick(self,evt):
    self.PopupMenu(self.ctrlMenu)

  def onListCharacteristics(self,evt):
    try:
      dialog = BehaviouralCharacteristicsDialog(self,self.theTaskName)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Task Characteristics',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def Set(self,tName,ctrlVal):
    self.theTaskName = tName
    self.SetValue(ctrlVal)
    if (tName == ''):
      self.cmItem.Enable(False)
      self.viItem.Enable(False)
    else:
      self.cmItem.Enable(True)
      self.viItem.Enable(True)

  def onListCharacteristics(self,evt):
    try:
      dialog = BehaviouralCharacteristicsDialog(self,self.theTaskName)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Task Characteristics',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onVisualiseCharacteristics(self,evt):
    dialog = None
    try:
      b = Borg()
      modelAssocs = b.dbProxy.assumptionTaskModel(self.theTaskName)
      if (len(modelAssocs) > 0):
        associations = AssumptionTaskModel(modelAssocs)
        dialog = ATModelViewer(self.theTaskName)
        dialog.ShowModal(associations)
      else:
        errorTxt = 'No assumption task associations defined'
        dlg = wx.MessageDialog(self,errorTxt,'View Assumption Task Model',wx.OK | wx.ICON_EXCLAMATION)
        dlg.ShowModal()
        dlg.Destroy()
    except ARMException,errorText:
      dialog.destroy()
      dlg = wx.MessageDialog(self,str(errorText),'Edit Task Characteristics',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
