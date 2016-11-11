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
import WidgetFactory
import os
from cairis.core.Borg import Borg
from cairis.core.ARM import *
from cairis.core.PersonaParameters import PersonaParameters
from PersonaPanel import PersonaPanel

__author__ = 'Shamal Faily'

class PersonaDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,parameters.id(),parameters.label(),style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(500,800))
    self.theParent = parent 
    self.thePersonaId = -1
    self.thePersonaName = ''
    self.theTags = []
    self.isAssumption = False
    self.theActivities = ''
    self.theAttitudes = ''
    self.theAptitudes = ''
    self.theMotivations = ''
    self.theSkills = ''
    self.theIntrinsic = ''
    self.theContextual = ''
    self.theImage = ''
    self.theType = ''
    self.theCodes = {'activities':{}, 'attitudes':{}, 'motivations':{}, 'skills':{}, 'intrinsic':{}, 'contextual':{}}
    self.theEnvironmentProperties = []
    self.panel = 0
    self.buildControls(parameters)
    self.theCommitVerb = 'Create'

  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = PersonaPanel(self)
    self.panel.buildControls(parameters.createFlag())
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,PERSONA_BUTTONCOMMIT_ID,self.onCommit)

  def load(self,persona):
    self.thePersonaId = persona.id()
    personaImage = persona.image()
    b = Borg()
    imageFile = b.imageDir + "/" + persona.image()
    if ((personaImage != None) and (imageFile != '')):
      if (os.path.exists(imageFile) == False):
        errorText = 'Persona image ' + imageFile + ' does not exist.'
        dlg = wx.MessageDialog(self.theParent,errorText,'Load Persona Image',wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
        persona.theImage = ''
    self.panel.loadControls(persona)
    self.theCommitVerb = 'Edit'
   

  def onCommit(self,evt):
    nameCtrl = self.FindWindowById(PERSONA_TEXTNAME_ID)
    tagCtrl = self.FindWindowById(PERSONA_TAGS_ID)
    typeCtrl = self.FindWindowById(PERSONA_COMBOTYPE_ID)
    assumptionCtrl = self.FindWindowById(PERSONA_CHECKASSUMPTION_ID)
    activitiesCtrl = self.FindWindowById(PERSONA_TEXTACTIVITIES_ID)
    attitudesCtrl = self.FindWindowById(PERSONA_TEXTATTITUDES_ID)
    aptitudesCtrl = self.FindWindowById(PERSONA_TEXTAPTITUDES_ID)
    motivationsCtrl = self.FindWindowById(PERSONA_TEXTMOTIVATIONS_ID)
    skillsCtrl = self.FindWindowById(PERSONA_TEXTSKILLS_ID)
    intrinsicCtrl = self.FindWindowById(PERSONA_TEXTINTRINSIC_ID)
    contextualCtrl = self.FindWindowById(PERSONA_TEXTCONTEXTUAL_ID)
    imageCtrl = self.FindWindowById(PERSONA_IMAGEPERSONAIMAGE_ID)
    environmentCtrl = self.FindWindowById(PERSONA_PANELENVIRONMENT_ID)

    self.thePersonaName = nameCtrl.GetValue()
    self.theTags = tagCtrl.tags()
    if (self.theCommitVerb == 'Create'):
      b = Borg()
      try:
        b.dbProxy.nameCheck(self.thePersonaName,'persona')
      except ARMException,errorText:
        dlg = wx.MessageDialog(self,str(errorText),'Add persona',wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
        return

    self.theType = typeCtrl.GetValue()
    self.isAssumption = assumptionCtrl.GetValue()
    self.theActivities = activitiesCtrl.GetValue()
    self.theCodes['activities'] = activitiesCtrl.codes()
    self.theAttitudes = attitudesCtrl.GetValue()
    self.theCodes['attitudes'] = attitudesCtrl.codes()
    self.theAptitudes = aptitudesCtrl.GetValue()
    self.theCodes['aptitudes'] = aptitudesCtrl.codes()
    self.theMotivations = motivationsCtrl.GetValue()
    self.theCodes['motivations'] = motivationsCtrl.codes()
    self.theSkills = skillsCtrl.GetValue()
    self.theCodes['skills'] = skillsCtrl.codes()
    self.theIntrinsic = intrinsicCtrl.GetValue()
    self.theCodes['intrinsic'] = intrinsicCtrl.codes()
    self.theContextual = contextualCtrl.GetValue()
    self.theCodes['contextual'] = contextualCtrl.codes()
    self.theImage = imageCtrl.personaImage()
    
    self.theEnvironmentProperties = environmentCtrl.environmentProperties()

    commitLabel = self.theCommitVerb + ' persona'

    if len(self.thePersonaName) == 0:
      dlg = wx.MessageDialog(self,'Persona name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theType) == 0:
      dlg = wx.MessageDialog(self,'Persona type cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theActivities) == 0:
      dlg = wx.MessageDialog(self,'Activities cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theAttitudes) == 0:
      dlg = wx.MessageDialog(self,'Attitudes cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theAptitudes) == 0:
      dlg = wx.MessageDialog(self,'Aptitudes cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theMotivations) == 0:
      dlg = wx.MessageDialog(self,'Motivations cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theSkills) == 0:
      dlg = wx.MessageDialog(self,'Skills cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theIntrinsic) == 0:
      dlg = wx.MessageDialog(self,'Intrinsic cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theContextual) == 0:
      dlg = wx.MessageDialog(self,'Contextual cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theEnvironmentProperties) == 0):
      dlg = wx.MessageDialog(self,'No environments have been associated with this persona',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      for environmentProperties in self.theEnvironmentProperties:
        if len(environmentProperties.roles()) == 0:
          errorTxt = 'No roles associated with environment ' + environmentProperties.name()
          dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK)
          dlg.ShowModal()
          dlg.Destroy()
          return
        if len(environmentProperties.narrative()) == 0:
          errorTxt = 'No narrative associated with environment ' + environmentProperties.name()
          dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK)
          dlg.ShowModal()
          dlg.Destroy()
          return
        if len(environmentProperties.directFlag()) == 0:
          errorTxt = 'No direct flag associated with environment ' + environmentProperties.name()
          dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK)
          dlg.ShowModal()
          dlg.Destroy()
          return
      self.EndModal(PERSONA_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = PersonaParameters(self.thePersonaName,self.theActivities,self.theAttitudes,self.theAptitudes,self.theMotivations,self.theSkills,self.theIntrinsic,self.theContextual,self.theImage,self.isAssumption,self.theType,self.theTags,self.theEnvironmentProperties,self.theCodes)
    parameters.setId(self.thePersonaId)
    return parameters
