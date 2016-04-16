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

class RequirementsDocumentationPanel(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,REQDOCPANEL_ID)
    checkSizer = wx.BoxSizer(wx.VERTICAL)

    self.projectPurposeCheck = wx.CheckBox(self,REQDOCPANEL_CHECKPROJECTPURPOSE_ID,'Project Purpose')
    self.projectPurposeCheck.SetValue(True)
    checkSizer.Add(self.projectPurposeCheck,0,wx.EXPAND)

    self.environmentsCheck = wx.CheckBox(self,REQDOCPANEL_CHECKENVIRONMENTS_ID,'Environments')
    self.environmentsCheck.SetValue(True)
    checkSizer.Add(self.environmentsCheck,0,wx.EXPAND)

    self.stakeholdersCheck = wx.CheckBox(self,REQDOCPANEL_CHECKSTAKEHOLDERS_ID,'Personas')
    self.stakeholdersCheck.SetValue(True)
    checkSizer.Add(self.stakeholdersCheck,0,wx.EXPAND)

    self.mandatedConstraintsCheck = wx.CheckBox(self,REQDOCPANEL_CHECKMANDATEDCONSTRAINTS_ID,'Mandated Constraints')
    self.mandatedConstraintsCheck.SetValue(True)
    checkSizer.Add(self.mandatedConstraintsCheck,0,wx.EXPAND)

    self.namingConventionsCheck = wx.CheckBox(self,REQDOCPANEL_CHECKNAMINGCONVENTIONS_ID,'Naming Conventions')
    self.namingConventionsCheck.SetValue(True)
    checkSizer.Add(self.namingConventionsCheck,0,wx.EXPAND)

    self.projectScopeCheck = wx.CheckBox(self,REQDOCPANEL_CHECKPROJECTSCOPE_ID,'Project Scope')
    self.projectScopeCheck.SetValue(True)
    checkSizer.Add(self.projectScopeCheck,0,wx.EXPAND)

    self.assetsCheck = wx.CheckBox(self,REQDOCPANEL_CHECKASSETS_ID,'Assets')
    self.assetsCheck.SetValue(True)
    checkSizer.Add(self.assetsCheck,0,wx.EXPAND)

    self.tasksCheck = wx.CheckBox(self,REQDOCPANEL_CHECKTASKS_ID,'Tasks')
    self.tasksCheck.SetValue(True)
    checkSizer.Add(self.tasksCheck,0,wx.EXPAND)

    self.ucsCheck = wx.CheckBox(self,REQDOCPANEL_CHECKUSECASES_ID,'Use Cases')
    self.ucsCheck.SetValue(True)
    checkSizer.Add(self.ucsCheck,0,wx.EXPAND)

    self.goalsCheck = wx.CheckBox(self,REQDOCPANEL_CHECKGOALS_ID,'Goals')
    self.goalsCheck.SetValue(True)
    checkSizer.Add(self.goalsCheck,0,wx.EXPAND)

    self.responsibilityCheck = wx.CheckBox(self,REQDOCPANEL_CHECKRESPONSIBILITIES_ID,'Responsibilities')
    self.responsibilityCheck.SetValue(True)
    checkSizer.Add(self.responsibilityCheck,0,wx.EXPAND)

    self.requirementsCheck = wx.CheckBox(self,REQDOCPANEL_CHECKREQUIREMENTS_ID,'Requirements')
    self.requirementsCheck.SetValue(True)
    checkSizer.Add(self.requirementsCheck,0,wx.EXPAND)

    self.obstaclesCheck = wx.CheckBox(self,REQDOCPANEL_CHECKOBSTACLES_ID,'Obstacles')
    self.obstaclesCheck.SetValue(True)
    checkSizer.Add(self.obstaclesCheck,0,wx.EXPAND)

    self.vulnerabilitiesCheck = wx.CheckBox(self,REQDOCPANEL_CHECKVULNERABILITIES_ID,'Vulnerabilities')
    self.vulnerabilitiesCheck.SetValue(True)
    checkSizer.Add(self.vulnerabilitiesCheck,0,wx.EXPAND)

    self.attackersCheck = wx.CheckBox(self,REQDOCPANEL_CHECKATTACKERS_ID,'Attackers')
    self.attackersCheck.SetValue(True)
    checkSizer.Add(self.attackersCheck,0,wx.EXPAND)

    self.threatsCheck = wx.CheckBox(self,REQDOCPANEL_CHECKTHREATS_ID,'Threats')
    self.threatsCheck.SetValue(True)
    checkSizer.Add(self.threatsCheck,0,wx.EXPAND)

    self.risksCheck = wx.CheckBox(self,REQDOCPANEL_CHECKRISKS_ID,'Risks')
    self.risksCheck.SetValue(True)
    checkSizer.Add(self.risksCheck,0,wx.EXPAND)

    self.misuseCasesCheck = wx.CheckBox(self,REQDOCPANEL_CHECKMISUSECASES_ID,'Misuse Cases')
    self.misuseCasesCheck.SetValue(True)
    checkSizer.Add(self.misuseCasesCheck,0,wx.EXPAND)

    self.responsesCheck = wx.CheckBox(self,REQDOCPANEL_CHECKRESPONSES_ID,'Responses')
    self.responsesCheck.SetValue(True)
    checkSizer.Add(self.responsesCheck,0,wx.EXPAND)

    self.countermeasuresCheck = wx.CheckBox(self,REQDOCPANEL_CHECKCOUNTERMEASURES_ID,'Countermeasures')
    self.countermeasuresCheck.SetValue(True)
    checkSizer.Add(self.countermeasuresCheck,0,wx.EXPAND)

    self.SetSizer(checkSizer)

  def sectionFlags(self):
    flags = [
      self.projectPurposeCheck.GetValue(),
      self.environmentsCheck.GetValue(),
      self.stakeholdersCheck.GetValue(),
      self.mandatedConstraintsCheck.GetValue(),
      self.namingConventionsCheck.GetValue(),
      self.projectScopeCheck.GetValue(),
      self.assetsCheck.GetValue(),
      self.tasksCheck.GetValue(),
      self.ucsCheck.GetValue(),
      self.goalsCheck.GetValue(),
      self.responsibilityCheck.GetValue(),
      self.requirementsCheck.GetValue(),
      self.obstaclesCheck.GetValue(),
      self.vulnerabilitiesCheck.GetValue(),
      self.attackersCheck.GetValue(),
      self.threatsCheck.GetValue(),
      self.risksCheck.GetValue(),
      self.misuseCasesCheck.GetValue(),
      self.responsesCheck.GetValue(),
      self.countermeasuresCheck.GetValue()
    ]
    return flags
