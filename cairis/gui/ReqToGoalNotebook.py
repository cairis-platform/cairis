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
from GoalPage import GoalPage

class ReqToGoalNotebook(wx.Notebook):
  def __init__(self,parent,dp):
    wx.Notebook.__init__(self,parent,GOAL_NOTEBOOKENVIRONMENT_ID)
    p1 = GoalPage(self,GOAL_LISTGOALREFINEMENTS_ID,True,dp)
    p2 = GoalPage(self,GOAL_LISTSUBGOALREFINEMENTS_ID,False,dp)
    self.AddPage(p1,'Goals')
    self.AddPage(p2,'Sub-Goals')
