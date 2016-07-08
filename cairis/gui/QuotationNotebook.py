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

class CodePage(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,-1)
    topSizer = wx.BoxSizer(wx.VERTICAL)
    topSizer.Add(self.buildTextSizer('Code',(87,30),QUOTATION_TEXTCODE_ID,'',True),0,wx.EXPAND)
    artBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
    topSizer.Add(artBoxSizer,0,wx.EXPAND)
    artBoxSizer.Add(self.buildTextSizer('Artifact Type',(87,30),QUOTATION_TEXTARTIFACTTYPE_ID,'',True),1,wx.EXPAND)
    artBoxSizer.Add(self.buildTextSizer('Name',(87,30),QUOTATION_TEXTARTIFACTNAME_ID,'',True),1,wx.EXPAND)
    topSizer.Add(self.buildMLTextSizer('Source',(87,30),QUOTATION_TEXTSOURCE_ID),1,wx.EXPAND)
    self.SetSizer(topSizer)

class SynopsisPage(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,-1)
    topSizer = wx.BoxSizer(wx.VERTICAL)
    topSizer.Add(self.buildTextSizer('Label',(87,30),QUOTATION_TEXTLABEL_ID),0,wx.EXPAND)
    topSizer.Add(self.buildMLTextSizer('Synopsis',(87,30),QUOTATION_TEXTSYNOPSIS_ID),1,wx.EXPAND)
    self.SetSizer(topSizer)

class QuotationNotebook(wx.Notebook):
  def __init__(self,parent):
    wx.Notebook.__init__(self,parent,QUOTATION_NOTEBOOKQUOTATION_ID)
    p1 = CodePage(self)
    p2 = SynopsisPage(self)
    self.AddPage(p1,'Code')
    self.AddPage(p2,'Synopsis')
