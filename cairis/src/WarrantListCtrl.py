#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/WarrantListCtrl.py $ $Id: WarrantListCtrl.py 465 2011-05-01 16:00:00Z shaf $

import wx
import armid
from Borg import Borg
from ReferenceListCtrl import ReferenceListCtrl
from ReferenceDialog import ReferenceDialog

class WarrantListCtrl(ReferenceListCtrl):
  def __init__(self,parent,backingList,isTask = False,pName = ''):
    ReferenceListCtrl.__init__(self,parent,armid.PERSONACHARACTERISTIC_LISTWARRANT_ID,'warrant')
    self.thePcId = -1
    self.thePersonaName = pName
    self.theBackingList = backingList
    self.isTaskIndicator = isTask

  def onAddReference(self,evt):
    dlg = ReferenceDialog(self,self.theCharacteristicType)
    if (dlg.ShowModal() == armid.CHARACTERISTICREFERENCE_BUTTONCOMMIT_ID):
      self.theSelectedIdx = self.GetItemCount()
      refName = dlg.reference()
      dimName = dlg.dimension()
      refDesc = dlg.description()
      self.InsertStringItem(self.theSelectedIdx,refName)
      self.SetStringItem(self.theSelectedIdx,1,refDesc)
      self.theReferenceTypeDictionary[refName] = dimName
      self.reloadBackingList()

  def onDeleteReference(self,evt):
    if (self.theSelectedIdx == -1):
      errorText = 'No reference selected'
      errorLabel = 'Delete ' + self.theCharacteristicType + ' reference'
      dlg = wx.MessageDialog(self,errorText,errorLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
    else:
      refName = self.GetItemText(self.theSelectedIdx)
      self.DeleteItem(self.theSelectedIdx)
      del self.theReferenceTypeDictionary[refName]
      self.reloadBackingList()
  
  def load(self,pcId,refs):
    self.thePcId = pcId
    ReferenceListCtrl.load(self,refs)
    self.reloadBackingList()

  def reloadBackingList(self):
    fnName = 'characteristicBacking'
    if (self.isTaskIndicator):
      fnName = 'taskCharacteristicBacking'
    backing = self.dbProxy.characteristicBacking(self.thePcId,fnName)
    self.theBackingList.DeleteAllItems()
    for idx,b in enumerate(backing):
      self.theBackingList.InsertStringItem(idx,b[0]) 
      self.theBackingList.SetStringItem(idx,1,b[1])
