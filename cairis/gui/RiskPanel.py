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
from BasePanel import BasePanel
import armid
import RiskParameters
from Borg import Borg

class RiskPanel(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,armid.RISK_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theThreats = self.dbProxy.getDimensions('threat')
    self.theVulnerabilities = self.dbProxy.getDimensions('vulnerability')
    self.detailsList = []
 
  def buildControls(self,isCreate,isUpdateable=True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(self.buildTextSizer('Name',(87,30),armid.RISK_TEXTNAME_ID),0,wx.EXPAND)
    mainSizer.Add(self.buildTagCtrlSizer((87,30),armid.RISK_TAGS_ID),0,wx.EXPAND)
    tvSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(tvSizer,0,wx.EXPAND)
    tvSizer.Add(self.buildComboSizer('Threat',(87,30),armid.RISK_COMBOTHREAT_ID,self.theThreats),1,wx.EXPAND)
    tvSizer.Add(self.buildComboSizer('Vulnerability',(87,30),armid.RISK_COMBOVULNERABILITY_ID,self.theVulnerabilities),1,wx.EXPAND)

    environmentBox = wx.StaticBox(self,-1,'Environments')
    environmentBoxSizer = wx.StaticBoxSizer(environmentBox,wx.VERTICAL)
    mainSizer.Add(environmentBoxSizer,0,wx.EXPAND)
    self.environmentList = wx.ListBox(self,armid.RISK_LISTENVIRONMENTS_ID,size=(150,70),style=wx.LB_SINGLE | wx.LB_SORT)
    environmentBoxSizer.Add(self.environmentList,0,wx.EXPAND)

    mainSizer.Add(self.buildTextSizer('Rating',(87,30),armid.RISK_TEXTRATING_ID,isReadOnly=True),0,wx.EXPAND)

    scoreBox = wx.StaticBox(self,-1,'')
    scoreBoxSizer = wx.StaticBoxSizer(scoreBox,wx.VERTICAL)
    mainSizer.Add(scoreBoxSizer,1,wx.EXPAND)
    self.scoreList = wx.ListCtrl(self,armid.RISK_LISTSCORE_ID,style=wx.LC_REPORT)
    self.scoreList.InsertColumn(0,'Response')
    self.scoreList.InsertColumn(1,'Unmit. Score')
    self.scoreList.InsertColumn(2,'Mit. Score')
    self.scoreList.SetColumnWidth(0,200)
    self.scoreList.SetColumnWidth(1,100)
    self.scoreList.SetColumnWidth(2,100)
    scoreBoxSizer.Add(self.scoreList,0,wx.EXPAND)

    scoreButtonSizer = wx.BoxSizer(wx.HORIZONTAL)
    scoreBoxSizer.Add(scoreButtonSizer,0,wx.EXPAND)
    self.detailsButton = wx.Button(self,armid.RISK_BUTTONDETAILS_ID,'Show Details')
    scoreButtonSizer.Add(self.detailsButton,0,wx.EXPAND)

    self.scoreDetailsSizer = wx.BoxSizer(wx.VERTICAL)
    scoreBoxSizer.Add(self.scoreDetailsSizer,1,wx.EXPAND)
    self.detailsCtrl = wx.TextCtrl(self,armid.RISK_TEXTSCOREDETAILS_ID,style=wx.TE_READONLY | wx.TE_MULTILINE)
    self.scoreDetailsSizer.Add(self.detailsCtrl,1,wx.EXPAND)
    mainSizer.Add(self.buildRiskButtonSizer(armid.RISK_BUTTONCOMMIT_ID,armid.RISK_BUTTONMISUSECASE_ID,isCreate),0,wx.ALIGN_CENTER)
    self.nameCtrl = self.FindWindowById(armid.RISK_TEXTNAME_ID)
    self.tagsCtrl = self.FindWindowById(armid.RISK_TAGS_ID)
    self.threatCombo = self.FindWindowById(armid.RISK_COMBOTHREAT_ID)
    self.vulnerabilityCombo = self.FindWindowById(armid.RISK_COMBOVULNERABILITY_ID)
    self.ratingCtrl = self.FindWindowById(armid.RISK_TEXTRATING_ID)
    self.threatCombo.Bind(wx.EVT_COMBOBOX,self.onThreatChange)
    self.vulnerabilityCombo.Bind(wx.EVT_COMBOBOX,self.onVulnerabilityChange)
    self.environmentList.Bind(wx.EVT_LISTBOX,self.onEnvironmentSelected)
    self.scoreList.Bind(wx.EVT_LIST_ITEM_SELECTED,self.onResponseSelected)
    self.detailsButton.Bind(wx.EVT_BUTTON,self.onButtonDetails)
    self.SetSizer(mainSizer)
    self.detailsCtrl.Show(False)

  def loadControls(self,risk,isReadOnly = False):
    self.environmentList.Unbind(wx.EVT_LISTBOX)
    riskName = risk.name()
    threatName = risk.threat()
    vulName = risk.vulnerability()
    tags = risk.tags()
    self.nameCtrl.SetValue(riskName)
    self.tagsCtrl.set(tags)
    self.threatCombo.SetStringSelection(threatName)
    self.vulnerabilityCombo.SetStringSelection(vulName)
    self.evaluateEnvironments()
    self.environmentList.Bind(wx.EVT_LISTBOX,self.onEnvironmentSelected)

  def onThreatChange(self,evt):
    self.evaluateEnvironments()

  def onVulnerabilityChange(self,evt):
    self.evaluateEnvironments()

  def evaluateEnvironments(self):
    threatName = self.threatCombo.GetStringSelection()
    vulName = self.vulnerabilityCombo.GetStringSelection()
    riskEnvironments = self.dbProxy.riskEnvironments(threatName,vulName)
    self.environmentList.Set(riskEnvironments)
    if ((len(threatName) == 0) or (len(vulName) == 0) or (len(riskEnvironments) == 0)):
      self.environmentList.Clear()
      self.ratingCtrl.Clear()
      self.scoreList.DeleteAllItems()
      self.detailsCtrl.Clear()
    else:
      self.environmentList.Set(self.dbProxy.riskEnvironments(threatName,vulName))

  def onEnvironmentSelected(self,evt):
    if (evt.GetSelection() != -1):
      riskName = self.nameCtrl.GetValue()
      threatName = self.threatCombo.GetStringSelection()
      vulName = self.vulnerabilityCombo.GetStringSelection()
      environmentName = self.environmentList.GetString(evt.GetSelection())
      self.ratingCtrl.SetValue(self.dbProxy.riskRating(threatName,vulName,environmentName))
      riskScoreList = self.dbProxy.riskScore(threatName,vulName,environmentName,riskName)
      self.detailsList = []
      self.scoreList.DeleteAllItems()
      for idx,riskScore in enumerate(riskScoreList):
        riskResponse = riskScore[0]
        prmValue = str(riskScore[1])
        pomValue = str(riskScore[2])
        riskDetails = riskScore[3]
        self.scoreList.InsertStringItem(idx,riskResponse)
        self.scoreList.SetStringItem(idx,1,prmValue) 
        self.scoreList.SetStringItem(idx,2,pomValue) 
        self.detailsList.append(riskDetails)
      self.scoreList.Select(0)

  def onResponseSelected(self,evt):
    idx = evt.GetIndex()
    if (idx != -1):
      self.detailsCtrl.SetValue(self.detailsList[idx])

  def onButtonDetails(self,evt):
    if (self.detailsButton.GetLabelText() == 'Show Details'):
      self.detailsCtrl.Show(True)
      self.detailsButton.SetLabel('Hide Details')
    else:
      self.detailsCtrl.Show(False)
      self.detailsButton.SetLabel('Show Details')
