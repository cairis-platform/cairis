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
from Borg import Borg

class WeaknessTreatmentPanel(BasePanel):
  def __init__(self,parent,cvName):
    BasePanel.__init__(self,parent,armid.WEAKNESSTREATMENT_ID)
    self.theViewName = cvName
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theGoalIndicator = 0
    reqList = self.dbProxy.componentViewRequirements(cvName)
    assetList = []
    effValues = ['None','Low','Medium','High']
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(self.buildRadioButtonSizer('Type',(87,30),[(armid.WEAKNESSTREATMENT_RADIOGOAL_ID,'Goal'),(armid.WEAKNESSTREATMENT_RADIOREQUIREMENT_ID,'Requirement')]))
    mainSizer.Add(self.buildComboSizerList('',(87,30),armid.WEAKNESSTREATMENT_COMBOREQGOAL_ID,reqList),0,wx.EXPAND)
    mainSizer.Add(self.buildComboSizerList('Asset',(87,30),armid.WEAKNESSTREATMENT_COMBOASSET_ID,assetList),0,wx.EXPAND)
    mainSizer.Add(self.buildComboSizerList('Effectiveness',(87,30),armid.WEAKNESSTREATMENT_COMBOEFFECTIVENESS_ID,effValues),0,wx.EXPAND)
    mainSizer.Add(self.buildMLTextSizer('Rationale',(87,60),armid.WEAKNESSTREATMENT_TEXTRATIONALE_ID),1,wx.EXPAND)
    mainSizer.Add(self.buildCommitButtonSizer(armid.WEAKNESSTREATMENT_BUTTONCOMMIT_ID,False),0,wx.CENTER)
    self.SetSizer(mainSizer)
    reqCtrl = self.FindWindowById(armid.WEAKNESSTREATMENT_COMBOREQGOAL_ID)
    reqCtrl.Bind(wx.EVT_COMBOBOX,self.onRequirementChange)
    wx.EVT_RADIOBUTTON(self,armid.WEAKNESSTREATMENT_RADIOGOAL_ID,self.onGoalSelected)
    wx.EVT_RADIOBUTTON(self,armid.WEAKNESSTREATMENT_RADIOREQUIREMENT_ID,self.onRequirementSelected)
    reqRadioCtrl = self.FindWindowById(armid.WEAKNESSTREATMENT_RADIOREQUIREMENT_ID)
    reqRadioCtrl.SetValue(True)

  def onGoalSelected(self,evt):
    self.theGoalIndicator = 1
    rgCtrl = self.FindWindowById(armid.WEAKNESSTREATMENT_COMBOREQGOAL_ID)
    goals = self.dbProxy.componentViewGoals(self.theViewName)
    rgCtrl.SetItems(goals)
    rgCtrl.SetValue('')

  def onRequirementSelected(self,evt):
    self.theGoalIndicator = 0
    rgCtrl = self.FindWindowById(armid.WEAKNESSTREATMENT_COMBOREQGOAL_ID)
    reqs = self.dbProxy.componentViewRequirements(self.theViewName)
    rgCtrl.SetItems(reqs)
    rgCtrl.SetValue('')


  def loadControls(self,reqName,assetName,effValue,tRat):
    reqCtrl = self.FindWindowById(armid.WEAKNESSTREATMENT_COMBOREQGOAL_ID)
    reqCtrl.SetValue(reqName)
    assetCtrl = self.FindWindowById(armid.WEAKNESSTREATMENT_COMBOASSET_ID)
    assetCtrl.SetValue(assetName)
    effCtrl = self.FindWindowById(armid.WEAKNESSTREATMENT_COMBOEFFECTIVENESS_ID)
    effCtrl.SetValue(effValue)
    ratCtrl = self.FindWindowById(armid.WEAKNESSTREATMENT_TEXTRATIONALE_ID)
    ratCtrl.SetValue(tRat)

  def onRequirementChange(self,evt):
    reqCtrl = self.FindWindowById(armid.WEAKNESSTREATMENT_COMBOREQGOAL_ID)
    assetCtrl = self.FindWindowById(armid.WEAKNESSTREATMENT_COMBOASSET_ID)
    reqName = reqCtrl.GetValue()
    componentAssets = []
    if self.theGoalIndicator == 0:
      componentAssets = self.dbProxy.componentAssets(self.theViewName,reqName)
    else:
      componentAssets = self.dbProxy.componentGoalAssets(self.theViewName,reqName)
    assetList = []
    for caPair in componentAssets:
      assetList.append(caPair[0])
    assetCtrl.SetItems(assetList)
