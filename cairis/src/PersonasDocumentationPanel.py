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

class PersonasDocumentationPanel(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,armid.PERDOCPANEL_ID)
    checkSizer = wx.BoxSizer(wx.VERTICAL)

    self.projectPurposeCheck = wx.CheckBox(self,armid.PERDOCPANEL_CHECKPROJECTPURPOSE_ID,'Project Purpose')
    self.projectPurposeCheck.SetValue(True)
    checkSizer.Add(self.projectPurposeCheck,0,wx.EXPAND)

    self.projectScopeCheck = wx.CheckBox(self,armid.PERDOCPANEL_CHECKPROJECTSCOPE_ID,'Project Scope')
    self.projectScopeCheck.SetValue(True)
    checkSizer.Add(self.projectScopeCheck,0,wx.EXPAND)

    self.environmentsCheck = wx.CheckBox(self,armid.PERDOCPANEL_CHECKENVIRONMENTS_ID,'Environments')
    self.environmentsCheck.SetValue(True)
    checkSizer.Add(self.environmentsCheck,0,wx.EXPAND)

    self.stakeholdersCheck = wx.CheckBox(self,armid.PERDOCPANEL_CHECKSTAKEHOLDERS_ID,'Personas')
    self.stakeholdersCheck.SetValue(True)
    checkSizer.Add(self.stakeholdersCheck,0,wx.EXPAND)

    self.tasksCheck = wx.CheckBox(self,armid.PERDOCPANEL_CHECKTASKS_ID,'Tasks')
    self.tasksCheck.SetValue(True)
    checkSizer.Add(self.tasksCheck,0,wx.EXPAND)

    self.SetSizer(checkSizer)

  def sectionFlags(self):
    flags = [
      self.projectPurposeCheck.GetValue(),
      self.projectScopeCheck.GetValue(),
      self.environmentsCheck.GetValue(),
      self.stakeholdersCheck.GetValue(),
      self.tasksCheck.GetValue()
    ]
    return flags
