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


from cairis.core.armid import *
from Traceable import Traceable
import wx
from cairis.core.ARM import *
from RequirementHistoryDialog import RequirementHistoryDialog
from TraceExplorer import TraceExplorer
from cairis.core.GoalAssociationParameters import GoalAssociationParameters
from cairis.core.Borg import Borg

__author__ = 'Shamal Faily'

class EnvironmentGrid(Traceable):
  def __init__(self):
    Traceable.__init__(self)
    self.theTraceMenu.Enable(TRACE_MENUTRACE_TO_ID,False)
    self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.onRightClick)

  def onAddSupportLink(self,evt):
    pass

  def onAddContributionLink(self,evt):
    try:
      objtTable = self.GetTable()
      selectedObjt = (objtTable.om.objects())[self.GetGridCursorRow()]
      self.onTraceFrom(objtTable.dimension,selectedObjt.id(),objtTable.envName)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add contribution link',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onTrace(self,dimensionName,fromId,isFrom,envName):
    dlg = TraceExplorer(self,dimensionName,isFrom,envName)
    if (dlg.ShowModal() == TRACE_BUTTONADD_ID):
      objtTable = self.GetTable()
      objtName = ((objtTable.om.objects())[self.GetGridCursorRow()]).name()
      p = GoalAssociationParameters(envName,objtName,dimensionName,'and',dlg.toValue(),dlg.toDimension(),0,'')
      self.dbProxy.addGoalAssociation(p)
    dlg.Destroy()
