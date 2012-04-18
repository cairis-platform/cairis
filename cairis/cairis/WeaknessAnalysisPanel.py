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
import Asset
from WeaknessAnalysisNotebook import WeaknessAnalysisNotebook

class WeaknessAnalysisPanel(BasePanel):
  def __init__(self,parent,cvName):
    BasePanel.__init__(self,parent,armid.WEAKNESSANALYSIS_ID)
    self.theAssetId = None
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    nbBox = wx.StaticBox(self,-1)
    nbSizer = wx.StaticBoxSizer(nbBox,wx.VERTICAL)
    mainSizer.Add(nbSizer,1,wx.EXPAND)
    nbSizer.Add(WeaknessAnalysisNotebook(self,cvName),1,wx.EXPAND)

    buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
    applyButton = wx.Button(self,armid.WEAKNESSANALYSIS_BUTTONCOMMIT_ID,"Apply")
    buttonSizer.Add(applyButton)
    closeButton = wx.Button(self,wx.ID_CANCEL,"Cancel")
    buttonSizer.Add(closeButton)
    mainSizer.Add(buttonSizer,0,wx.CENTER)

    self.SetSizer(mainSizer)
