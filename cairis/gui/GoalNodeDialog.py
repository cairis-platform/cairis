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


import sys
import gtk
from cairis.core.Borg import Borg
from cairis.core.GoalParameters import GoalParameters
from cairis.core.GoalAssociationParameters import GoalAssociationParameters
from cairis.core.GoalEnvironmentProperties import GoalEnvironmentProperties
from NDImplementationDecorator import NDImplementationDecorator

class GoalNodeDialog:
  def __init__(self,objt,environmentName,dupProperty,overridingEnvironment,builder):
    self.window = builder.get_object("GoalNodeDialog")
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theEnvironmentName = environmentName
    self.theGoalAssociation = None
    self.theGoalId = -1
    self.decorator = NDImplementationDecorator(builder)
    goalCategories = self.dbProxy.getDimensionNames('goal_category_type')
    priorityTypes = self.dbProxy.getDimensionNames('priority_type')
    self.goalAssociations = []
    self.subGoalAssociations= []
    if (objt == None):
      self.decorator.updateComboCtrl("goalCategoryCtrl",goalCategories,'')
      self.decorator.updateComboCtrl("goalPriorityCtrl",priorityTypes,'')
      self.decorator.updateButtonLabel("goalOkButton","Create")
      self.isCreate = True
    else:
      self.theGoalId = objt.id()
      envProperty = objt.environmentProperty(self.theEnvironmentName)
      self.goalAssociations = envProperty.goalRefinements()
      self.subGoalAssociations = envProperty.subGoalRefinements()
      self.decorator.updateTextCtrl("goalNameCtrl",objt.name())
      self.decorator.updateMLTextCtrl("goalDefinitionCtrl",objt.definition(environmentName,dupProperty))
      self.decorator.updateComboCtrl("goalCategoryCtrl",goalCategories,objt.category(environmentName,dupProperty))
      self.decorator.updateComboCtrl("goalPriorityCtrl",priorityTypes,objt.priority(environmentName,dupProperty))
      self.decorator.updateMLTextCtrl("goalFitCriterionCtrl",objt.fitCriterion(environmentName,dupProperty))
      self.decorator.updateMLTextCtrl("goalIssueCtrl",objt.issue(environmentName,dupProperty))
      self.decorator.updateButtonLabel("goalOkButton","Update")
      self.isCreate = False
    self.window.resize(350,600)


  def environmentProperties(self):
    goalDef = self.decorator.getMLText("goalDefinitionCtrl")
    goalCat = self.decorator.getComboValue("goalCategoryCtrl")
    goalPri = self.decorator.getComboValue("goalPriorityCtrl")
    goalFC = self.decorator.getMLText("goalFitCriterionCtrl")
    goalIssue = self.decorator.getMLText("goalIssueCtrl")
    envProperties = GoalEnvironmentProperties(self.theEnvironmentName,'',goalDef,goalCat,goalPri,goalFC,goalIssue,self.goalAssociations,self.subGoalAssociations)
    return envProperties

  def newGoalParameters(self):
    goalName = self.decorator.getText("goalNameCtrl")
    envProperties = self.environmentProperties()
    parameters = GoalParameters(goalName,'None',[],[envProperties]) 
    parameters.setId(self.theGoalId)
    return parameters

  def existingGoalParameters(self):
    goalName = self.decorator.getText("goalNameCtrl")
    modifiedProperties = self.environmentProperties()
    goalEnvProperties = self.dbProxy.goalEnvironmentProperties(self.theGoalId)
    for idx,p in enumerate(goalEnvProperties):
      if (p.name() == self.theEnvironmentName):
        goalEnvProperties[idx] = modifiedProperties
    parameters = GoalParameters(goalName,'None',[],goalEnvProperties) 
    parameters.setId(self.theGoalId)
    return parameters

  def parentGoal(self,goalName,assocType):
    self.theGoalAssociation = GoalAssociationParameters(self.theEnvironmentName,goalName,'goal',assocType)

  def on_goalOkButton_clicked(self,callback_data):
    if (self.isCreate):
      parameters = self.newGoalParameters()
      self.dbProxy.addGoal(parameters)
      self.theGoalAssociation.theSubGoal = parameters.name()
      self.theGoalAssociation.theSubGoalDimension = 'goal'
      self.theGoalAssociation.theAlternativeId = 0
      self.theGoalAssociation.theRationale = ''
      self.dbProxy.addGoalAssociation(self.theGoalAssociation)
    else:
      parameters = self.existingGoalParameters()
      self.dbProxy.updateGoal(parameters)
    self.window.destroy()

  def show(self):
    self.window.show()
