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
from cairis.core.Borg import Borg
from BasePanel import BasePanel
from cairis.core.UseCase import UseCase
from DimensionListCtrl import DimensionListCtrl
from UseCaseEnvironmentPanel import UseCaseEnvironmentPanel

__author__ = 'Shamal Faily'

class UseCasePanel(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,USECASE_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    mainSizer = wx.BoxSizer(wx.VERTICAL)

    summBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(summBoxSizer,0,wx.EXPAND)
    summBoxSizer.Add(self.buildTextSizer('Name',(87,30),USECASE_TEXTNAME_ID),1,wx.EXPAND)
    summBoxSizer.Add(self.buildTextSizer('Code',(87,30),USECASE_TEXTSHORTCODE_ID),1,wx.EXPAND)
    mainSizer.Add(self.buildTagCtrlSizer((87,30),USECASE_TAGS_ID),0,wx.EXPAND)
    mainSizer.Add(self.buildTextSizer('Author/s',(87,30),USECASE_TEXTAUTHOR_ID),0,wx.EXPAND)

    objtBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(objtBoxSizer,0,wx.EXPAND)
    objtBoxSizer.Add(self.buildMLTextSizer('Description',(87,60),USECASE_TEXTDESCRIPTION_ID),1,wx.EXPAND)

    roleBox = wx.StaticBox(self)
    roleSizer = wx.StaticBoxSizer(roleBox,wx.HORIZONTAL)
    self.roleList = DimensionListCtrl(self,USECASE_LISTACTORS_ID,wx.DefaultSize,'Actor','role',self.dbProxy)
    roleSizer.Add(self.roleList,1,wx.EXPAND)
    objtBoxSizer.Add(roleSizer,1,wx.EXPAND)

    self.environmentPanel = UseCaseEnvironmentPanel(self)
    mainSizer.Add(self.environmentPanel,1,wx.EXPAND)
    self.SetSizer(mainSizer)


  def loadControls(self,uc,isReadOnly=False):
    nameCtrl = self.FindWindowById(USECASE_TEXTNAME_ID)
    nameCtrl.SetValue(uc.name())
    tagsCtrl = self.FindWindowById(USECASE_TAGS_ID)
    tagsCtrl.set(uc.tags())
    authCtrl = self.FindWindowById(USECASE_TEXTAUTHOR_ID)
    authCtrl.SetValue(uc.author())
    codeCtrl = self.FindWindowById(USECASE_TEXTSHORTCODE_ID)
    codeCtrl.SetValue(uc.code())
    descCtrl = self.FindWindowById(USECASE_TEXTDESCRIPTION_ID)
    descCtrl.SetValue(uc.description())
    roleCtrl = self.FindWindowById(USECASE_LISTACTORS_ID)
    roleCtrl.load(uc.actors())
    self.environmentPanel.loadControls(uc)
