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
from SecurityPatternPanel import SecurityPatternPanel
from cairis.core.SecurityPatternParameters import SecurityPatternParameters
import DialogClassParameters

__author__ = 'Shamal Faily'

class SecurityPatternDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,parameters.id(),parameters.label(),style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,500))
    self.thePatternName = ''
    self.thePatternContext = ''
    self.thePatternProblem = ''
    self.thePatternSolution = ''
    self.theConcernAssociations = []
    self.theRequirements = []
    self.thePatternId = -1
    self.panel = 0
    self.buildControls(parameters)
    self.commitVerb = 'Add'
    
  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = SecurityPatternPanel(self)
    self.panel.buildControls(parameters.createFlag())
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,SECURITYPATTERN_BUTTONCOMMIT_ID,self.onCommit)

  def load(self,pattern):
    self.thePatternId = pattern.id()
    self.panel.loadControls(pattern)
    self.commitVerb = 'Edit'

  def onCommit(self,evt):
    commitLabel = self.commitVerb + ' security pattern'
    nameCtrl = self.FindWindowById(SECURITYPATTERN_TEXTNAME_ID)
    contextCtrl = self.FindWindowById(SECURITYPATTERN_TEXTCONTEXT_ID)
    problemCtrl = self.FindWindowById(SECURITYPATTERN_TEXTPROBLEM_ID)
    solutionCtrl = self.FindWindowById(SECURITYPATTERN_TEXTSOLUTION_ID)
    concernsCtrl = self.FindWindowById(SECURITYPATTERN_LISTPATTERNSTRUCTURE_ID)
    reqsCtrl = self.FindWindowById(SECURITYPATTERN_LISTREQUIREMENTS_ID)
    self.thePatternName = nameCtrl.GetValue()
    self.thePatternContext = contextCtrl.GetValue()
    self.thePatternProblem = problemCtrl.GetValue()
    self.thePatternSolution = solutionCtrl.GetValue()
    self.theConcernAssociations = concernsCtrl.associations()
    self.theRequirements = reqsCtrl.requirements()

    if len(self.thePatternName) == 0:
      dlg = wx.MessageDialog(self,'Pattern name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.thePatternContext) == 0:
      dlg = wx.MessageDialog(self,'Context cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.thePatternProblem) == 0:
      dlg = wx.MessageDialog(self,'Problem cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.thePatternSolution) == 0):
      dlg = wx.MessageDialog(self,'Solution cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(SECURITYPATTERN_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = SecurityPatternParameters(self.thePatternName,self.thePatternContext,self.thePatternProblem,self.thePatternSolution,self.theRequirements,self.theConcernAssociations)
    parameters.setId(self.thePatternId)
    return parameters
