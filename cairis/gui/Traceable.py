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
from cairis.core.ARM import *
import wx
from cairis.core.Borg import Borg
from TraceExplorer import TraceExplorer

__author__ = 'Shamal Faily'

class Traceable:
  def __init__(self):
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theTraceMenu = wx.Menu()
    self.theTraceMenu.Append(TRACE_MENUTRACE_TO_ID,'Supported by')
    self.theTraceMenu.Append(TRACE_MENUTRACE_FROM_ID,'Contributes to')
    wx.EVT_MENU(self,TRACE_MENUTRACE_FROM_ID,self.onAddContributionLink)
    wx.EVT_MENU(self,TRACE_MENUTRACE_TO_ID,self.onAddSupportLink)

  def onRightClick(self,evt):
    self.PopupMenu(self.theTraceMenu)

  def onTraceFrom(self,dimensionName,fromId,envName=''):
    self.onTrace(dimensionName,fromId,True,envName)

  def onTraceTo(self,dimensionName,toId):
    self.onTrace(dimensionName,toId,False,envName)

  def onTrace(self,dimensionName,fromId,isFrom,envName):
    dlg = TraceExplorer(self,dimensionName,isFrom,envName)
    if (dlg.ShowModal() == TRACE_BUTTONADD_ID):
      if (isFrom):
        traceDimension = dlg.fromDimension()
        traceLabel = dlg.label()
        linkTable = dimensionName + '_' + traceDimension
        toId = dlg.toId()
        self.dbProxy.addTrace(linkTable,fromId,toId,traceLabel)
      else: 
        traceDimension = dlg.toDimension()
        traceLabel = dlg.label()
        linkTable = traceDimension + '_' + dimensionName
        toId = dlg.toId()
        self.dbProxy.addTrace(linkTable,toId,fromId,traceLabel)
    dlg.Destroy()
