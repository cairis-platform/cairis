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
import armid
import PersonaCharacteristic
from PersonaCharacteristicDialog import PersonaCharacteristicDialog
from DialogClassParameters import DialogClassParameters
import ARM
from DimensionBaseDialog import DimensionBaseDialog

class PersonaCharacteristicsDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,armid.PERSONACHARACTERISTICS_ID,'Persona Characteristics',(930,300),'persona.png')
    self.theMainWindow = parent
    idList = [armid.PERSONACHARACTERISTICS_CHARLIST_ID,armid.PERSONACHARACTERISTICS_BUTTONADD_ID,armid.PERSONACHARACTERISTICS_BUTTONDELETE_ID]
    columnList = ['Persona','Variable','Characteristic']
    self.buildControls(idList,columnList,self.dbProxy.getPersonaCharacteristics,'persona_characteristic')
    listCtrl = self.FindWindowById(armid.PERSONACHARACTERISTICS_CHARLIST_ID)
    listCtrl.SetColumnWidth(0,100)
    listCtrl.SetColumnWidth(1,100)
    listCtrl.SetColumnWidth(2,700)


  def addObjectRow(self,listCtrl,listRow,objt):
    listCtrl.InsertStringItem(listRow,objt.persona())
    listCtrl.SetStringItem(listRow,1,objt.behaviouralVariable())
    listCtrl.SetStringItem(listRow,2,objt.characteristic())

  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters(armid.PERSONACHARACTERISTIC_ID,'Add Persona Characteristic',PersonaCharacteristicDialog,armid.PERSONACHARACTERISTIC_BUTTONCOMMIT_ID,self.dbProxy.addPersonaCharacteristic,True)
      self.addObject(addParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add persona characteristic',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.deprecatedLabel()]
    objtId = selectedObjt.id()
    try:
      updateParameters = DialogClassParameters(armid.PERSONACHARACTERISTIC_ID,'Edit Persona Characteristic',PersonaCharacteristicDialog,armid.PERSONACHARACTERISTIC_BUTTONCOMMIT_ID,self.dbProxy.updatePersonaCharacteristic,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit persona characteristic',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No persona characteristic','Delete persona characteristic',self.dbProxy.deletePersonaCharacteristic)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete persona characteristic',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def deprecatedLabel(self):
    listCtrl = self.FindWindowById(armid.PERSONACHARACTERISTICS_CHARLIST_ID)
    pItem = listCtrl.GetItem(self.selectedIdx,0)
    pTxt = pItem.GetText()
    bvItem = listCtrl.GetItem(self.selectedIdx,1)
    bvTxt = bvItem.GetText()
    charItem = listCtrl.GetItem(self.selectedIdx,2)
    charTxt = charItem.GetText()
    pcLabel = pTxt + '/' + bvTxt + '/' + charTxt
    return pcLabel
