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
from cairis.core.Borg import Borg

__author__ = 'Shamal Faily'

class ReferenceSynopsisPanel(BasePanel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,REFERENCESYNOPSIS_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(self.buildTextSizer('Reference',(87,30),REFERENCESYNOPSIS_TEXTREFNAME_ID),0,wx.EXPAND)
    mainSizer.Add(self.buildTextSizer('Synopsis',(87,30),REFERENCESYNOPSIS_TEXTSYNOPSIS_ID),0,wx.EXPAND)
    dimTypes = self.dbProxy.getDimensionNames('trace_dimension')
    mainSizer.Add(self.buildComboSizerList('Dimension',(87,30),REFERENCESYNOPSIS_COMBODIMENSION_ID,dimTypes),0,wx.EXPAND)

    actorSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(actorSizer,0,wx.EXPAND)
    actorSizer.Add(self.buildComboSizerList('Actor Type',(87,30),REFERENCESYNOPSIS_COMBOACTORTYPE_ID,['asset','persona','component']),1,wx.EXPAND)
    actorSizer.Add(self.buildComboSizerList('Actor',(87,30),REFERENCESYNOPSIS_COMBOACTORNAME_ID,['']),1,wx.EXPAND)
    mainSizer.Add(wx.StaticText(self,-1,''),1,wx.EXPAND)
    mainSizer.Add(self.buildCommitButtonSizer(REFERENCESYNOPSIS_BUTTONCOMMIT_ID,True),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)
    wx.EVT_COMBOBOX(self,REFERENCESYNOPSIS_COMBOACTORTYPE_ID,self.onActorType)


  def load(self,refsyn,charDetails = None):
    refCtrl = self.FindWindowById(REFERENCESYNOPSIS_TEXTREFNAME_ID)
    synCtrl = self.FindWindowById(REFERENCESYNOPSIS_TEXTSYNOPSIS_ID)
    dimCtrl = self.FindWindowById(REFERENCESYNOPSIS_COMBODIMENSION_ID)
    actorTypeCtrl = self.FindWindowById(REFERENCESYNOPSIS_COMBOACTORTYPE_ID)
    actorCtrl = self.FindWindowById(REFERENCESYNOPSIS_COMBOACTORNAME_ID)
    refCtrl.SetValue(refsyn.reference())
    synCtrl.SetValue(refsyn.synopsis())
    dimCtrl.SetValue(refsyn.dimension())
    actorType = refsyn.actorType()
    actorTypeCtrl.SetValue(actorType)
    if actorType != '':
      self.setActorNames(actorType)
    actorCtrl.SetValue(refsyn.actor())
    refCtrl.Disable()

    if charDetails != None:
      charType = charDetails[0]
      if charType == 'persona':
        actorTypeCtrl.Disable()
        actorCtrl.Disable()

  def onActorType(self,evt):
    self.setActorNames(evt.GetString())

  def setActorNames(self,actorType):
    aNames = self.dbProxy.getDimensionNames(actorType)
    actorCtrl = self.FindWindowById(REFERENCESYNOPSIS_COMBOACTORNAME_ID)
    actorCtrl.SetItems(aNames)
