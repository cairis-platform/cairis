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
import GoalFactory
from Borg import Borg
from ARM import *

class ResponseListCtrl(wx.ListCtrl):

  def __init__(self,parent,winId):
    wx.ListCtrl.__init__(self,parent,winId,style=wx.LC_REPORT)
    self.theParentDialog = parent
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theTraceMenu = wx.Menu()
    self.theTraceMenu.Append(armid.TRACE_MENUTRACE_GENERATESPECIFIC_ID,'Generate Goal')
    wx.EVT_MENU(self,armid.TRACE_MENUTRACE_GENERATESPECIFIC_ID,self.onSelectGenerate)
    self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onRightClick)


  def onRightClick(self,evt):
    generateItem = self.theTraceMenu.FindItemById(armid.TRACE_MENUTRACE_GENERATESPECIFIC_ID)
    if (evt.GetIndex() == -1):
      generateItem.Enable(False)
    else:
      response = self.theParentDialog.objts[self.theParentDialog.selectedLabel]
      if (response.responseType() == 'Mitigate'):
        generateItem.Enable(True)
      else:
        generateItem.Enable(False)
    self.PopupMenu(self.theTraceMenu)

  def onSelectGenerate(self,evt):
    response = self.theParentDialog.objts[self.theParentDialog.selectedLabel]
    try:
      if (self.dbProxy.existingResponseGoal(response.id())):
        dlg = wx.MessageDialog(self,'A goal has already been generated for this response','Generate response goal',wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        return
      else:
        goalParameters = GoalFactory.build(response)
        riskParameters = goalParameters[0]
        riskGoalId = self.dbProxy.addGoal(riskParameters)
        self.dbProxy.addTrace('response_goal',response.id(),riskGoalId)
        if (goalParameters > 1):
          threatParameters = goalParameters[1]
          vulnerabilityParameters = goalParameters[2]
          self.dbProxy.addGoal(vulnerabilityParameters)
          self.dbProxy.addGoal(threatParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Generate response goal',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return
