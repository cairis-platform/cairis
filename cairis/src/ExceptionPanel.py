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


#$URL$ $Id: ExceptionPanel.py 424 2011-02-25 21:29:47Z shaf $

import wx
import armid
import WidgetFactory
from Borg import Borg

class ExceptionPanel(wx.Panel):
  def __init__(self,parent,envName):
    wx.Panel.__init__(self,parent,armid.EXCEPTION_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theEnvironmentName = envName
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Name',(87,30),armid.EXCEPTION_TEXTNAME_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildRadioButtonSizer(self,'Type',(87,30),[(armid.EXCEPTION_RADIOGOAL_ID,'Goal'),(armid.EXCEPTION_RADIOREQUIREMENT_ID,'Requirement')]))
    goalList = self.dbProxy.environmentGoals(self.theEnvironmentName)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Values',(87,30),armid.EXCEPTION_COMBOGOALS_ID,goalList),0,wx.EXPAND)
    catList = ['Confidentiality Threat','Integrity Threat','Availability Threat','Accountability Threat','Anonymity Threat','Pseudonymity Threat','Unlinkability Threat','Unobservability Threat','Vulnerability','Duration','Frequency','Demands','Goal Support']
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Category',(87,30),armid.EXCEPTION_COMBOCATEGORY_ID,catList),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildMLTextSizer(self,'Definition',(87,30),armid.EXCEPTION_TEXTDEFINITION_ID),1,wx.EXPAND)
    self.SetSizer(mainSizer)

    wx.EVT_RADIOBUTTON(self,armid.EXCEPTION_RADIOGOAL_ID,self.onGoalSelected)
    wx.EVT_RADIOBUTTON(self,armid.EXCEPTION_RADIOREQUIREMENT_ID,self.onRequirementSelected)

  def onGoalSelected(self,evt):
    goalCtrl = self.FindWindowById(armid.EXCEPTION_COMBOGOALS_ID)
    goals = self.dbProxy.environmentGoals(self.theEnvironmentName)
    goalCtrl.SetItems(goals)
    goalCtrl.SetValue('')

  def onRequirementSelected(self,evt):
    goalCtrl = self.FindWindowById(armid.EXCEPTION_COMBOGOALS_ID)
    goals = self.dbProxy.getDimensionNames('requirement')
    goalCtrl.SetItems(goals)
    goalCtrl.SetValue('')

  def loadControls(self,stepEx):
    nameCtrl = self.FindWindowById(armid.EXCEPTION_TEXTNAME_ID)
    nameCtrl.SetValue(stepEx[0])

    goalCtrl = self.FindWindowById(armid.EXCEPTION_COMBOGOALS_ID)

    dimType = stepEx[1]
    if (dimType == 'goal'):
      typeCtrl = self.FindWindowById(armid.EXCEPTION_RADIOGOAL_ID)
      typeCtrl.SetValue(True)
    else:
      typeCtrl = self.FindWindowById(armid.EXCEPTION_RADIOREQUIREMENT_ID)
      typeCtrl.SetValue(True)
      goals = self.dbProxy.getDimensionNames('requirement')
      goalCtrl.SetItems(goals)

    dimName = stepEx[2]
    goalCtrl.SetValue(dimName)

    exCat = stepEx[3]
    catCtrl = self.FindWindowById(armid.EXCEPTION_COMBOCATEGORY_ID)
    catCtrl.SetValue(exCat)

    exDef = stepEx[4]
    defCtrl = self.FindWindowById(armid.EXCEPTION_TEXTDEFINITION_ID)
    defCtrl.SetValue(exDef)
