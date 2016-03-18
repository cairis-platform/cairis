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
import os
from Borg import Borg
import ARM
from CodeNetworkPanel import CodeNetworkPanel

class CodeNetworkViewer(wx.Dialog):
  def __init__(self,parent,personaName,codeNet):
    wx.Dialog.__init__(self,parent,-1,'Code network',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(500,800))
    self.theParent = parent 
    self.panel = 0
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = CodeNetworkPanel(self,personaName,codeNet)
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
