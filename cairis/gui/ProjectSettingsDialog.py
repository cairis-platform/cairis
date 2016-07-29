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
from ProjectSettingsPanel import ProjectSettingsPanel

__author__ = 'Shamal Faily'

class ProjectSettingsDialog(wx.Dialog):
  def __init__(self,parent,settingsDictionary,dictionary,contributors,revisions):
    wx.Dialog.__init__(self,parent,PROJECTSETTINGS_ID,'Project Settings',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME,size=(600,500))
    self.theId = -1
    self.panel = 0
    self.theProjectName = settingsDictionary['Project Name']
    self.theBackground = settingsDictionary['Project Background']
    self.theGoals = settingsDictionary['Project Goals']
    self.theScope = settingsDictionary['Project Scope']
    self.theRichPicture = settingsDictionary['Rich Picture']
    self.theDefinitions = dictionary
    self.theContributors = contributors
    self.theRevisions = revisions
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = ProjectSettingsPanel(self,self.theProjectName,self.theBackground,self.theGoals,self.theScope,self.theDefinitions,self.theContributors,self.theRevisions,self.theRichPicture)
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,PROJECTSETTINGS_BUTTONCOMMIT_ID,self.onCommit)

  def onCommit(self,evt):
    self.theProjectName = self.panel.name()
    self.theBackground = self.panel.background()
    self.theGoals = self.panel.goals()
    self.theScope = self.panel.scope()
    self.theDefinitions = self.panel.definitions()
    self.theContributors = self.panel.contributors()
    self.theRevisions = self.panel.revisions()
    self.theRichPicture = self.panel.richPicture()
    self.EndModal(PROJECTSETTINGS_BUTTONCOMMIT_ID)

  def name(self): return self.theProjectName
  def background(self): return self.theBackground
  def goals(self): return self.theGoals
  def scope(self): return self.theScope
  def definitions(self): return self.theDefinitions
  def contributors(self): return self.theContributors
  def revisions(self): return self.theRevisions
  def richPicture(self): return self.theRichPicture
