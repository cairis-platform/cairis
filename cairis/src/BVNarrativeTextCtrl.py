import wx
import armid
from ARM import *
from BehaviouralCharacteristicsDialog import BehaviouralCharacteristicsDialog
from Borg import Borg
from AssumptionPersonaModel import AssumptionPersonaModel
from APModelViewer import APModelViewer

class BVNarrativeTextCtrl(wx.TextCtrl):
  def __init__(self, parent, winId):
    wx.TextCtrl.__init__(self,parent,winId,style=wx.TE_MULTILINE)
    self.ctrlMenu = wx.Menu()
    self.cmItem = self.ctrlMenu.Append(armid.BVNTC_LISTCHARACTERISTICS_ID,'Characteristics')
    self.viItem = self.ctrlMenu.Append(armid.BVNTC_VISCHARACTERISTICS_ID,'Visualise')
    wx.EVT_MENU(self,armid.BVNTC_LISTCHARACTERISTICS_ID,self.onListCharacteristics)
    wx.EVT_MENU(self,armid.BVNTC_VISCHARACTERISTICS_ID,self.onVisualiseCharacteristics)
    self.Bind(wx.EVT_RIGHT_DOWN, self.onRightClick)

    self.thePersonaName = ''
    self.theBehaviouralVariable = ''

    self.cmItem.Enable(False)
    self.viItem.Enable(False)

  def onRightClick(self,evt):
    self.PopupMenu(self.ctrlMenu)

  def onListCharacteristics(self,evt):
    try:
      dialog = BehaviouralCharacteristicsDialog(self,self.thePersonaName,self.theBehaviouralVariable)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Persona Characteristics',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def Set(self,pName,bvName,ctrlVal):
    self.thePersonaName = pName
    self.theBehaviouralVariable = bvName
    self.SetValue(ctrlVal)
    if (pName == ''):
      self.cmItem.Enable(False)
      self.viItem.Enable(False)
    else:
      self.cmItem.Enable(True)
      self.viItem.Enable(True)

  def onListCharacteristics(self,evt):
    try:
      dialog = BehaviouralCharacteristicsDialog(self,self.thePersonaName,self.theBehaviouralVariable)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Persona Characteristics',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onVisualiseCharacteristics(self,evt):
    dialog = None
    try:
      b = Borg()
      modelAssocs = b.dbProxy.assumptionPersonaModel(self.thePersonaName,self.theBehaviouralVariable)
      if (len(modelAssocs) > 0):
        associations = AssumptionPersonaModel(modelAssocs)
        dialog = APModelViewer(self.thePersonaName,self.theBehaviouralVariable)
        dialog.ShowModal(associations)
      else:
        errorTxt = 'No assumption persona associations defined'
        dlg = wx.MessageDialog(self,errorTxt,'View Assumption Persona Model',wx.OK | wx.ICON_EXCLAMATION)
        dlg.ShowModal()
        dlg.Destroy()
    except ARMException,errorText:
      dialog.destroy()
      dlg = wx.MessageDialog(self,str(errorText),'Edit Persona Characteristics',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
