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
from cairis.core.ARM import *
from GoalObstaclePanel import GoalObstaclePanel

__author__ = 'Shamal Faily'

class GoalObstacleDialog(wx.Dialog):
  def __init__(self,parent,goalName,obsName,envName):
    wx.Dialog.__init__(self,parent,-1, goalName + ' / ' + obsName + ' in ' + envName,style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,300))
    
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = GoalObstaclePanel(self,goalName,obsName,envName)
    self.theIgnoreFlag = True
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,GOALOBSTACLE_BUTTONADD_ID,self.onAdd)
    wx.EVT_BUTTON(self,GOALOBSTACLE_BUTTONIGNORE_ID,self.onIgnore)

  def onAdd(self,evt):
    self.theIgnoreFlag = False
    self.EndModal(GOALOBSTACLE_BUTTONCOMMIT_ID)

  def onIgnore(self,evt):
    self.theIgnoreFlag = True
    self.EndModal(GOALOBSTACLE_BUTTONCOMMIT_ID)
 
  def ignore(self): return self.theIgnoreFlag
