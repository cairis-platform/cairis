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
from ResponseParameters import ResponseParameters
from ResponsePanel import ResponsePanel

class ResponseDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,parameters.id(),parameters.label(),style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,600))

    self.theResponseId = -1
    self.panel = 0
    self.buildControls(parameters)

  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = ResponsePanel(self,parameters.responseType(),parameters.panel())
    self.panel.buildControls(parameters.createFlag())
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.RESPONSE_BUTTONCOMMIT_ID,self.onCommit)


  def load(self,response):
    self.theResponseId = response.id()
    self.panel.loadControls(response)

  def onCommit(self,evt):
    if (self.panel.commit() != -1):
      self.EndModal(armid.RESPONSE_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = self.panel.parameters()
    parameters.setId(self.theResponseId)
    return parameters
