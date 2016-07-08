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
from BasePanel import BasePanel
from DimensionNameDialog import DimensionNameDialog
from DialogClassParameters import DialogClassParameters
from DocumentReferenceDialog import DocumentReferenceDialog
from ConceptReferenceDialog import ConceptReferenceDialog
from cairis.core.Borg import Borg

class PersonaCharacteristicPanel(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,PERSONACHARACTERISTIC_ID)
    self.theId = None
    b = Borg()
    self.dbProxy = b.dbProxy
    
  def buildControls(self,isCreate,inPersona):
    mainSizer = wx.BoxSizer(wx.VERTICAL)

    if (inPersona == False):
      personas = self.dbProxy.getDimensionNames('persona')
      mainSizer.Add(self.buildComboSizerList('Persona',(87,30),PERSONACHARACTERISTIC_COMBOPERSONA_ID,personas),0,wx.EXPAND)

    mainSizer.Add(self.buildRadioButtonSizer('Type',(87,30),[(PERSONACHARACTERISTIC_RADIOREFERENCE_ID,'Reference'),(PERSONACHARACTERISTIC_RADIOCONCEPT_ID,'Concept')]))

    refs = ['[New reference]']
    refs += self.dbProxy.getDimensionNames('document_reference')
    mainSizer.Add(self.buildComboSizerList('Reference',(87,30),PERSONACHARACTERISTIC_COMBOREFERENCE_ID,refs),0,wx.EXPAND)

    if (inPersona == False):
      bVars = self.dbProxy.getDimensionNames('behavioural_variable')
      mainSizer.Add(self.buildComboSizerList('Behavioural Variable',(87,30),PERSONACHARACTERISTIC_COMBOVARIABLE_ID,bVars),0,wx.EXPAND)

    mainSizer.Add(self.buildMLTextSizer('Characteristic',(87,30),PERSONACHARACTERISTIC_TEXTCHARACTERISTIC_ID),1,wx.EXPAND)
    mainSizer.Add(self.buildCommitButtonSizer(PERSONACHARACTERISTIC_BUTTONCOMMIT_ID,isCreate),0,wx.CENTER)
    wx.EVT_COMBOBOX(self,PERSONACHARACTERISTIC_COMBOREFERENCE_ID,self.onReferenceChange)
    wx.EVT_RADIOBUTTON(self,PERSONACHARACTERISTIC_RADIOREFERENCE_ID,self.onReferenceSelected)
    wx.EVT_RADIOBUTTON(self,PERSONACHARACTERISTIC_RADIOCONCEPT_ID,self.onConceptSelected)
    self.SetSizer(mainSizer)

  def loadControls(self,objt,inPersona):
    self.theId = objt.id()

    refCtrl = self.FindWindowById(PERSONACHARACTERISTIC_COMBOREFERENCE_ID)
    charCtrl = self.FindWindowById(PERSONACHARACTERISTIC_TEXTCHARACTERISTIC_ID)
    refCtrl.SetValue(objt.reference())
    charCtrl.SetValue(objt.characteristic())

    if (inPersona == False):
      pCtrl = self.FindWindowById(PERSONACHARACTERISTIC_COMBOPERSONA_ID)
      varCtrl = self.FindWindowById(PERSONACHARACTERISTIC_COMBOVARIABLE_ID)
      pCtrl.SetValue(objt.persona())
      varCtrl.SetValue(objt.behaviouralVariable())

  def onReferenceChange(self,evt):
    refValue = evt.GetString()
    if (refValue == '[New reference]' or refValue == '[New concept]'):
      if (refValue == '[New reference]'):
        addParameters = DialogClassParameters(DOCUMENTREFERENCE_ID,'Add Document Reference',DocumentReferenceDialog,DOCUMENTREFERENCE_BUTTONCOMMIT_ID,self.dbProxy.addDocumentReference,True)
      else:
        addParameters = DialogClassParameters(CONCEPTREFERENCE_ID,'Add Concept Reference',ConceptReferenceDialog,CONCEPTREFERENCE_BUTTONCOMMIT_ID,self.dbProxy.addConceptReference,True)
      dialogClass = addParameters.dclass()
      addDialog = dialogClass(self,addParameters)
      if (addDialog.ShowModal() == addParameters.createButtonId()):
        dialogOutParameters = addDialog.parameters()
        addFn = addParameters.setter()
        objtId = addFn(dialogOutParameters)
        dimName = dialogOutParameters.name()
        refCtrl = self.FindWindowById(PERSONACHARACTERISTIC_COMBOREFERENCE_ID)
        refCtrl.Append(dimName)
        refCtrl.SetValue(dimName)
      addDialog.Destroy()

  def onReferenceSelected(self,evt):
    refCtrl = self.FindWindowById(PERSONACHARACTERISTIC_COMBOREFERENCE_ID)
    refs = ['[New reference]']
    refs += self.dbProxy.getDimensionNames('document_reference')
    refCtrl.SetItems(refs)
    refCtrl.SetValue('')

  def onConceptSelected(self,evt):
    refCtrl = self.FindWindowById(PERSONACHARACTERISTIC_COMBOREFERENCE_ID)
    refs = ['[New concept]']
    refs += self.dbProxy.getDimensionNames('concept_reference')
    refCtrl.SetItems(refs)
    refCtrl.SetValue('')

