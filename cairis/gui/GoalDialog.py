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
from cairis.core.ARM import *
from cairis.core.Borg import Borg
from GoalPanel import GoalPanel
from cairis.core.GoalParameters import GoalParameters
import DialogClassParameters

class GoalDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,parameters.id(),parameters.label(),style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(600,400))
    self.theGoalId = -1
    self.theGoalName = ''
    self.theTags = []
    self.theGoalOriginator = ''
    self.theEnvironmentProperties = []
    self.panel = 0
    self.buildControls(parameters)
    self.commitVerb = 'Add'
    
  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = GoalPanel(self)
    self.panel.buildControls(parameters.createFlag())
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,GOAL_BUTTONCOMMIT_ID,self.onCommit)

  def load(self,goal):
    self.theGoalId = goal.id()
    self.panel.loadControls(goal)
    self.commitVerb = 'Edit'

  def onCommit(self,evt):
    nameCtrl = self.FindWindowById(GOAL_TEXTNAME_ID)
    tagsCtrl = self.FindWindowById(GOAL_TAGS_ID)
    origCtrl = self.FindWindowById(GOAL_TEXTORIGINATOR_ID)
    environmentCtrl = self.FindWindowById(GOAL_PANELENVIRONMENT_ID)

    self.theGoalName = nameCtrl.GetValue()
    self.theTags = tagsCtrl.tags()
    self.theGoalOriginator = origCtrl.GetValue()

    if (self.commitVerb == 'Add'):
      b = Borg()
      try:
        b.dbProxy.nameCheck(self.theGoalName,'goal')
      except ARMException,errorText:
        dlg = wx.MessageDialog(self,str(errorText),'Add goal',wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
        return
    self.theEnvironmentProperties = environmentCtrl.environmentProperties()

    commitLabel = self.commitVerb + ' goal'
    if len(self.theGoalName) == 0:
      dlg = wx.MessageDialog(self,'Goal name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theGoalOriginator) == 0:
      dlg = wx.MessageDialog(self,'Goal originator cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theEnvironmentProperties) == 0):
      dlg = wx.MessageDialog(self,'No environments have been associated with this goal',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      for environmentProperties in self.theEnvironmentProperties:
        if len(environmentProperties.definition()) == 0:
          errorTxt = 'No definition associated with environment ' + environmentProperties.name()
          dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK)
          dlg.ShowModal()
          dlg.Destroy()
          return
        if len(environmentProperties.category()) == 0:
          errorTxt = 'No category associated with environment ' + environmentProperties.name()
          dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK)
          dlg.ShowModal()
          dlg.Destroy()
          return
        if len(environmentProperties.priority()) == 0:
          errorTxt = 'No priority associated with environment ' + environmentProperties.name()
          dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK)
          dlg.ShowModal()
          dlg.Destroy()
          return
        if len(environmentProperties.fitCriterion()) == 0:
          errorTxt = 'No fit criterion associated with environment ' + environmentProperties.name()
          dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK)
          dlg.ShowModal()
          dlg.Destroy()
          return
        if len(environmentProperties.issue()) == 0:
          errorTxt = 'No issues associated with environment ' + environmentProperties.name()
          dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK)
          dlg.ShowModal()
          dlg.Destroy()
          return
      self.EndModal(GOAL_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = GoalParameters(self.theGoalName,self.theGoalOriginator,self.theTags,self.theEnvironmentProperties)
    parameters.setId(self.theGoalId)
    return parameters
