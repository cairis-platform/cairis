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
from cairis.core.GoalAssociationParameters import GoalAssociationParameters
from NDImplementationDecorator import NDImplementationDecorator

class GoalRefinementNodeDialog:
  def __init__(self,objt,environmentName,builder,goalIndicator,gName,reqIndicator = False):
    self.window = builder.get_object("GoalRefinementNodeDialog")
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theEnvironmentName = environmentName
    self.decorator = NDImplementationDecorator(builder)
    self.reqIndicator = reqIndicator

    refTypes = ['and','or']
    goals = self.dbProxy.environmentGoals(self.theEnvironmentName)
    if (self.reqIndicator == True):
      refTypes = ['and']
      goals = self.dbProxy.getDimensionNames('requirement')

    self.decorator.updateComboCtrl("goalRefNameCtrl",goals,'')
    self.decorator.updateComboCtrl("goalRefinementCtrl",refTypes,'')
    self.decorator.updateButtonLabel("goalRefinementOkButton","Create")
    self.window.resize(350,200)
    self.goalIndicator = goalIndicator
    self.inputGoalName = gName

  def on_goalRefinementOkButton_clicked(self,callback_data):
    goalName = self.decorator.getComboValue("goalRefNameCtrl")
    assocType = self.decorator.getComboValue("goalRefinementCtrl")
    if (self.reqIndicator == True):
      parameters = GoalAssociationParameters(self.theEnvironmentName,self.inputGoalName,'goal','and',goalName,'requirement')
    elif (self.goalIndicator == True):
      parameters = GoalAssociationParameters(self.theEnvironmentName,goalName,'goal',assocType,self.inputGoalName,'goal')
    else:
      parameters = GoalAssociationParameters(self.theEnvironmentName,self.inputGoalName,'goal',assocType,goalName,'goal')
    self.dbProxy.addGoalAssociation(parameters)
    self.window.destroy()

  def show(self):
    self.window.show()
