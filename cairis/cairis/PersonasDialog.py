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
from PersonaDialog import PersonaDialog
from DialogClassParameters import DialogClassParameters
import ARM
from DimensionBaseDialog import DimensionBaseDialog

class PersonasDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,armid.PERSONAS_ID,'Personas',(800,300),'persona.png')
    idList = [armid.PERSONAS_PERSONALIST_ID,armid.PERSONAS_BUTTONADD_ID,armid.PERSONAS_BUTTONDELETE_ID]
    columnList = ['Name','Type']
    self.buildControls(idList,columnList,self.dbProxy.getPersonas,'persona')
    listCtrl = self.FindWindowById(armid.PERSONAS_PERSONALIST_ID)
    listCtrl.SetColumnWidth(0,100)
    listCtrl.SetColumnWidth(1,600)


  def addObjectRow(self,personaListCtrl,listRow,persona):
    personaListCtrl.InsertStringItem(listRow,persona.name())
    personaListCtrl.SetStringItem(listRow,1,persona.type())

  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters(armid.PERSONA_ID,'Add persona',PersonaDialog,armid.PERSONA_BUTTONCOMMIT_ID,self.dbProxy.addPersona,True)
      self.addObject(addParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add persona',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.selectedLabel]
    try:
      updateParameters = DialogClassParameters(armid.PERSONA_ID,'Edit persona',PersonaDialog,armid.PERSONA_BUTTONCOMMIT_ID,self.dbProxy.updatePersona,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit persona',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onDelete(self,evt):
    try:
      self.deleteObject('No persona','Delete persona',self.dbProxy.deletePersona)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete persona',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return
