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
from cairis.core.TaskParameters import TaskParameters
from TaskPanel import TaskPanel
from BaseDialog import BaseDialog
from cairis.core.TaskEnvironmentProperties import TaskEnvironmentProperties
from cairis.core.Borg import Borg

__author__ = 'Shamal Faily'

class TaskDialog(BaseDialog):
  def __init__(self,parent,parameters):
    BaseDialog.__init__(self,parent,parameters.id(),parameters.label(),(700,800))
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theTaskId = -1
    self.theName = ''
    self.theTags = []
    self.theShortCode = ''
    self.theObjective = ''
    self.isAssumption = False
    self.theAuthor = ''
    
    self.theEnvironmentProperties = []
    self.panel = 0
    self.buildControls(parameters)
    self.theCommitVerb = 'Create'

  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = TaskPanel(self,self.dbProxy)
    self.panel.buildControls(parameters.createFlag())
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,TASK_BUTTONCOMMIT_ID,self.onCommit)

  def load(self,task):
    self.theTaskId = task.id()
    self.panel.loadControls(task)
    self.theCommitVerb = 'Edit'

  def onCommit(self,evt):
    nameCtrl = self.FindWindowById(TASK_TEXTNAME_ID)
    tagCtrl = self.FindWindowById(TASK_TAGS_ID)
    shortCodeCtrl = self.FindWindowById(TASK_TEXTSHORTCODE_ID)
    authorCtrl = self.FindWindowById(TASK_TEXTAUTHOR_ID)
    objectiveCtrl = self.FindWindowById(TASK_TEXTOBJECTIVE_ID)
    assumptionCtrl = self.FindWindowById(TASK_CHECKASSUMPTION_ID)
    environmentCtrl = self.FindWindowById(TASK_PANELENVIRONMENT_ID)

    self.theName = nameCtrl.GetValue()
    self.theShortCode = shortCodeCtrl.GetValue()
    self.theAuthor = authorCtrl.GetValue()
    self.isAssumption = assumptionCtrl.GetValue()
    self.theObjective = objectiveCtrl.GetValue()
    self.theTags = tagCtrl.tags()
    self.theEnvironmentProperties = environmentCtrl.environmentProperties()

    commitLabel = self.theCommitVerb +  ' Task' 

    if (len(self.theName) == 0):
      dlg = wx.MessageDialog(self,'Name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theShortCode) == 0):
      dlg = wx.MessageDialog(self,'Short Code cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theAuthor) == 0):
      dlg = wx.MessageDialog(self,'Author cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theObjective) == 0):
      dlg = wx.MessageDialog(self,'Objective cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      for environmentProperties in self.theEnvironmentProperties:
        if len(environmentProperties.personas()) == 0:
          errorTxt = 'No personas defined in environment ' + environmentProperties.name()
          dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK) 
          dlg.ShowModal()
          dlg.Destroy()
          return
        if len(environmentProperties.dependencies()) == 0:
          errorTxt = 'No dependencies defined in environment ' + environmentProperties.name()
          dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK) 
          dlg.ShowModal()
          dlg.Destroy()
          return
        if len(environmentProperties.narrative()) == 0:
          errorTxt = 'No narrative defined in environment ' + environmentProperties.name()
          dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK) 
          dlg.ShowModal()
          dlg.Destroy()
          return
    self.EndModal(TASK_BUTTONCOMMIT_ID)

  def parameters(self): 
    parameters = TaskParameters(self.theName,self.theShortCode,self.theObjective,self.isAssumption,self.theAuthor,self.theTags,self.theEnvironmentProperties)
    parameters.setId(self.theTaskId)
    return parameters
