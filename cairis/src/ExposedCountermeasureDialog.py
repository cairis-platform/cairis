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
from ExposedCountermeasurePanel import ExposedCountermeasurePanel

class ExposedCountermeasureDialog(wx.Dialog):
  def __init__(self,parent,vulCms = []):
    wx.Dialog.__init__(self,parent,armid.EXPOSEDCOUNTERMEASURE_ID,'Exposed countermeasures',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,500))
    
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = ExposedCountermeasurePanel(self,vulCms)
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizerAndFit(mainSizer)
    wx.EVT_BUTTON(self,armid.EXPOSEDCOUNTERMEASURE_BUTTONCOMMIT_ID,self.onCommit)


  def onCommit(self,evt):
    self.EndModal(armid.EXPOSEDCOUNTERMEASURE_BUTTONCOMMIT_ID)

  def countermeasureEffectiveness(self): return self.panel.countermeasureEffectiveness()
