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

class CodePage(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,-1)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    topSizer.Add(self.buildTextSizer('Code',(87,30),armid.QUOTATION_TEXTCODE_ID,'',True),0,wx.EXPAND)

    artBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
    topSizer.Add(artBoxSizer,0,wx.EXPAND)
    artBoxSizer.Add(self.buildTextSizer('Artifact Type',(87,30),armid.QUOTATION_TEXTARTIFACTTYPE_ID,'',True),1,wx.EXPAND)
    artBoxSizer.Add(self.buildTextSizer('Name',(87,30),armid.QUOTATION_TEXTARTIFACTNAME_ID,'',True),1,wx.EXPAND)

    topSizer.Add(self.buildMLTextSizer('Source',(87,30),armid.QUOTATION_TEXTSOURCE_ID),1,wx.EXPAND)
    topSizer.Add(self.buildCommitButtonSizer(armid.QUOTATION_BUTTONCOMMIT_ID,False),0,wx.ALIGN_CENTER)

    self.SetSizer(topSizer)

class QuotationNotebook(wx.Notebook):
  def __init__(self,parent):
    wx.Notebook.__init__(self,parent,armid.QUOTATION_NOTEBOOKQUOTATION_ID)
    p1 = CodePage(self)
    self.AddPage(p1,'Code')
