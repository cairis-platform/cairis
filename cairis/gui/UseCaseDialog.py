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


#$URL$ $Id: UseCaseDialog.py 530 2011-11-16 19:29:16Z shaf $
import wx
from cairis.core.armid import *
from cairis.core.UseCaseParameters import UseCaseParameters
import WidgetFactory
from UseCasePanel import UseCasePanel
from cairis.core.UseCaseEnvironmentProperties import UseCaseEnvironmentProperties
from cairis.core.Borg import Borg

class UseCaseDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,parameters.id(),parameters.label(),style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(700,800))
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theUseCaseId = -1
    self.theName = ''
    self.theTags = []
    self.theAuthor = ''
    self.theCode = '' 
    self.theActors = []
    self.theDescription = ''
    self.theEnvironmentProperties = []
    self.panel = 0
    self.theCommitVerb = 'Create'
    self.buildControls(parameters)

  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = UseCasePanel(self)
    mainSizer.Add(self.panel,1,wx.EXPAND)
    if (self.theCommitVerb == 'Create'):
      isCreate = True
    else:
      isCreate = False
    mainSizer.Add(WidgetFactory.buildCommitButtonSizer(self,USECASE_BUTTONCOMMIT_ID,isCreate),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,USECASE_BUTTONCOMMIT_ID,self.onCommit)

  def load(self,uc):
    self.theUseCaseId = uc.id()
    self.theCommitVerb = 'Edit'
    buttonCtrl = self.FindWindowById(USECASE_BUTTONCOMMIT_ID)
    buttonCtrl.SetLabel('Update')
    self.panel.loadControls(uc)

  def onCommit(self,evt):
    nameCtrl = self.FindWindowById(USECASE_TEXTNAME_ID)
    tagCtrl = self.FindWindowById(USECASE_TAGS_ID)
    authCtrl = self.FindWindowById(USECASE_TEXTAUTHOR_ID)
    codeCtrl = self.FindWindowById(USECASE_TEXTSHORTCODE_ID)
    actorsCtrl = self.FindWindowById(USECASE_LISTACTORS_ID)
    descCtrl = self.FindWindowById(USECASE_TEXTDESCRIPTION_ID)
    environmentCtrl = self.FindWindowById(USECASE_PANELENVIRONMENT_ID)

    self.theName = nameCtrl.GetValue()
    self.theTags = tagCtrl.tags()
    self.theAuthor = authCtrl.GetValue()
    self.theCode = codeCtrl.GetValue()
    self.theActors = actorsCtrl.dimensions()
    self.theDescription = descCtrl.GetValue()

    self.theEnvironmentProperties = environmentCtrl.environmentProperties()
    commitLabel = self.theCommitVerb +  ' Use Case' 

    if (len(self.theName) == 0):
      dlg = wx.MessageDialog(self,'Name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theAuthor) == 0):
      dlg = wx.MessageDialog(self,'Author name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theCode) == 0):
      dlg = wx.MessageDialog(self,'Code cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theActors) == 0):
      dlg = wx.MessageDialog(self,'At least one actor must be selected',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theDescription) == 0):
      dlg = wx.MessageDialog(self,'Description cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      if (len(self.theEnvironmentProperties) == 0):
        errorTxt = 'At least one environment must be associated with this use case'
        dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK) 
        dlg.ShowModal()
        dlg.Destroy()
        return

      for environmentProperties in self.theEnvironmentProperties:
        if len(environmentProperties.preconditions()) == 0:
          errorTxt = 'Preconditions cannot be empty in environment ' + environmentProperties.name()
          dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK) 
          dlg.ShowModal()
          dlg.Destroy()
          return
        if environmentProperties.steps().size() == 0:
          errorTxt = 'Flow in environment ' + environmentProperties.name() + ' must contain at least 1 step'
          dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK) 
          dlg.ShowModal()
          dlg.Destroy()
          return
        if len(environmentProperties.postconditions()) == 0:
          errorTxt = 'Postconditions cannot be empty in environment ' + environmentProperties.name()
          dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK) 
          dlg.ShowModal()
          dlg.Destroy()
          return
    self.EndModal(USECASE_BUTTONCOMMIT_ID)

  def parameters(self): 
    parameters = UseCaseParameters(self.theName,self.theAuthor,self.theCode,self.theActors,self.theDescription,self.theTags,self.theEnvironmentProperties)
    parameters.setId(self.theUseCaseId)
    return parameters
