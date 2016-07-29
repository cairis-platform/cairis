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
from GenerateDocumentationPanel import GenerateDocumentationPanel

__author__ = 'Shamal Faily'

class GenerateDocumentationDialog(wx.Dialog):
  def __init__(self,parent):
    wx.Dialog.__init__(self,parent,GENDOCDIALOG_ID,'Generate documentation',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX,size=(250,700))
    self.theId = -1
    self.panel = 0
    self.theDocumentType = 'Requirements'
    self.theSectionFlags = []
    self.theTypeFlags = []
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = GenerateDocumentationPanel(self)
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,GENDOCPANEL_BUTTONGENERATE_ID,self.onGenerate)

  def onGenerate(self,evt):
    self.EndModal(GENDOCPANEL_BUTTONGENERATE_ID)

  def documentType(self): return self.panel.documentType()
  def sectionFlags(self): return self.panel.sectionFlags()
  def typeFlags(self): return self.panel.typeFlags()
