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
import WidgetFactory
from cairis.core.Borg import Borg
from cairis.core.GoalAssociationParameters import GoalAssociationParameters

class GoalAssociationDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,GOALASSOCIATION_ID,'Goal association',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(600,400))
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theGoalAssociationId = -1
    self.theEnvironmentName = ''
    self.theGoal = ''
    self.theGoalDimension = ''
    self.theGoalAssociationType = ''
    self.theSubGoal = ''
    self.theSubGoalDimension = ''
    self.theRationale = 'None.'
    self.theAlternativeFlag = 0
    self.buildControls(parameters)
    self.commitVerb = 'Add'

  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    associationSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(WidgetFactory.buildCheckSizer(self,'Alternative',GOALASSOCIATION_CHECKALTERNATIVE_ID,False),0,wx.EXPAND)
    mainSizer.Add(associationSizer,0,wx.EXPAND)
    environments = self.dbProxy.getDimensionNames('environment')
    goals = []
    associationTypes = ['and','or','conflict','responsible','obstruct','resolve']
    goalDimensions = ['goal','requirement','countermeasure','obstacle']
    subGoalDimensions = ['goal','requirement','role','task','usecase','countermeasure','domainproperty','obstacle','threat','vulnerability']

    associationSizer.Add(WidgetFactory.buildComboSizerList(self,'Environment',(87,30),GOALASSOCIATION_COMBOENVIRONMENT_ID,environments),0,wx.EXPAND)
    associationSizer.Add(WidgetFactory.buildComboSizerList(self,'Dimension',(87,30),GOALASSOCIATION_COMBOGOALDIM_ID,goalDimensions),0,wx.EXPAND)
    associationSizer.Add(WidgetFactory.buildComboSizerList(self,'Goal',(87,30),GOALASSOCIATION_COMBOGOAL_ID,goals),0,wx.EXPAND)
    associationSizer.Add(WidgetFactory.buildComboSizerList(self,'Type',(87,30),GOALASSOCIATION_COMBOATYPE_ID,associationTypes),0,wx.EXPAND)
    associationSizer.Add(WidgetFactory.buildComboSizerList(self,'Dimension',(87,30),GOALASSOCIATION_COMBOSUBGOALDIM_ID,subGoalDimensions),0,wx.EXPAND)
    associationSizer.Add(WidgetFactory.buildComboSizerList(self,'Sub-Goal',(87,30),GOALASSOCIATION_COMBOSUBGOAL_ID,goals),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildMLTextSizer(self,'Rationale',(87,60),GOALASSOCIATION_TEXTRATIONALE_ID),1,wx.EXPAND,1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildAddCancelButtonSizer(self,GOALASSOCIATION_BUTTONCOMMIT_ID),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

    wx.EVT_BUTTON(self,GOALASSOCIATION_BUTTONCOMMIT_ID,self.onCommit)
    wx.EVT_COMBOBOX(self,GOALASSOCIATION_COMBOENVIRONMENT_ID,self.onEnvironmentChange)
    wx.EVT_COMBOBOX(self,GOALASSOCIATION_COMBOGOALDIM_ID,self.onGoalDimChange)
    wx.EVT_COMBOBOX(self,GOALASSOCIATION_COMBOSUBGOALDIM_ID,self.onSubGoalDimChange)

  def load(self,association):
    self.theGoalAssociationId = association.id()
    envCtrl = self.FindWindowById(GOALASSOCIATION_COMBOENVIRONMENT_ID)
    goalCtrl = self.FindWindowById(GOALASSOCIATION_COMBOGOAL_ID)
    goalDimCtrl = self.FindWindowById(GOALASSOCIATION_COMBOGOALDIM_ID)
    atypeCtrl = self.FindWindowById(GOALASSOCIATION_COMBOATYPE_ID)
    subGoalCtrl = self.FindWindowById(GOALASSOCIATION_COMBOSUBGOAL_ID)
    subGoalDimCtrl = self.FindWindowById(GOALASSOCIATION_COMBOSUBGOALDIM_ID)
    alternativeCtrl = self.FindWindowById(GOALASSOCIATION_CHECKALTERNATIVE_ID)
    rationaleCtrl = self.FindWindowById(GOALASSOCIATION_TEXTRATIONALE_ID)
    buttonCtrl = self.FindWindowById(GOALASSOCIATION_BUTTONCOMMIT_ID)
    buttonCtrl.SetLabel('Edit')
  
    self.theEnvironmentName = association.environment()
    self.theGoal = association.goal()
    self.theGoalDimension = association.goalDimension()
    self.theGoalAssociationType = association.type()
    self.theSubGoal = association.subGoal()
    self.theSubGoalDimension = association.subGoalDimension()
    self.theAlternativeFlag = association.alternative()
    self.theRationale = association.rationale()


    envCtrl.SetValue(self.theEnvironmentName)
    goalCtrl.SetValue(self.theGoal)
    goalDimCtrl.SetValue(self.theGoalDimension)
    atypeCtrl.SetValue(self.theGoalAssociationType)
    subGoalCtrl.SetValue(self.theSubGoal)
    subGoalDimCtrl.SetValue(self.theSubGoalDimension)
    alternativeCtrl.SetValue(self.theAlternativeFlag)
    rationaleCtrl.SetValue(self.theRationale)
    
    self.commitVerb = 'Edit'
    
  def onCommit(self,evt):
    commitLabel = self.commitVerb + ' association'
    envCtrl = self.FindWindowById(GOALASSOCIATION_COMBOENVIRONMENT_ID)
    goalCtrl = self.FindWindowById(GOALASSOCIATION_COMBOGOAL_ID)
    goalDimCtrl = self.FindWindowById(GOALASSOCIATION_COMBOGOALDIM_ID)
    atypeCtrl = self.FindWindowById(GOALASSOCIATION_COMBOATYPE_ID)
    subGoalCtrl = self.FindWindowById(GOALASSOCIATION_COMBOSUBGOAL_ID)
    subGoalDimCtrl = self.FindWindowById(GOALASSOCIATION_COMBOSUBGOALDIM_ID)
    alternativeCtrl = self.FindWindowById(GOALASSOCIATION_CHECKALTERNATIVE_ID)
    rationaleCtrl = self.FindWindowById(GOALASSOCIATION_TEXTRATIONALE_ID)

    self.theEnvironmentName = envCtrl.GetValue()
    self.theGoal = goalCtrl.GetValue()
    self.theGoalDimension = goalDimCtrl.GetValue()
    self.theGoalAssociationType = atypeCtrl.GetValue()
    self.theSubGoal = subGoalCtrl.GetValue()
    self.theSubGoalDimension = subGoalDimCtrl.GetValue()
    self.theAlternativeFlag = alternativeCtrl.GetValue()
    self.theRationale = rationaleCtrl.GetValue()

    if (len(self.theRationale) == 0):
      self.theRationale = 'None.'

    if len(self.theEnvironmentName) == 0:
      dlg = wx.MessageDialog(self,'No environment selected',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif len(self.theGoalDimension) == 0:
      dlg = wx.MessageDialog(self,'No goal dimension selected',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif len(self.theGoal) == 0:
      dlg = wx.MessageDialog(self,'No goal selected',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif len(self.theSubGoalDimension) == 0:
      dlg = wx.MessageDialog(self,'No sub goal dimension selected',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif len(self.theSubGoal) == 0:
      dlg = wx.MessageDialog(self,'No sub goal selected',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theGoalAssociationType) == 0):
      dlg = wx.MessageDialog(self,'No association type selected',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(GOALASSOCIATION_BUTTONCOMMIT_ID)

  def onEnvironmentChange(self,evt):
    envCtrl = self.FindWindowById(GOALASSOCIATION_COMBOENVIRONMENT_ID)
    goalCtrl = self.FindWindowById(GOALASSOCIATION_COMBOGOAL_ID)
    goalDimCtrl = self.FindWindowById(GOALASSOCIATION_COMBOGOALDIM_ID)
    atypeCtrl = self.FindWindowById(GOALASSOCIATION_COMBOATYPE_ID)
    subGoalCtrl = self.FindWindowById(GOALASSOCIATION_COMBOSUBGOAL_ID)
    subGoalDimCtrl = self.FindWindowById(GOALASSOCIATION_COMBOSUBGOALDIM_ID)
    alternativeCtrl = self.FindWindowById(GOALASSOCIATION_CHECKALTERNATIVE_ID)
    rationaleCtrl = self.FindWindowById(GOALASSOCIATION_TEXTRATIONALE_ID)
    goalCtrl.SetItems([])
    subGoalCtrl.SetItems([])
    goalCtrl.SetValue('')
    goalDimCtrl.SetValue('')
    atypeCtrl.SetValue('')
    subGoalCtrl.SetValue('')
    subGoalDimCtrl.SetValue('')
    alternativeCtrl.SetValue(0)
    rationaleCtrl.SetValue('')
    envName = envCtrl.GetStringSelection()

  def onGoalDimChange(self,evt):
    envCtrl = self.FindWindowById(GOALASSOCIATION_COMBOENVIRONMENT_ID)
    goalDimCtrl = self.FindWindowById(GOALASSOCIATION_COMBOGOALDIM_ID)
    envName = envCtrl.GetStringSelection()
    goalDimName = goalDimCtrl.GetStringSelection()

    if (envName != '') and (goalDimName != ''):
      goalCtrl = self.FindWindowById(GOALASSOCIATION_COMBOGOAL_ID)
      if (goalDimName == 'goal'):
        goalCtrl.SetItems(self.dbProxy.environmentGoals(envName))
      elif (goalDimName == 'obstacle'):
        goalCtrl.SetItems(self.dbProxy.environmentObstacles(envName))
      elif (goalDimName == 'countermeasure'):
        goalCtrl.SetItems(self.dbProxy.environmentCountermeasures(envName))
      elif (goalDimName == 'requirement'):
        reqDict = self.dbProxy.getRequirements()
        descList = []
        for r in reqDict.values():
          descList.append(r.label())
        goalCtrl.SetItems(descList)


  def onSubGoalDimChange(self,evt):
    envCtrl = self.FindWindowById(GOALASSOCIATION_COMBOENVIRONMENT_ID)
    subGoalDimCtrl = self.FindWindowById(GOALASSOCIATION_COMBOSUBGOALDIM_ID)
    envName = envCtrl.GetStringSelection()
    subGoalDimName = subGoalDimCtrl.GetStringSelection()

    if (envName != '') and (subGoalDimName != ''):
      subGoalCtrl = self.FindWindowById(GOALASSOCIATION_COMBOSUBGOAL_ID)
      if (subGoalDimName == 'goal'):
        subGoalCtrl.SetItems(self.dbProxy.environmentGoals(envName))
      elif (subGoalDimName == 'obstacle'):
        subGoalCtrl.SetItems(self.dbProxy.environmentObstacles(envName))
      elif (subGoalDimName == 'domainproperty'):
        subGoalCtrl.SetItems(self.dbProxy.environmentDomainProperties(envName))
      elif (subGoalDimName == 'task'):
        subGoalCtrl.SetItems(self.dbProxy.environmentTasks(envName))
      elif (subGoalDimName == 'usecase'):
        subGoalCtrl.SetItems(self.dbProxy.environmentUseCases(envName))
      elif (subGoalDimName == 'countermeasure'):
        subGoalCtrl.SetItems(self.dbProxy.environmentCountermeasures(envName))
      elif (subGoalDimName == 'requirement'):
        reqDict = self.dbProxy.getRequirements()
        descList = []
        for r in reqDict.values():
          descList.append(r.label())
        subGoalCtrl.SetItems(descList)
      elif (subGoalDimName == 'role'):
        roleDict = self.dbProxy.getRoles()
        descList = []
        for r in roleDict.values():
          descList.append(r.name())
        subGoalCtrl.SetItems(descList)


  def parameters(self):
    parameters = GoalAssociationParameters(self.theEnvironmentName,self.theGoal,self.theGoalDimension,self.theGoalAssociationType,self.theSubGoal,self.theSubGoalDimension,self.theAlternativeFlag,self.theRationale)
    parameters.setId(self.theGoalAssociationId)
    return parameters
