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
from StepPanel import StepPanel
from UseCaseTextCtrl import UseCaseTextCtrl


class TextPage(wx.Panel):
  def __init__(self,parent,winId):
    wx.Panel.__init__(self,parent,-1)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    textBox = wx.StaticBox(self,-1)
    textBoxSizer = wx.StaticBoxSizer(textBox,wx.HORIZONTAL)
    topSizer.Add(textBoxSizer,1,wx.EXPAND)
    self.textCtrl = UseCaseTextCtrl(self,winId)
    textBoxSizer.Add(self.textCtrl,1,wx.EXPAND)
    self.SetSizer(topSizer)

class StepPage(wx.Panel):
  def __init__(self,parent,envName):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    sBox = wx.StaticBox(self,-1)
    sSizer = wx.StaticBoxSizer(sBox,wx.HORIZONTAL)
    topSizer.Add(sSizer,1,wx.EXPAND)
    sSizer.Add(StepPanel(self,envName),1,wx.EXPAND)
    self.SetSizer(topSizer)


class UseCaseEnvironmentNotebook(wx.Notebook):
  def __init__(self,parent,envName):
    wx.Notebook.__init__(self,parent,USECASE_NOTEBOOKENVIRONMENT_ID)
    p1 = TextPage(self,USECASE_TEXTPRECONDITION_ID)
    p2 = StepPage(self,envName)
    p3 = TextPage(self,USECASE_TEXTPOSTCONDITION_ID)
    self.AddPage(p1,'Pre-Conditions')
    self.AddPage(p2,'Flow')
    self.AddPage(p3,'Post-Conditions')
