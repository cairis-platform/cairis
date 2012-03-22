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
from Borg import Borg
from EnvironmentNotebook import EnvironmentNotebook

class EnvironmentPanel(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,armid.ENVIRONMENT_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.environmentName = ''
    self.environmentDescription = ''

  def buildControls(self,isCreate,isUpdateable=True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(self.buildTextSizer('Name',(87,30),armid.ENVIRONMENT_TEXTNAME_ID),0,wx.EXPAND)
    self.envNotebook = EnvironmentNotebook(self,self.dbProxy)
    mainSizer.Add(self.envNotebook,1,wx.EXPAND)
    mainSizer.Add(self.buildCommitButtonSizer(armid.ENVIRONMENT_BUTTONCOMMIT_ID,isCreate),0,wx.CENTER)
    self.SetSizer(mainSizer)


  def loadControls(self,environment):
    nameCtrl = self.FindWindowById(armid.ENVIRONMENT_TEXTNAME_ID)
    shortCodeCtrl = self.envNotebook.FindWindowById(armid.ENVIRONMENT_TEXTSHORTCODE_ID)
    valueCtrl = self.envNotebook.FindWindowById(armid.ENVIRONMENT_TEXTDESCRIPTION_ID)
    environmentCtrl = self.envNotebook.FindWindowById(armid.ENVIRONMENT_PANELENVIRONMENTPROPERTIES_ID)
    tensionCtrl = self.envNotebook.FindWindowById(armid.ENVIRONMENT_GRIDVALUETENSIONS_ID)
    nameCtrl.SetValue(environment.name())
    shortCodeCtrl.SetValue(environment.shortCode())
    valueCtrl.SetValue(environment.description())
    environmentCtrl.load(environment)
    tensionCtrl.setTable(environment.tensions())
