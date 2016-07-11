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
import os
from cairis.core.ARM import *
from cairis.core.Borg import Borg
from AttackerPanel import AttackerPanel
from cairis.core.AttackerParameters import AttackerParameters

class AttackerDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,parameters.id(),parameters.label(),style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(600,600))

    self.theAttackerId = -1
    self.theAttackerName = ''
    self.theAttackerDescription = ''
    self.theAttackerImage = ''
    self.theTags = []
    self.theEnvironmentProperties = []
    self.panel = 0
    self.buildControls(parameters)
    self.theCommitVerb = 'Create'
 
  def load(self,attacker):
    self.theAttackerId = attacker.id()
    imageFile = attacker.image()
    if ((imageFile != None) and (imageFile != '')):
      if (os.path.exists(imageFile) == False):
        attacker.theImage = ''
        errorText = 'Attacker image ' + imageFile + ' does not exist.'
        dlg = wx.MessageDialog(self,errorText,'Load Attacker Image',wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
    self.panel.loadControls(attacker)
    self.theCommitVerb = 'Edit'

  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = AttackerPanel(self)
    self.panel.buildControls(parameters.createFlag())
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,ATTACKER_BUTTONCOMMIT_ID,self.onCommit)


  def onCommit(self,evt):
    nameCtrl = self.FindWindowById(ATTACKER_TEXTNAME_ID)
    tagCtrl = self.FindWindowById(ATTACKER_TAGS_ID)
    descriptionCtrl = self.FindWindowById(ATTACKER_TEXTDESCRIPTION_ID)
    imageCtrl = self.FindWindowById(ATTACKER_IMAGEATTACKERIMAGE_ID)
    environmentCtrl = self.FindWindowById(ATTACKER_PANELENVIRONMENT_ID)

    self.theAttackerName = nameCtrl.GetValue()
    if (self.theCommitVerb == 'Create'):
      b = Borg()
      try:
        b.dbProxy.nameCheck(self.theAttackerName,'attacker')
      except ARMException,errorText:
        dlg = wx.MessageDialog(self,str(errorText),'Add attacker',wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
        return

    self.theAttackerDescription = descriptionCtrl.GetValue()
    self.theAttackerImage = imageCtrl.personaImage()
    self.theTags = tagCtrl.tags()
    self.theEnvironmentProperties = environmentCtrl.environmentProperties()

    commitLabel = self.theCommitVerb + ' attacker'
    if len(self.theAttackerName) == 0:
      dlg = wx.MessageDialog(self,'Attacker name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theEnvironmentProperties) == 0):
      dlg = wx.MessageDialog(self,'No environments have been associated with this attacker',commitLabel,wx.OK) 
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
        if len(environmentProperties.motives()) == 0:
          errorTxt = 'No motives associated with environment ' + environmentProperties.name()
          dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK) 
          dlg.ShowModal()
          dlg.Destroy()
          return
        if len(environmentProperties.capabilities()) == 0:
          errorTxt = 'No capabilities associated with environment ' + environmentProperties.name()
          dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK) 
          dlg.ShowModal()
          dlg.Destroy()
          return
      self.EndModal(ATTACKER_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = AttackerParameters(self.theAttackerName,self.theAttackerDescription,self.theAttackerImage,self.theTags,self.theEnvironmentProperties)
    parameters.setId(self.theAttackerId)
    return parameters
