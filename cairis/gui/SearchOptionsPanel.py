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

class SearchOptionsPanel(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,SEARCHOPTIONSPANEL_ID)
    mainSizer = wx.BoxSizer(wx.VERTICAL)

    self.toggleCheck = wx.CheckBox(self,SEARCHPANEL_CHECKTOGGLE_ID,'Toggle all')
    self.toggleCheck.SetValue(True)
    mainSizer.Add(self.toggleCheck,0,wx.EXPAND)
    optSizer = wx.GridSizer(10,2,5,5)
    mainSizer.Add(optSizer,1,wx.EXPAND)

    self.psCheck = wx.CheckBox(self,SEARCHPANEL_CHECKPS_ID,'Project Settings')
    self.psCheck.SetValue(True)
    self.envCheck = wx.CheckBox(self,SEARCHPANEL_CHECKENV_ID,'Environments')
    self.envCheck.SetValue(True)
    self.roleCheck = wx.CheckBox(self,SEARCHPANEL_CHECKROLE_ID,'Roles')
    self.roleCheck.SetValue(True)
    self.pcCheck = wx.CheckBox(self,SEARCHPANEL_CHECKPC_ID,'Persona Characteristics')
    self.pcCheck.SetValue(True)
    self.tcCheck = wx.CheckBox(self,SEARCHPANEL_CHECKTC_ID,'Task Characteristics')
    self.tcCheck.SetValue(True)
    self.refCheck = wx.CheckBox(self,SEARCHPANEL_CHECKREF_ID,'References')
    self.refCheck.SetValue(True)
    self.pCheck = wx.CheckBox(self,SEARCHPANEL_CHECKP_ID,'Personas')
    self.pCheck.SetValue(True)
    self.taskCheck = wx.CheckBox(self,SEARCHPANEL_CHECKTASK_ID,'Tasks')
    self.taskCheck.SetValue(True)
    self.ucCheck = wx.CheckBox(self,SEARCHPANEL_CHECKUC_ID,'Use Cases')
    self.ucCheck.SetValue(True)
    self.dpCheck = wx.CheckBox(self,SEARCHPANEL_CHECKDP_ID,'Domain Properties')
    self.dpCheck.SetValue(True)
    self.goalCheck = wx.CheckBox(self,SEARCHPANEL_CHECKGOAL_ID,'Goals')
    self.goalCheck.SetValue(True)
    self.obsCheck = wx.CheckBox(self,SEARCHPANEL_CHECKOBS_ID,'Obstacles')
    self.obsCheck.SetValue(True)
    self.reqCheck = wx.CheckBox(self,SEARCHPANEL_CHECKREQ_ID,'Requirements')
    self.reqCheck.SetValue(True)
    self.assetCheck = wx.CheckBox(self,SEARCHPANEL_CHECKASSET_ID,'Assets')
    self.assetCheck.SetValue(True)
    self.vulCheck = wx.CheckBox(self,SEARCHPANEL_CHECKVUL_ID,'Vulnerabilities')
    self.vulCheck.SetValue(True)
    self.attackerCheck = wx.CheckBox(self,SEARCHPANEL_CHECKATTACKER_ID,'Attackers')
    self.attackerCheck.SetValue(True)
    self.thrCheck = wx.CheckBox(self,SEARCHPANEL_CHECKTHR_ID,'Threats')
    self.thrCheck.SetValue(True)
    self.riskCheck = wx.CheckBox(self,SEARCHPANEL_CHECKRISK_ID,'Risks')
    self.riskCheck.SetValue(True)
    self.respCheck = wx.CheckBox(self,SEARCHPANEL_CHECKRESP_ID,'Responses')
    self.respCheck.SetValue(True)
    self.cmCheck = wx.CheckBox(self,SEARCHPANEL_CHECKCM_ID,'Countermeasures')
    self.cmCheck.SetValue(True)
    self.dirCheck = wx.CheckBox(self,SEARCHPANEL_CHECKDIR_ID,'Directories')
    self.dirCheck.SetValue(True)
    self.codeCheck = wx.CheckBox(self,SEARCHPANEL_CHECKCODE_ID,'Codes')
    self.codeCheck.SetValue(True)
    self.memoCheck = wx.CheckBox(self,SEARCHPANEL_CHECKMEMO_ID,'Memos')
    self.memoCheck.SetValue(True)
    self.internalDocumentCheck = wx.CheckBox(self,SEARCHPANEL_CHECKINTERNALDOCUMENT_ID,'Internal Documents')
    self.internalDocumentCheck.SetValue(True)
    self.tagCheck = wx.CheckBox(self, armdid.SEARCHPANEL_CHECKTAGS_ID,'Tags')
    self.tagCheck.SetValue(True)

    optSizer.Add(self.psCheck)
    optSizer.Add(self.envCheck)
    optSizer.Add(self.roleCheck)
    optSizer.Add(self.pcCheck)
    optSizer.Add(self.tcCheck)
    optSizer.Add(self.refCheck)
    optSizer.Add(self.pCheck)
    optSizer.Add(self.taskCheck)
    optSizer.Add(self.ucCheck)
    optSizer.Add(self.dpCheck)
    optSizer.Add(self.goalCheck)
    optSizer.Add(self.obsCheck)
    optSizer.Add(self.reqCheck)
    optSizer.Add(self.assetCheck)
    optSizer.Add(self.vulCheck)
    optSizer.Add(self.attackerCheck)
    optSizer.Add(self.thrCheck)
    optSizer.Add(self.riskCheck)
    optSizer.Add(self.respCheck)
    optSizer.Add(self.cmCheck)
    optSizer.Add(self.dirCheck)
    optSizer.Add(self.codeCheck)
    optSizer.Add(self.memoCheck)
    optSizer.Add(self.internalDocumentCheck)
    optSizer.Add(self.tagCheck)

    self.SetSizer(mainSizer)
    self.toggleCheck.Bind(wx.EVT_CHECKBOX,self.toggleFlags)

  def toggleFlags(self,evt):
    if self.toggleCheck.GetValue() == True:
      self.psCheck.SetValue(True)
      self.envCheck.SetValue(True)
      self.roleCheck.SetValue(True)
      self.pcCheck.SetValue(True)
      self.tcCheck.SetValue(True)
      self.refCheck.SetValue(True)
      self.pCheck.SetValue(True)
      self.taskCheck.SetValue(True)
      self.ucCheck.SetValue(True)
      self.dpCheck.SetValue(True)
      self.goalCheck.SetValue(True)
      self.obsCheck.SetValue(True)
      self.reqCheck.SetValue(True)
      self.assetCheck.SetValue(True)
      self.vulCheck.SetValue(True)
      self.attackerCheck.SetValue(True)
      self.thrCheck.SetValue(True)
      self.riskCheck.SetValue(True)
      self.respCheck.SetValue(True)
      self.cmCheck.SetValue(True)
      self.dirCheck.SetValue(True)
      self.codeCheck.SetValue(True)
      self.memoCheck.SetValue(True)
      self.internalDocumentCheck.SetValue(True)
      self.tagCheck.SetValue(True)
    else:
      self.psCheck.SetValue(False)
      self.envCheck.SetValue(False)
      self.roleCheck.SetValue(False)
      self.pcCheck.SetValue(False)
      self.tcCheck.SetValue(False)
      self.refCheck.SetValue(False)
      self.pCheck.SetValue(False)
      self.taskCheck.SetValue(False)
      self.ucCheck.SetValue(False)
      self.dpCheck.SetValue(False)
      self.goalCheck.SetValue(False)
      self.obsCheck.SetValue(False)
      self.reqCheck.SetValue(False)
      self.assetCheck.SetValue(False)
      self.vulCheck.SetValue(False)
      self.attackerCheck.SetValue(False)
      self.thrCheck.SetValue(False)
      self.riskCheck.SetValue(False)
      self.respCheck.SetValue(False)
      self.cmCheck.SetValue(False)
      self.dirCheck.SetValue(False)
      self.codeCheck.SetValue(False)
      self.memoCheck.SetValue(False)
      self.internalDocumentCheck.SetValue(False)
      self.tagCheck.SetValue(False)

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
      self.cmCheck.GetValue(),
      self.dirCheck.GetValue(),
      self.codeCheck.GetValue(),
      self.memoCheck.GetValue(),
      self.internalDocumentCheck.GetValue(),
      self.tagCheck.GetValue()]
    return flags

