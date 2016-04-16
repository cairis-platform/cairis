#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.



import wx
from cairis.core.armid import *
from cairis.core.Borg import Borg
from ReferenceListCtrl import ReferenceListCtrl
from ReferenceDialog import ReferenceDialog

class WarrantListCtrl(ReferenceListCtrl):
  def __init__(self,parent,backingList,isTask = False,pName = ''):
    ReferenceListCtrl.__init__(self,parent,PERSONACHARACTERISTIC_LISTWARRANT_ID,'warrant')
    self.thePcId = -1
    self.thePersonaName = pName
    self.theBackingList = backingList
    self.isTaskIndicator = isTask

  def onAddReference(self,evt):
    dlg = ReferenceDialog(self,self.theCharacteristicType)
    if (dlg.ShowModal() == CHARACTERISTICREFERENCE_BUTTONCOMMIT_ID):
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
