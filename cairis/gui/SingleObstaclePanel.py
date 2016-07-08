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
import cairis.core.Obstacle
from cairis.core.Borg import Borg
from ObstacleEnvironmentNotebook import ObstacleEnvironmentNotebook

class SingleObstaclePanel(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,OBSTACLE_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Name',(87,30),OBSTACLE_TEXTNAME_ID),0,wx.EXPAND)
    self.nameCtrl = self.FindWindowById(OBSTACLE_TEXTNAME_ID)
    self.notebook = ObstacleEnvironmentNotebook(self,self.dbProxy)

    mainSizer.Add(self.notebook,1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildCommitButtonSizer(self,OBSTACLE_BUTTONCOMMIT_ID,True),0,wx.CENTER)
    self.definitionCtrl = self.notebook.FindWindowById(OBSTACLE_TEXTDEFINITION_ID)
    self.categoryCtrl = self.notebook.FindWindowById(OBSTACLE_COMBOCATEGORY_ID)
    self.goalAssociationCtrl = self.notebook.FindWindowById(OBSTACLE_LISTGOALS_ID)
    self.subGoalAssociationCtrl = self.notebook.FindWindowById(OBSTACLE_LISTSUBGOALS_ID)
    self.cCtrl = self.notebook.FindWindowById(OBSTACLE_LISTCONCERNS_ID)
    self.SetSizer(mainSizer)
