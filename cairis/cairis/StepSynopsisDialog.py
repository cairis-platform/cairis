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
import WidgetFactory
import ARM
from Borg import Borg
from StepSynopsisPanel import StepSynopsisPanel

class StepSynopsisDialog(wx.Dialog):
  def __init__(self,parent,stepSyn,stepActor,stepActorType):
    wx.Dialog.__init__(self,parent,-1,'Edit Step Synopsis',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX,size=(475,150))
    self.theSynopsis = ''
    self.theActorType = ''
    self.theActor = ''
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = StepSynopsisPanel(self)
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.STEPSYNOPSIS_BUTTONCOMMIT_ID,self.onCommit)

    if (self.theSynopsis == ''):
      self.SetLabel = 'Create Step Synopsis'
    self.panel.load(stepSyn,stepActor,stepActorType)
   

  def onCommit(self,evt):
    synCtrl = self.FindWindowById(armid.STEPSYNOPSIS_TEXTSYNOPSIS_ID)
    atCtrl = self.FindWindowById(armid.STEPSYNOPSIS_COMBOACTORTYPE_ID)
    actorCtrl = self.FindWindowById(armid.STEPSYNOPSIS_COMBOACTORNAME_ID)

    self.theSynopsis = synCtrl.GetValue()
    self.theActorType = atCtrl.GetValue()
    self.theActor = actorCtrl.GetValue()

    self.EndModal(armid.STEPSYNOPSIS_BUTTONCOMMIT_ID)

  def synopsis(self):
    return self.theSynopsis

  def actor(self):
    return self.theActor

  def actorType(self):
    return self.theActorType
