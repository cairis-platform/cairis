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


import ARM
from Borg import Borg
from GoalEnvironmentProperties import GoalEnvironmentProperties
from Goal import Goal
from GoalParameters import GoalParameters


class GoalManager:  

  def __init__(self,goalCombo,envCombo):
    b = Borg()
    self.dbProxy = b.dbProxy
    self.goalCombo = goalCombo
    self.envCombo = envCombo
    envName = self.envCombo.GetValue()
    goalName = self.goalCombo.GetValue()
    self.goals = self.dbProxy.getEnvironmentGoals(goalName,envName)

  def __getitem__(self,goalId):
    return self.goals[goalId]

  def objects(self):
    return self.goals

  def environment(self):
    return self.dbProxy.environmentId

  def size(self):
    return len(self.goals)

  def update(self,label,attr,value):
    idx,goal = self.goalByLabel(label)
    goal.update(attr,value)    

  def commitChanges(self):
    envName = self.envCombo.GetValue()
    for g in self.goals:
      self.dbProxy.updateEnvironmentGoal(g,envName)
        
  def labelIndex(self,label):
    x = 0
    for key, r in enumerate(self.goals):
      if (r.label() == label):
        return x
      else:
        x += 1
 
  def goalById(self,id):
    for idx,r in enumerate(self.goals):
      if (str(r.id()) == str(id)):
        return (idx,r)
    exceptionText = 'Parent Goal ' + str(id) + ' does not exist'
    raise ARM.RequirementDoesNotExist(exceptionText)
 
  def posByGoal(self,id):
    for idx,r in enumerate(self.goals):
      if (str(r.id()) == str(id)):
        return idx
    exceptionText = 'Goal ' + str(id) + ' does not exist'
    raise ARM.RequirementDoesNotExist(exceptionText)

  def goalByLabel(self,label):
    for idx,r in enumerate(self.goals):
      if (r.label() == label):
        return (idx,r)

  def add(self,idx=-1,goalName="",envName="",newDefinition="",newCategory="Maintain", newPriority="Low", newFitCriterion="None", newIssue="None", newOriginator=""):
    envName = self.envCombo.GetValue()
    parentGoalName = self.goalCombo.GetValue()

    ep = GoalEnvironmentProperties(envName,'',newDefinition,newCategory,newPriority,newFitCriterion,newIssue,[(parentGoalName,'goal','and','No','None')])
    g = Goal(-1,goalName,newOriginator,[],[ep])
    gp = GoalParameters(goalName,newOriginator,[],[ep])
    g.setId(self.dbProxy.addGoal(gp))
    if (idx != -1):
      self.goals.insert(idx,g)
    else:
      self.goals.append(g)
    return g

  def delete(self,idx):
    g = self.goals[idx]
    goalId = g.id()
    self.goals.remove(g)    
    self.dbProxy.deleteGoal(goalId)
    return 1

  def asString(self):
    for g in self.goals:
      print g.asString()
