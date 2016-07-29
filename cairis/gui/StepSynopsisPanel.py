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

class StepSynopsisPanel(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,STEPSYNOPSIS_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Synopsis',(87,30),STEPSYNOPSIS_TEXTSYNOPSIS_ID),0,wx.EXPAND)
    actorSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(actorSizer,0,wx.EXPAND)
    actorSizer.Add(WidgetFactory.buildComboSizerList(self,'Actor Type',(87,30),STEPSYNOPSIS_COMBOACTORTYPE_ID,['asset','role']),1,wx.EXPAND)
    actorSizer.Add(WidgetFactory.buildComboSizerList(self,'Actor',(87,30),STEPSYNOPSIS_COMBOACTORNAME_ID,['']),1,wx.EXPAND)
    mainSizer.Add(wx.StaticText(self,-1,''),1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildCommitButtonSizer(self,STEPSYNOPSIS_BUTTONCOMMIT_ID,True),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)
    wx.EVT_COMBOBOX(self,STEPSYNOPSIS_COMBOACTORTYPE_ID,self.onActorType)


  def load(self,stepSyn,stepActor,stepActorType):
    synCtrl = self.FindWindowById(STEPSYNOPSIS_TEXTSYNOPSIS_ID)
    actorTypeCtrl = self.FindWindowById(STEPSYNOPSIS_COMBOACTORTYPE_ID)
    actorCtrl = self.FindWindowById(STEPSYNOPSIS_COMBOACTORNAME_ID)
    synCtrl.SetValue(stepSyn)
    actorTypeCtrl.SetValue(stepActorType)
    if stepActor != '':
      self.setActorNames(stepActorType)
    actorCtrl.SetValue(stepActor)

  def onActorType(self,evt):
    self.setActorNames(evt.GetString())

  def setActorNames(self,actorType):
    aNames = self.dbProxy.getDimensionNames(actorType)
    actorCtrl = self.FindWindowById(STEPSYNOPSIS_COMBOACTORNAME_ID)
    actorCtrl.SetItems(aNames)
    actorCtrl.SetValue('')
