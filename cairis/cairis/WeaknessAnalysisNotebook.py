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
from Borg import Borg
from WeaknessTargetListCtrl import WeaknessTargetListCtrl

class WeaknessTargetPage(wx.Panel):
  def __init__(self,parent,winId,cvName,targets):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)
    asBox = wx.StaticBox(self,-1)
    asBoxSizer = wx.StaticBoxSizer(asBox,wx.HORIZONTAL)
    topSizer.Add(asBoxSizer,1,wx.EXPAND)
    self.targetList = WeaknessTargetListCtrl(self,winId,cvName)
    self.targetList.load(targets)
    asBoxSizer.Add(self.targetList,1,wx.EXPAND)
    self.SetSizer(topSizer)

class WeaknessAnalysisNotebook(wx.Notebook):
  def __init__(self,parent,cvName,envName):
    wx.Notebook.__init__(self,parent,armid.WEAKNESSANALYSIS_NOTEBOOKWEAKNESS_ID)
    b = Borg()
    thrTargets,vulTargets = b.dbProxy.componentViewWeaknesses(cvName,envName)
    p1 = WeaknessTargetPage(self,armid.WEAKNESSANALYSIS_LISTTHREATS_ID,cvName,thrTargets)
    p2 = WeaknessTargetPage(self,armid.WEAKNESSANALYSIS_LISTVULNERABILITIES_ID,cvName,vulTargets)
    self.AddPage(p1,'Threats')
    self.AddPage(p2,'Vulnerabilities')
