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
from ProjectSettingsNotebook import ProjectSettingsNotebook

__author__ = 'Shamal Faily'

class ProjectSettingsPanel(wx.Panel):
  def __init__(self,parent,projName,background,goals,scope,definitions,contributors,revisions,richPicture):
    wx.Panel.__init__(self,parent,PROJECTSETTINGS_PANELSETTINGS_ID)
    mainSizer = wx.BoxSizer(wx.VERTICAL)

    nbBox = wx.StaticBox(self,-1)
    nbSizer = wx.StaticBoxSizer(nbBox,wx.HORIZONTAL)
    mainSizer.Add(nbSizer,1,wx.EXPAND)
    self.notebook = ProjectSettingsNotebook(self)
    nbSizer.Add(self.notebook,1,wx.EXPAND)

    self.nameCtrl = self.notebook.FindWindowById(PROJECTSETTINGS_TEXTPROJECTNAME_ID)
    self.nameCtrl.SetValue(projName)
    self.backgroundCtrl = self.notebook.FindWindowById(PROJECTSETTINGS_TEXTBACKGROUND_ID)
    self.backgroundCtrl.SetValue(background)
    self.goalsCtrl = self.notebook.FindWindowById(PROJECTSETTINGS_TEXTGOALS_ID)
    self.goalsCtrl.SetValue(goals)
    self.scopeCtrl = self.notebook.FindWindowById(PROJECTSETTINGS_TEXTSCOPE_ID)
    self.scopeCtrl.SetValue(scope)
    self.definitionCtrl = self.notebook.FindWindowById(PROJECTSETTINGS_LISTDICTIONARY_ID)
    self.definitionCtrl.load(definitions)
    self.contributorsCtrl = self.notebook.FindWindowById(PROJECTSETTINGS_LISTCONTRIBUTORS_ID)
    self.contributorsCtrl.load(contributors)
    self.revisionsCtrl = self.notebook.FindWindowById(PROJECTSETTINGS_LISTREVISIONS_ID)
    self.revisionsCtrl.load(revisions)
    self.richPictureCtrl = self.notebook.FindWindowById(PROJECTSETTINGS_IMAGERICHPICTURE_ID)
    self.richPictureCtrl.loadImage(richPicture)

    buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(buttonSizer,0,wx.ALIGN_CENTER)

    buttonSizer.Add(wx.Button(self,PROJECTSETTINGS_BUTTONCOMMIT_ID,'Update'))
    buttonSizer.Add(wx.Button(self,wx.ID_CANCEL,'Cancel'))

    self.SetSizer(mainSizer)

  def name(self): return self.nameCtrl.GetValue()
  def background(self): return self.backgroundCtrl.GetValue()
  def goals(self): return self.goalsCtrl.GetValue()
  def scope(self): return self.scopeCtrl.GetValue()
  def definitions(self): return self.definitionCtrl.dimensions()
  def contributors(self): return self.contributorsCtrl.dimensions()
  def revisions(self): return self.revisionsCtrl.dimensions()
  def richPicture(self): return self.richPictureCtrl.personaImage()
