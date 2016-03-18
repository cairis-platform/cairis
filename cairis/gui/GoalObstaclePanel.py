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
from BasePanel import BasePanel
from Borg import Borg

class GoalObstaclePanel(BasePanel):
  def __init__(self,parent,goalName,obsName,envName):
    BasePanel.__init__(self,parent,armid.GOALOBSTACLE_ID)
    self.theAssetId = None
    b = Borg()
    self.dbProxy = b.dbProxy

    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(self.buildMLTextSizer('Goal',(87,30),armid.GOALOBSTACLE_TEXTGOAL_ID,True),1,wx.EXPAND)
    mainSizer.Add(self.buildMLTextSizer('Obstacle',(87,30),armid.GOALOBSTACLE_TEXTOBSTACLE_ID,True),1,wx.EXPAND)

    buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
    addButton = wx.Button(self,armid.GOALOBSTACLE_BUTTONADD_ID,"Add")
    buttonSizer.Add(addButton)
    ignoreButton = wx.Button(self,armid.GOALOBSTACLE_BUTTONIGNORE_ID,"Ignore")
    buttonSizer.Add(ignoreButton)
    mainSizer.Add(buttonSizer,0,wx.CENTER)

    goalId = b.dbProxy.getDimensionId(goalName,'template_goal')
    envId = b.dbProxy.getDimensionId(envName,'environment')
    goalDef = b.dbProxy.templateGoalDefinition(goalId)
    goalCtrl = self.FindWindowById(armid.GOALOBSTACLE_TEXTGOAL_ID)
    goalCtrl.SetValue(goalDef)

    obsId = b.dbProxy.getDimensionId(obsName,'obstacle')
    obsTuple = b.dbProxy.obstacleDefinition(obsId,envId)
    obsDef = obsTuple[0]
    obsCtrl = self.FindWindowById(armid.GOALOBSTACLE_TEXTOBSTACLE_ID)
    obsCtrl.SetValue(obsDef)

    self.SetSizer(mainSizer)
