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
from PersonaCharacteristicNotebook import PersonaCharacteristicNotebook
from PersonaCharacteristicParameters import PersonaCharacteristicParameters
from BaseDialog import BaseDialog 

class PersonaCharacteristicDialog(BaseDialog):
  def __init__(self,parent,parameters):
    BaseDialog.__init__(self,parent,parameters.id(),parameters.label(),(700,300))
    self.thePersonaName = ''
    self.theVariable = ''
    self.theModalQualifier = ''
    self.theCharacteristic = ''
    self.theGrounds = []
    self.theWarrant = []
    self.theBacking = []
    self.theRebuttal = []
    self.isCreate = True

    self.theId = -1
    self.panel = 0
    self.inPersona = False
    if (parameters.__class__.__name__ == 'PersonaCharacteristicDialogParameters'):
      self.inPersona = True

    if (self.inPersona):
      self.thePersonaName = parameters.persona()
      self.theVariable = parameters.behaviouralVariable()

    self.commitVerb = 'Add'
    
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = PersonaCharacteristicNotebook(self,self.thePersonaName)
    mainSizer.Add(self.panel,1,wx.EXPAND)
    mainSizer.Add(self.buildCommitButtonSizer(armid.PERSONACHARACTERISTIC_BUTTONCOMMIT_ID,True),0,wx.CENTER)

    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.PERSONACHARACTERISTIC_BUTTONCOMMIT_ID,self.onCommit)

  def load(self,objt):
    self.theId = objt.id()
    buttonCtrl = self.FindWindowById(armid.PERSONACHARACTERISTIC_BUTTONCOMMIT_ID)
    buttonCtrl.SetLabel('Edit')
    self.panel.loadControls(objt)
    self.commitVerb = 'Edit'

  def onCommit(self,evt):
    commitLabel = self.commitVerb + ' persona characteristic'

    qualCtrl = self.FindWindowById(armid.PERSONACHARACTERISTIC_TEXTQUALIFIER_ID)
    charCtrl = self.FindWindowById(armid.PERSONACHARACTERISTIC_TEXTCHARACTERISTIC_ID)
    groundsCtrl = self.FindWindowById(armid.PERSONACHARACTERISTIC_LISTGROUNDS_ID)
    warrantCtrl = self.FindWindowById(armid.PERSONACHARACTERISTIC_LISTWARRANT_ID)
    rebuttalCtrl = self.FindWindowById(armid.PERSONACHARACTERISTIC_LISTREBUTTAL_ID)

    self.theModalQualifier = qualCtrl.GetValue()
    self.theCharacteristic = charCtrl.GetValue()
    self.theGrounds = groundsCtrl.dimensions()
    self.theWarrant = warrantCtrl.dimensions()
    self.theRebuttal = rebuttalCtrl.dimensions()
 
    
    if (self.inPersona == False):
      pCtrl = self.FindWindowById(armid.PERSONACHARACTERISTIC_COMBOPERSONA_ID)
      varCtrl = self.FindWindowById(armid.PERSONACHARACTERISTIC_COMBOVARIABLE_ID)
      self.thePersonaName = pCtrl.GetValue()
      self.theVariable = varCtrl.GetValue()

    if len(self.thePersonaName) == 0:
      dlg = wx.MessageDialog(self,'Persona cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theVariable) == 0:
      dlg = wx.MessageDialog(self,'Variable cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theModalQualifier) == 0:
      dlg = wx.MessageDialog(self,'Model Qualifier cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theCharacteristic) == 0:
      dlg = wx.MessageDialog(self,'Characteristic cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theGrounds) == 0:
      dlg = wx.MessageDialog(self,'Some grounds for this characteristic must be provided',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(armid.PERSONACHARACTERISTIC_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = PersonaCharacteristicParameters(self.thePersonaName,self.theModalQualifier,self.theVariable,self.theCharacteristic,self.theGrounds,self.theWarrant,[],self.theRebuttal)
    parameters.setId(self.theId)
    return parameters
