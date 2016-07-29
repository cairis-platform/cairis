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

__author__ = 'Shamal Faily'

class AssignResponsibilityNodeDialog:
  def __init__(self,objt,environmentName,builder,goalName,isGoal = True):
    self.window = builder.get_object("AssignResponsibilityNodeDialog")
    b = Borg()
    self.isGoalIndicator = isGoal
    self.dbProxy = b.dbProxy
    self.theEnvironmentName = environmentName
    self.theGoalName = goalName
    self.decorator = NDImplementationDecorator(builder)
    self.theObjtId = objt.id()

    roles = self.dbProxy.getDimensionNames('role')
    self.decorator.updateComboCtrl("roleRespNameCtrl",roles,'')
    self.window.resize(350,200)

  def on_roleResponsibilityOkButton_clicked(self,callback_data):
    roleName = self.decorator.getComboValue("roleRespNameCtrl")
    if (self.isGoalIndicator == False):
      roleId = self.dbProxy.getDimensionId(roleName,'role')
      self.dbProxy.addTrace('requirement_role',self.theObjtId,roleId)
    else: 
      goalDim = 'goal'
      if (self.isGoalIndicator == False):
        goalDim = 'requirement'
      parameters = GoalAssociationParameters(self.theEnvironmentName,self.theGoalName,goalDim,'responsible',roleName,'role')
      self.dbProxy.addGoalAssociation(parameters)
    self.window.destroy()

  def show(self):
    self.window.show()
