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
import cairis.core.Goal
from cairis.core.Borg import Borg
from GoalEnvironmentNotebook import GoalEnvironmentNotebook

class SingleGoalPanel(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,GOAL_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Name',(87,30),GOAL_TEXTNAME_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Originator',(87,30),GOAL_TEXTORIGINATOR_ID),0,wx.EXPAND)
    self.nameCtrl = self.FindWindowById(GOAL_TEXTNAME_ID)
    self.notebook = GoalEnvironmentNotebook(self,self.dbProxy,True)

    mainSizer.Add(self.notebook,1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildCommitButtonSizer(self,GOAL_BUTTONCOMMIT_ID,True),0,wx.CENTER)
    self.definitionCtrl = self.notebook.FindWindowById(GOAL_TEXTDEFINITION_ID)
    self.categoryCtrl = self.notebook.FindWindowById(GOAL_COMBOCATEGORY_ID)
    self.priorityCtrl = self.notebook.FindWindowById(GOAL_COMBOPRIORITY_ID)
    self.fitCriterionCtrl = self.notebook.FindWindowById(GOAL_TEXTFITCRITERION_ID)
    self.issueCtrl = self.notebook.FindWindowById(GOAL_TEXTISSUE_ID)
    self.goalAssociationCtrl = self.notebook.FindWindowById(GOAL_LISTGOALREFINEMENTS_ID)
    self.subGoalAssociationCtrl = self.notebook.FindWindowById(GOAL_LISTSUBGOALREFINEMENTS_ID)
    self.cCtrl = self.notebook.FindWindowById(GOAL_LISTCONCERNS_ID)
    self.caCtrl = self.notebook.FindWindowById(GOAL_LISTCONCERNASSOCIATIONS_ID)
    self.ctCtrl = self.notebook.FindWindowById(GOAL_COMBOCONTRIBUTIONTYPE_ID)
    self.SetSizer(mainSizer)
