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
import WidgetFactory
from cairis.core.Borg import Borg

__author__ = 'Shamal Faily'

class SingleEnvironmentPanel(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,ENVIRONMENT_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.environmentName = ''
    self.environmentDescription = ''

  def buildControls(self):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Name',(87,30),ENVIRONMENT_TEXTNAME_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Short Code',(87,30),ENVIRONMENT_TEXTSHORTCODE_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildMLTextSizer(self,'Description',(87,30),ENVIRONMENT_TEXTDESCRIPTION_ID),1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildCommitButtonSizer(self,ENVIRONMENT_BUTTONCOMMIT_ID,True))
    self.SetSizer(mainSizer)


  def loadControls(self,environment,isReadOnly=False):
    nameCtrl = self.FindWindowById(ENVIRONMENT_TEXTNAME_ID)
    shortCode = self.FindWindowById(ENVIRONMENT_TEXTSHORTCODE_ID)
    valueCtrl = self.FindWindowById(ENVIRONMENT_TEXTDESCRIPTION_ID)
    nameCtrl.SetValue(environment.name())
    shortCodeCtrl.SetValue(environment.shortCode())
    valueCtrl.SetValue(environment.description())
