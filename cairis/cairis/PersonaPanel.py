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
from Borg import Borg
from BasePanel import BasePanel
from SummaryDetailsNotebook import SummaryDetailsNotebook
from PersonaEnvironmentPanel import PersonaEnvironmentPanel
from PersonalImageView import PersonalImageView

class PersonaPanel(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,armid.PERSONA_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
 
  def buildControls(self,isCreate,isUpdateable = True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(self.buildTextSizer('Name',(87,30),armid.PERSONA_TEXTNAME_ID),0,wx.EXPAND)

    pTypes = self.dbProxy.getDimensionNames('persona_type')
    mainSizer.Add(self.buildComboSizerList('Type',(87,30),armid.PERSONA_COMBOTYPE_ID,pTypes),0,wx.EXPAND)

    directBox = wx.StaticBox(self,-1,'Assumption Persona')
    directSizer = wx.StaticBoxSizer(directBox,wx.HORIZONTAL)
    mainSizer.Add(directSizer,0,wx.EXPAND)
    self.directCtrl = wx.CheckBox(self,armid.PERSONA_CHECKASSUMPTION_ID)
    self.directCtrl.SetValue(False)
    directSizer.Add(self.directCtrl,0,wx.EXPAND)

    sdSizer = wx.BoxSizer(wx.HORIZONTAL)
    self.nb = SummaryDetailsNotebook(self)
    mainSizer.Add(sdSizer,1,wx.EXPAND)
    sdSizer.Add(self.nb,1,wx.EXPAND)

    iBox = wx.StaticBox(self,-1)
    iSizer = wx.StaticBoxSizer(iBox,wx.HORIZONTAL)
    sdSizer.Add(iSizer,1,wx.EXPAND)
    imagePanel = PersonalImageView(self,armid.PERSONA_IMAGEPERSONAIMAGE_ID)
    iSizer.Add(imagePanel,1,wx.EXPAND)

    self.environmentPanel = PersonaEnvironmentPanel(self,self.dbProxy)
    mainSizer.Add(self.environmentPanel,1,wx.EXPAND)

    mainSizer.Add(self.buildCommitButtonSizer(armid.PERSONA_BUTTONCOMMIT_ID,isCreate),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

  def loadControls(self,persona):
    nameCtrl = self.FindWindowById(armid.PERSONA_TEXTNAME_ID)
    typeCtrl = self.FindWindowById(armid.PERSONA_COMBOTYPE_ID)
    assumptionCtrl = self.FindWindowById(armid.PERSONA_CHECKASSUMPTION_ID)
    activitiesCtrl = self.nb.FindWindowById(armid.PERSONA_TEXTACTIVITIES_ID)
    attitudesCtrl = self.nb.FindWindowById(armid.PERSONA_TEXTATTITUDES_ID)
    aptitudesCtrl = self.nb.FindWindowById(armid.PERSONA_TEXTAPTITUDES_ID)
    motivationsCtrl = self.nb.FindWindowById(armid.PERSONA_TEXTMOTIVATIONS_ID)
    skillsCtrl = self.nb.FindWindowById(armid.PERSONA_TEXTSKILLS_ID)
    imageCtrl = self.FindWindowById(armid.PERSONA_IMAGEPERSONAIMAGE_ID)
    nameCtrl.SetValue(persona.name())
    typeCtrl.SetValue(persona.type())
    assumptionCtrl.SetValue(persona.assumption())
    activitiesCtrl.Set(persona.name(),'Activities',persona.activities())
    attitudesCtrl.Set(persona.name(),'Attitudes',persona.attitudes())
    aptitudesCtrl.Set(persona.name(),'Aptitudes',persona.aptitudes())
    motivationsCtrl.Set(persona.name(),'Motivations',persona.motivations())
    skillsCtrl.Set(persona.name(),'Skills',persona.skills())
    imageCtrl.loadImage(persona.image())

    activitiesCtrl.setCodes(persona.codes('activities'))
    attitudesCtrl.setCodes(persona.codes('attitudes'))
    aptitudesCtrl.setCodes(persona.codes('aptitudes'))
    motivationsCtrl.setCodes(persona.codes('motivations'))
    skillsCtrl.setCodes(persona.codes('skills'))

    self.environmentPanel.loadControls(persona)

    self.thePersonaId = persona.id()
