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
from BasePanel import BasePanel
import Component
from Borg import Borg
from ComponentNotebook import ComponentNotebook

class ComponentPanel(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,armid.COMPONENT_ID)
    self.theComponentId = None
    b = Borg()
    self.dbProxy = b.dbProxy
    
  def buildControls(self,isCreate,isUpdateable=True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(self.buildTextSizer('Name',(87,30),armid.COMPONENT_TEXTNAME_ID),0,wx.EXPAND)

    nbBox = wx.StaticBox(self,-1)
    nbSizer = wx.StaticBoxSizer(nbBox,wx.VERTICAL)
    mainSizer.Add(nbSizer,1,wx.EXPAND)
    nbSizer.Add(ComponentNotebook(self),1,wx.EXPAND)

    mainSizer.Add(self.buildCommitButtonSizer(armid.COMPONENT_BUTTONCOMMIT_ID,isCreate),0,wx.CENTER)
    self.SetSizer(mainSizer)

  def loadControls(self,pattern,isReadOnly=False):
    self.thePatternId = pattern.id()
    nameCtrl = self.FindWindowById(armid.COMPONENT_TEXTNAME_ID)
    descCtrl = self.FindWindowById(armid.COMPONENT_TEXTDESCRIPTION_ID)
    ifCtrl = self.FindWindowById(armid.COMPONENT_LISTINTERFACES_ID)
    structCtrl = self.FindWindowById(armid.COMPONENT_LISTSTRUCTURE_ID)
    reqsCtrl = self.FindWindowById(armid.COMPONENT_LISTREQUIREMENTS_ID)

    nameCtrl.SetValue(pattern.name())
    descCtrl.SetValue(pattern.description())
    ifCtrl.load(pattern.interfaces())
    structCtrl.load(pattern.structure())
    reqsCtrl.load(pattern.requirements()) 
