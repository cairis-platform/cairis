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
import MySQLDatabaseProxy

class GoalRefinementDialog(wx.Dialog):
  def __init__(self,parent,dp,envName,subGoal='',subGoalDim='',refinement='',alternate='',rationale='',isGoal=False):
    wx.Dialog.__init__(self,parent,armid.GOALREFINEMENT_ID,'Add Goal Refinement',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,400))
    self.dbProxy = dp
    self.theCurrentEnvironment = envName
    self.theGoal = subGoal
    self.theGoalDimension = subGoalDim
    self.theRefinement = refinement
    self.theAlternateFlag = alternate
    self.theRationale = rationale
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    goals = self.dbProxy.environmentGoals(self.theCurrentEnvironment)
    goals += self.dbProxy.environmentObstacles(self.theCurrentEnvironment)
    goals += self.dbProxy.environmentDomainProperties(self.theCurrentEnvironment)
    reqList = self.dbProxy.getOrderedRequirements()
    for req in reqList:
      goals += [req.label()]
    refNames = ['and','or','conflict','responsible','obstruct','resolve']
    altNames = ['Yes','No']
    goalDims = ['goal','task','usecase','requirement','obstacle','domainproperty','threat','vulnerability','role','misusecase']
    goalTitle = 'Sub-Goal'
    if isGoal == True:
      goalTitle = 'Goal'
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Type',(87,30),armid.GOALREFINEMENT_COMBOGOALDIMENSION_ID,goalDims),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,goalTitle,(87,30),armid.GOALREFINEMENT_COMBOGOAL_ID,goals),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Refinement',(87,30),armid.GOALREFINEMENT_COMBOREFINEMENT_ID,refNames),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Alternate',(87,30),armid.GOALREFINEMENT_COMBOALTERNATE_ID,altNames),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildMLTextSizer(self,'Rationale',(87,60),armid.GOALREFINEMENT_TEXTRATIONALE_ID),1,wx.EXPAND,1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildAddCancelButtonSizer(self,armid.GOALREFINEMENT_BUTTONCOMMIT_ID),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

    wx.EVT_COMBOBOX(self,armid.GOALREFINEMENT_COMBOGOALDIMENSION_ID,self.onDimChange)
    wx.EVT_BUTTON(self,armid.GOALREFINEMENT_BUTTONCOMMIT_ID,self.onCommit)
    self.commitLabel = 'Add'
    if (len(self.theGoal) > 0):
      self.commitLabel = 'Edit'
      self.SetLabel('Edit Goal Refinement')
      subGoalCtrl = self.FindWindowById(armid.GOALREFINEMENT_COMBOGOAL_ID)
      subGoalCtrl.SetStringSelection(self.theGoal)
      dimCtrl = self.FindWindowById(armid.GOALREFINEMENT_COMBOGOALDIMENSION_ID)
      dimCtrl.SetStringSelection(self.theGoalDimension)
      refCtrl = self.FindWindowById(armid.GOALREFINEMENT_COMBOREFINEMENT_ID)
      refCtrl.SetStringSelection(self.theRefinement)
      altCtrl = self.FindWindowById(armid.GOALREFINEMENT_COMBOALTERNATE_ID)
      altCtrl.SetStringSelection(self.theAlternateFlag)
      ratCtrl = self.FindWindowById(armid.GOALREFINEMENT_TEXTRATIONALE_ID)
      ratCtrl.SetValue(self.theRationale)
      buttonCtrl = self.FindWindowById(armid.GOALREFINEMENT_BUTTONCOMMIT_ID)
      buttonCtrl.SetLabel('Edit')
      

  def onDimChange(self,evt):
    goalDimCtrl = self.FindWindowById(armid.GOALREFINEMENT_COMBOGOALDIMENSION_ID)
    goalDimName = goalDimCtrl.GetStringSelection()
    subGoalCtrl = self.FindWindowById(armid.GOALREFINEMENT_COMBOGOAL_ID)

    if (goalDimName != ''):
      goalCtrl = self.FindWindowById(armid.GOALASSOCIATION_COMBOGOAL_ID)
      if (goalDimName == 'goal'):
        subGoalCtrl.SetItems(self.dbProxy.environmentGoals(self.theCurrentEnvironment))
      elif (goalDimName == 'requirement'):
        reqDict = self.dbProxy.getRequirements()
        descList = []
        reqValues = reqDict.values()
        reqValues.sort()
        for r in reqValues:
          descList.append(r.label())
        subGoalCtrl.SetItems(descList)
      elif (goalDimName == 'obstacle'):
        subGoalCtrl.SetItems(self.dbProxy.environmentObstacles(self.theCurrentEnvironment))
      elif (goalDimName == 'domainproperty'):
        subGoalCtrl.SetItems(self.dbProxy.environmentDomainProperties(self.theCurrentEnvironment))
      elif (goalDimName == 'threat'):
        subGoalCtrl.SetItems(self.dbProxy.environmentThreats(self.theCurrentEnvironment))
      elif (goalDimName == 'vulnerability'):
        subGoalCtrl.SetItems(self.dbProxy.environmentVulnerabilities(self.theCurrentEnvironment))
      elif (goalDimName == 'task'):
        subGoalCtrl.SetItems(self.dbProxy.environmentTasks(self.theCurrentEnvironment))
      elif (goalDimName == 'usecase'):
        subGoalCtrl.SetItems(self.dbProxy.environmentUseCases(self.theCurrentEnvironment))
      elif (goalDimName == 'misusecase'):
        subGoalCtrl.SetItems(self.dbProxy.environmentMisuseCases(self.theCurrentEnvironment))
      elif (goalDimName == 'role'):
        subGoalCtrl.SetItems(self.dbProxy.getDimensionNames('role'))

  def onCommit(self,evt):
    subGoalCtrl = self.FindWindowById(armid.GOALREFINEMENT_COMBOGOAL_ID)
    dimCtrl = self.FindWindowById(armid.GOALREFINEMENT_COMBOGOALDIMENSION_ID)
    refCtrl = self.FindWindowById(armid.GOALREFINEMENT_COMBOREFINEMENT_ID)
    altCtrl = self.FindWindowById(armid.GOALREFINEMENT_COMBOALTERNATE_ID)
    ratCtrl = self.FindWindowById(armid.GOALREFINEMENT_TEXTRATIONALE_ID)

    self.theGoal = subGoalCtrl.GetStringSelection()
    self.theGoalDimension = dimCtrl.GetStringSelection()
    self.theRefinement = refCtrl.GetStringSelection()
    self.theAlternateFlag = altCtrl.GetStringSelection()
    self.theRationale = ratCtrl.GetValue()

    if (len(self.theGoal) == 0):
      dlg = wx.MessageDialog(self,'No goal selected',self.commitLabel + ' Goal Association',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theGoalDimension) == 0):
      dlg = wx.MessageDialog(self,'No goal type selected',self.commitLabel + ' Goal Association',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theRefinement) == 0):
      dlg = wx.MessageDialog(self,'No refinement selected',self.commitLabel + ' Goal Association',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theAlternateFlag) == 0):
      dlg = wx.MessageDialog(self,'No alternate flag selected',self.commitLabel + ' Goal Association',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      if (len(self.theRationale) == 0):
        self.theRationale = 'None'
      self.EndModal(armid.GOALREFINEMENT_BUTTONCOMMIT_ID)

  def goal(self): return self.theGoal
  def goalDimension(self): return self.theGoalDimension
  def refinement(self): return self.theRefinement
  def alternate(self): return self.theAlternateFlag
  def rationale(self): return self.theRationale
