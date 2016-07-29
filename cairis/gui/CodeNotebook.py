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

class MLTextPage(wx.Panel):
  def __init__(self,parent,winId):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    narrativeBox = wx.StaticBox(self,-1)
    narrativeBoxSizer = wx.StaticBoxSizer(narrativeBox,wx.HORIZONTAL)
    topSizer.Add(narrativeBoxSizer,1,wx.EXPAND)
    self.narrativeCtrl = wx.TextCtrl(self,winId,'',style=wx.TE_MULTILINE)
    narrativeBoxSizer.Add(self.narrativeCtrl,1,wx.EXPAND)
    self.SetSizer(topSizer)

class SummaryPage(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,-1)
    topSizer = wx.BoxSizer(wx.VERTICAL)
    topSizer.Add(self.buildTextSizer('Name',(87,30),CODE_TEXTNAME_ID),0,wx.EXPAND)
    topSizer.Add(self.buildComboSizerList('Type',(87,30),CODE_COMBOTYPE_ID,['event','context']),0,wx.EXPAND)
    topSizer.Add(self.buildMLTextSizer('Description',(87,30),CODE_TEXTDESCRIPTION_ID),1,wx.EXPAND)
    topSizer.Add(self.buildCloseButtonSizer(),0,wx.EXPAND)
    self.SetSizer(topSizer)

class CodeNotebook(wx.Notebook):
  def __init__(self,parent):
    wx.Notebook.__init__(self,parent,-1)
    p1 = SummaryPage(self)
    p2 = MLTextPage(self,CODE_TEXTINCLUSIONCRITERIA_ID)
    p3 = MLTextPage(self,CODE_TEXTEXAMPLE_ID)
    self.AddPage(p1,'Summary')
    self.AddPage(p2,'Inclusion Criteria')
    self.AddPage(p3,'Example')
