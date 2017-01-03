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
import WidgetFactory
import TracePanel

__author__ = 'Shamal Faily'

class TraceDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,parameters.id(),parameters.label(),style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,275))
    if (parameters.__class__.__name__ == 'TraceDialogParameters'):
      self.theOriginalFromObject = parameters.fromObject()
      self.theOriginalFromId = parameters.fromId()
      self.theOriginalToObject = parameters.toObject()
      self.theOriginalToId = parameters.toId()
    else:
      self.theOriginalFromObject = -1
      self.theOriginalFromId = -1
      self.theOriginalToObject = -1
      self.theOriginalToId = -1
    self.theFromObject = -1
    self.theFromId = -1
    self.theToObject = -1
    self.theToId = -1
    self.panel = 0
    self.buildControls(parameters)
    self.theCommitVerb = 'Add'
    
  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = TracePanel.TracePanel(self)
    self.panel.buildControls(parameters.createFlag())
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,TRACE_BUTTONCOMMIT_ID,self.onCommit)

  def load(self,threat):
    self.panel.loadControls(threat)
    self.theCommitVerb = 'Edit'

  def onCommit(self,evt):
    self.theFromObject = self.panel.theFromObject
    self.theFromId = self.panel.theFromId
    self.theToObject = self.panel.theToObject
    self.theToId = self.panel.theToId
    self.theFromName = self.panel.theFromName
    self.theToName = self.panel.theToName
    self.EndModal(TRACE_BUTTONCOMMIT_ID)
