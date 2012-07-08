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
import WidgetFactory
from SingleGoalPanel import SingleGoalPanel
from GoalParameters import GoalParameters
from GoalEnvironmentProperties import GoalEnvironmentProperties

class SingleGoalDialog(wx.Dialog):
  def __init__(self,parent,envName):
    wx.Dialog.__init__(self,parent,armid.GOAL_ID,'New Goal',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(500,400))
    self.theCommitVerb = 'Create'
    self.theEnvironmentName = envName
    self.theGoalName = ''
    self.theGoalOriginator = ''
    self.theGoalDefinition = ''
    self.theGoalCategory = ''
    self.theGoalPriority = ''
    self.theGoalFitCriterion = ''
    self.theGoalIssues = ''
    self.theContributionType = 'and'
    self.theAssociations = []
    self.theSubAssociations = []
    self.theConcerns = []
    self.theConcernAssociations = []
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = SingleGoalPanel(self)
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.GOAL_BUTTONCOMMIT_ID,self.onCommit)

  def onCommit(self,evt):
    nameCtrl = self.FindWindowById(armid.GOAL_TEXTNAME_ID)
    origCtrl = self.FindWindowById(armid.GOAL_TEXTORIGINATOR_ID)
    definitionCtrl = self.FindWindowById(armid.GOAL_TEXTDEFINITION_ID)
    categoryCtrl = self.FindWindowById(armid.GOAL_COMBOCATEGORY_ID)
    priorityCtrl = self.FindWindowById(armid.GOAL_COMBOPRIORITY_ID)
    fitCriterionCtrl = self.FindWindowById(armid.GOAL_TEXTFITCRITERION_ID)
    issueCtrl = self.FindWindowById(armid.GOAL_TEXTISSUE_ID)
    goalAssociationCtrl = self.FindWindowById(armid.GOAL_LISTGOALREFINEMENTS_ID)
    subGoalAssociationCtrl = self.FindWindowById(armid.GOAL_LISTSUBGOALREFINEMENTS_ID)
    cCtrl = self.FindWindowById(armid.GOAL_LISTCONCERNS_ID)
    caCtrl = self.FindWindowById(armid.GOAL_LISTCONCERNASSOCIATIONS_ID)
    ctCtrl = self.FindWindowById(armid.GOAL_COMBOCONTRIBUTIONTYPE_ID)

    self.theGoalName = nameCtrl.GetValue()
    self.theGoalOriginator = origCtrl.GetValue()
    self.theGoalDefinition = definitionCtrl.GetValue()
    self.theGoalCategory = categoryCtrl.GetValue()
    self.theGoalPriority = priorityCtrl.GetValue()
    self.theGoalFitCriterion = fitCriterionCtrl.GetValue()
    self.theGoalIssues = issueCtrl.GetValue()
    self.theAssociations = goalAssociationCtrl.dimensions()
    self.theSubAssociations = subGoalAssociationCtrl.dimensions()
    self.theConcerns = cCtrl.dimensions()
    self.theConcernAssociations = caCtrl.dimensions()

    if (ctCtrl.GetValue() == 'Obstructs'):
      self.theContributionType = 'obstruct'


    commitLabel = self.theCommitVerb + ' goal'

    if len(self.theGoalName) == 0:
      dlg = wx.MessageDialog(self,'Goal name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theGoalOriginator) == 0:
      dlg = wx.MessageDialog(self,'Originator cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif len(self.theGoalDefinition) == 0:
      errorTxt = 'No definition'
      dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif len(self.theGoalCategory) == 0:
      errorTxt = 'No category'
      dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif len(self.theGoalPriority) == 0:
      errorTxt = 'No priority'
      dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif len(self.theGoalFitCriterion) == 0:
      errorTxt = 'No fit criterion'
      dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    self.EndModal(armid.GOAL_BUTTONCOMMIT_ID)

  def parameters(self):
    properties = GoalEnvironmentProperties(self.theEnvironmentName,'',self.theGoalDefinition,self.theGoalCategory,self.theGoalPriority,self.theGoalFitCriterion,self.theGoalIssues,self.theAssociations,self.theSubAssociations,self.theConcerns,self.theConcernAssociations)
    parameters = GoalParameters(self.theGoalName,self.theGoalOriginator,[],[properties])
    return parameters
