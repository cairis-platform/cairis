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
from MisuseCaseEnvironmentPanel import MisuseCaseEnvironmentPanel

__author__ = 'Shamal Faily'

class MisuseCasePanel(wx.Panel):
  def __init__(self,parent,dp):
    wx.Panel.__init__(self,parent,MISUSECASE_ID)
    self.dbProxy = dp
 
  def buildControls(self,isCreate = True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Name',(87,30),MISUSECASE_TEXTNAME_ID,isReadOnly=True),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Risk',(87,30),MISUSECASE_TEXTRISK_ID,isReadOnly=True),0,wx.EXPAND)
    thrSizer = wx.BoxSizer(wx.HORIZONTAL)

    self.environmentPanel = MisuseCaseEnvironmentPanel(self,self.dbProxy)
    mainSizer.Add(self.environmentPanel,1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildCommitButtonSizer(self,MISUSECASE_BUTTONCOMMIT_ID,isCreate),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

    self.nameCtrl = self.FindWindowById(MISUSECASE_TEXTNAME_ID)
    self.riskCtrl = self.FindWindowById(MISUSECASE_TEXTRISK_ID)

  def loadMisuseCase(self,mc):
    self.nameCtrl.SetValue(mc.name())
    self.riskCtrl.SetValue(mc.risk())
    self.environmentPanel.loadMisuseCase(mc)

  def loadRiskComponents(self,riskName,threatName,vulName):
    mcName = 'Exploit ' + riskName
    self.nameCtrl.SetValue(mcName)
    self.riskCtrl.SetValue(riskName)
    self.environmentPanel.loadRiskComponents(threatName,vulName)
