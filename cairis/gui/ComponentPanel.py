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
from BasePanel import BasePanel
import cairis.core.Component
from cairis.core.Borg import Borg
from ComponentNotebook import ComponentNotebook

__author__ = 'Shamal Faily'

class ComponentPanel(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,COMPONENT_ID)
    self.theComponentId = None
    b = Borg()
    self.dbProxy = b.dbProxy
    
  def buildControls(self):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(self.buildTextSizer('Name',(87,30),COMPONENT_TEXTNAME_ID),0,wx.EXPAND)

    nbBox = wx.StaticBox(self,-1)
    nbSizer = wx.StaticBoxSizer(nbBox,wx.VERTICAL)
    mainSizer.Add(nbSizer,1,wx.EXPAND)
    nbSizer.Add(ComponentNotebook(self),1,wx.EXPAND)

    mainSizer.Add(self.buildCommitButtonSizer(COMPONENT_BUTTONCOMMIT_ID,True),0,wx.CENTER)
    self.SetSizer(mainSizer)

  def loadControls(self,component,isReadOnly=False):
    self.theComponentId = component.id()
    nameCtrl = self.FindWindowById(COMPONENT_TEXTNAME_ID)
    descCtrl = self.FindWindowById(COMPONENT_TEXTDESCRIPTION_ID)
    ifCtrl = self.FindWindowById(COMPONENT_LISTINTERFACES_ID)
    structCtrl = self.FindWindowById(COMPONENT_LISTSTRUCTURE_ID)
    reqsCtrl = self.FindWindowById(COMPONENT_LISTREQUIREMENTS_ID)
    goalsCtrl = self.FindWindowById(COMPONENT_LISTGOALS_ID)

    nameCtrl.SetValue(component.name())
    descCtrl.SetValue(component.description())
    ifCtrl.load(component.interfaces())
    structCtrl.load(component.structure())
    reqsCtrl.load(component.requirements()) 
    goalsCtrl.load(component.goals()) 
