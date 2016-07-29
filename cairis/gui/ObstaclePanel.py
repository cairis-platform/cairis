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
from BasePanel import BasePanel
from ObstacleEnvironmentPanel import ObstacleEnvironmentPanel

__author__ = 'Shamal Faily'

class ObstaclePanel(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,OBSTACLE_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    
  def buildControls(self,isCreate,isUpdateable=True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(self.buildTextSizer('Name',(87,30),OBSTACLE_TEXTNAME_ID),0,wx.EXPAND)
    mainSizer.Add(self.buildTagCtrlSizer((87,30),OBSTACLE_TAGS_ID),0,wx.EXPAND)
    mainSizer.Add(self.buildTextSizer('Originator',(87,30),OBSTACLE_TEXTORIGINATOR_ID),0,wx.EXPAND)
    self.environmentPanel = ObstacleEnvironmentPanel(self,self.dbProxy)
    mainSizer.Add(self.environmentPanel,1,wx.EXPAND)
    if (isUpdateable):
      mainSizer.Add(self.buildCommitButtonSizer(OBSTACLE_BUTTONCOMMIT_ID,isCreate),0,wx.CENTER)
    self.SetSizer(mainSizer)

  def loadControls(self,obstacle,isReadOnly=False):
    self.theObstacleId = obstacle.id()
    self.theObstacleOriginator = obstacle.originator()
    nameCtrl = self.FindWindowById(OBSTACLE_TEXTNAME_ID)
    tagsCtrl = self.FindWindowById(OBSTACLE_TAGS_ID)
    tagsCtrl.set(obstacle.tags())
    origCtrl = self.FindWindowById(OBSTACLE_TEXTORIGINATOR_ID)
    environmentCtrl = self.FindWindowById(OBSTACLE_PANELENVIRONMENT_ID)
    nameCtrl.SetValue(obstacle.name())
    origCtrl.SetValue(obstacle.originator())
    environmentCtrl.loadControls(obstacle)
