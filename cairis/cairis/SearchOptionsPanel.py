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

class SearchOptionsPanel(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,armid.SEARCHOPTIONSPANEL_ID)
    mainSizer = wx.GridSizer(10,2,5,5)

    self.psCheck = wx.CheckBox(self,armid.SEARCHPANEL_CHECKPS_ID,'Project Settings')
    self.psCheck.SetValue(True)
    self.envCheck = wx.CheckBox(self,armid.SEARCHPANEL_CHECKENV_ID,'Environments')
    self.envCheck.SetValue(True)
    self.roleCheck = wx.CheckBox(self,armid.SEARCHPANEL_CHECKROLE_ID,'Roles')
    self.roleCheck.SetValue(True)
    self.pcCheck = wx.CheckBox(self,armid.SEARCHPANEL_CHECKPC_ID,'Persona Characteristics')
    self.pcCheck.SetValue(True)
    self.tcCheck = wx.CheckBox(self,armid.SEARCHPANEL_CHECKTC_ID,'Task Characteristics')
    self.tcCheck.SetValue(True)
    self.refCheck = wx.CheckBox(self,armid.SEARCHPANEL_CHECKREF_ID,'References')
    self.refCheck.SetValue(True)
    self.pCheck = wx.CheckBox(self,armid.SEARCHPANEL_CHECKP_ID,'Personas')
    self.pCheck.SetValue(True)
    self.taskCheck = wx.CheckBox(self,armid.SEARCHPANEL_CHECKTASK_ID,'Tasks')
    self.taskCheck.SetValue(True)
    self.ucCheck = wx.CheckBox(self,armid.SEARCHPANEL_CHECKUC_ID,'Use Cases')
    self.ucCheck.SetValue(True)
    self.dpCheck = wx.CheckBox(self,armid.SEARCHPANEL_CHECKDP_ID,'Domain Properties')
    self.dpCheck.SetValue(True)
    self.goalCheck = wx.CheckBox(self,armid.SEARCHPANEL_CHECKGOAL_ID,'Goals')
    self.goalCheck.SetValue(True)
    self.obsCheck = wx.CheckBox(self,armid.SEARCHPANEL_CHECKOBS_ID,'Obstacles')
    self.obsCheck.SetValue(True)
    self.reqCheck = wx.CheckBox(self,armid.SEARCHPANEL_CHECKREQ_ID,'Requirements')
    self.reqCheck.SetValue(True)
    self.assetCheck = wx.CheckBox(self,armid.SEARCHPANEL_CHECKASSET_ID,'Assets')
    self.assetCheck.SetValue(True)
    self.vulCheck = wx.CheckBox(self,armid.SEARCHPANEL_CHECKVUL_ID,'Vulnerabilities')
    self.vulCheck.SetValue(True)
    self.attackerCheck = wx.CheckBox(self,armid.SEARCHPANEL_CHECKATTACKER_ID,'Attackers')
    self.attackerCheck.SetValue(True)
    self.thrCheck = wx.CheckBox(self,armid.SEARCHPANEL_CHECKTHR_ID,'Threats')
    self.thrCheck.SetValue(True)
    self.riskCheck = wx.CheckBox(self,armid.SEARCHPANEL_CHECKRISK_ID,'Risks')
    self.riskCheck.SetValue(True)
    self.respCheck = wx.CheckBox(self,armid.SEARCHPANEL_CHECKRESP_ID,'Responses')
    self.respCheck.SetValue(True)
    self.cmCheck = wx.CheckBox(self,armid.SEARCHPANEL_CHECKCM_ID,'Countermeasures')
    self.cmCheck.SetValue(True)

    mainSizer.Add(self.psCheck)
    mainSizer.Add(self.envCheck)
    mainSizer.Add(self.roleCheck)
    mainSizer.Add(self.pcCheck)
    mainSizer.Add(self.tcCheck)
    mainSizer.Add(self.refCheck)
    mainSizer.Add(self.pCheck)
    mainSizer.Add(self.taskCheck)
    mainSizer.Add(self.ucCheck)
    mainSizer.Add(self.dpCheck)
    mainSizer.Add(self.goalCheck)
    mainSizer.Add(self.obsCheck)
    mainSizer.Add(self.reqCheck)
    mainSizer.Add(self.assetCheck)
    mainSizer.Add(self.vulCheck)
    mainSizer.Add(self.attackerCheck)
    mainSizer.Add(self.thrCheck)
    mainSizer.Add(self.riskCheck)
    mainSizer.Add(self.respCheck)
    mainSizer.Add(self.cmCheck)

    self.SetSizer(mainSizer)

  def optionFlags(self):
    flags = [
      self.psCheck.GetValue(),
      self.envCheck.GetValue(),
      self.roleCheck.GetValue(),
      self.pcCheck.GetValue(),
      self.tcCheck.GetValue(),
      self.refCheck.GetValue(),
      self.pCheck.GetValue(),
      self.taskCheck.GetValue(),
      self.ucCheck.GetValue(),
      self.dpCheck.GetValue(),
      self.goalCheck.GetValue(),
      self.obsCheck.GetValue(),
      self.reqCheck.GetValue(),
      self.assetCheck.GetValue(),
      self.vulCheck.GetValue(),
      self.attackerCheck.GetValue(),
      self.thrCheck.GetValue(),
      self.riskCheck.GetValue(),
      self.respCheck.GetValue(),
      self.cmCheck.GetValue()]
    return flags

