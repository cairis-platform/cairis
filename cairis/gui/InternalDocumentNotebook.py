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
from CodingTextCtrl import CodingTextCtrl

class ContentPage(wx.Panel):
  def __init__(self,parent,winId):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    contentBox = wx.StaticBox(self,-1)
    contentBoxSizer = wx.StaticBoxSizer(contentBox,wx.HORIZONTAL)
    topSizer.Add(contentBoxSizer,1,wx.EXPAND)
    self.contentCtrl = CodingTextCtrl(self,winId)
    contentBoxSizer.Add(self.contentCtrl,1,wx.EXPAND)
    self.SetSizer(topSizer)

class SummaryPage(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,-1)
    topSizer = wx.BoxSizer(wx.VERTICAL)
    topSizer.Add(self.buildTextSizer('Name',(87,30),INTERNALDOCUMENT_TEXTNAME_ID),0,wx.EXPAND)
    topSizer.Add(self.buildMLTextSizer('Description',(87,30),INTERNALDOCUMENT_TEXTDESCRIPTION_ID),1,wx.EXPAND)
    self.SetSizer(topSizer)

class InternalDocumentNotebook(wx.Notebook):
  def __init__(self,parent):
    wx.Notebook.__init__(self,parent,-1)
    p1 = SummaryPage(self)
    p2 = ContentPage(self,INTERNALDOCUMENT_TEXTCONTENT_ID)
    self.AddPage(p1,'Summary')
    self.AddPage(p2,'Content')
