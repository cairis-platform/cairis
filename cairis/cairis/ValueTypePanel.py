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

class ValueTypePanel(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,armid.ROLE_ID)

  def buildControls(self,isCreate):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Name',(87,30),armid.VALUETYPE_TEXTNAME_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Score',(87,30),armid.VALUETYPE_TEXTSCORE_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildMLTextSizer(self,'Description',(87,80),armid.VALUETYPE_TEXTDESCRIPTION_ID),1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildMLTextSizer(self,'Rationale',(87,80),armid.VALUETYPE_TEXTRATIONALE_ID),1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildCommitButtonSizer(self,armid.VALUETYPE_BUTTONCOMMIT_ID,isCreate),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

  def loadControls(self,objt):
    nameCtrl = self.FindWindowById(armid.VALUETYPE_TEXTNAME_ID)
    scoreCtrl = self.FindWindowById(armid.VALUETYPE_TEXTSCORE_ID)
    descCtrl = self.FindWindowById(armid.VALUETYPE_TEXTDESCRIPTION_ID)
    ratCtrl = self.FindWindowById(armid.VALUETYPE_TEXTRATIONALE_ID)
    nameCtrl.SetValue(objt.name())
    scoreCtrl.SetValue(objt.score())
    descCtrl.SetValue(objt.description())
    ratCtrl.SetValue(objt.rationale())
