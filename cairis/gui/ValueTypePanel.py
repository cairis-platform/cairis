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

__author__ = 'Shamal Faily'

class ValueTypePanel(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,VALUETYPE_ID)

  def buildControls(self,isCreate):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(self.buildTextSizer('Name',(87,30),VALUETYPE_TEXTNAME_ID),0,wx.EXPAND)
    mainSizer.Add(self.buildTextSizer('Score',(87,30),VALUETYPE_TEXTSCORE_ID),0,wx.EXPAND)
    mainSizer.Add(self.buildMLTextSizer('Description',(87,80),VALUETYPE_TEXTDESCRIPTION_ID),1,wx.EXPAND)
    mainSizer.Add(self.buildMLTextSizer('Rationale',(87,80),VALUETYPE_TEXTRATIONALE_ID),1,wx.EXPAND)
    mainSizer.Add(self.buildCommitButtonSizer(VALUETYPE_BUTTONCOMMIT_ID,isCreate),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

  def loadControls(self,objt):
    nameCtrl = self.FindWindowById(VALUETYPE_TEXTNAME_ID)
    scoreCtrl = self.FindWindowById(VALUETYPE_TEXTSCORE_ID)
    descCtrl = self.FindWindowById(VALUETYPE_TEXTDESCRIPTION_ID)
    ratCtrl = self.FindWindowById(VALUETYPE_TEXTRATIONALE_ID)
    nameCtrl.SetValue(objt.name())
    scoreCtrl.SetValue(objt.score())
    descCtrl.SetValue(objt.description())
    ratCtrl.SetValue(objt.rationale())
