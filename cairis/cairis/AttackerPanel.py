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
from AttackerEnvironmentPanel import AttackerEnvironmentPanel
from PersonalImageView import PersonalImageView

class AttackerPanel(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,armid.ATTACKER_ID)
    b = Borg()
    self.dbProxy = b.dbProxy

  def buildControls(self,isCreate,isUpdateable=True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    staticCtrlBox = wx.StaticBox(self)
    staticCtrlSizer = wx.StaticBoxSizer(staticCtrlBox,wx.HORIZONTAL)
    mainSizer.Add(staticCtrlSizer,1,wx.EXPAND)
    sumDetailsSizer = wx.BoxSizer(wx.VERTICAL)
    staticCtrlSizer.Add(sumDetailsSizer,1,wx.EXPAND)
    sumDetailsSizer.Add(self.buildTextSizer('Name',(87,30),armid.ATTACKER_TEXTNAME_ID),0,wx.EXPAND)
    sumDetailsSizer.Add(self.buildTagCtrlSizer((87,30),armid.ATTACKER_TAGS_ID),0,wx.EXPAND)
    sumDetailsSizer.Add(self.buildMLTextSizer('Description',(87,30),armid.ATTACKER_TEXTDESCRIPTION_ID),1,wx.EXPAND)
    iBox = wx.StaticBox(self,-1)
    iSizer = wx.StaticBoxSizer(iBox,wx.HORIZONTAL)
    staticCtrlSizer.Add(iSizer,1,wx.EXPAND)
    imagePanel = PersonalImageView(self,armid.ATTACKER_IMAGEATTACKERIMAGE_ID)
    iSizer.Add(imagePanel,1,wx.EXPAND)
    
    self.environmentPanel = AttackerEnvironmentPanel(self,self.dbProxy)
    mainSizer.Add(self.environmentPanel,1,wx.EXPAND)
    if (isUpdateable):
      mainSizer.Add(self.buildCommitButtonSizer(armid.ATTACKER_BUTTONCOMMIT_ID,isCreate),0,wx.CENTER)
    self.SetSizer(mainSizer)

  def loadControls(self,attacker):
    nameCtrl = self.FindWindowById(armid.ATTACKER_TEXTNAME_ID)
    tagsCtrl = self.FindWindowById(armid.ATTACKER_TAGS_ID)
    descriptionCtrl = self.FindWindowById(armid.ATTACKER_TEXTDESCRIPTION_ID)
    imageCtrl = self.FindWindowById(armid.ATTACKER_IMAGEATTACKERIMAGE_ID)
    environmentCtrl = self.FindWindowById(armid.ATTACKER_PANELENVIRONMENT_ID)

    nameCtrl.SetValue(attacker.name())
    tagsCtrl.set(attacker.tags())
    descriptionCtrl.SetValue(attacker.description())
    imageCtrl.loadImage(attacker.image())

    environmentCtrl.loadControls(attacker)
    self.theAttackerId = attacker.id()
