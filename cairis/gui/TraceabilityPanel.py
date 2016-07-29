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
from BasePanel import BasePanel
from cairis.core.Borg import Borg
from cairis.core.armid import *

__author__ = 'Shamal Faily'

class TraceabilityPanel(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,TRACEABILITY_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.traces = self.dbProxy.riskAnalysisModel(initContxt)

    mainSizer = wx.BoxSizer(wx.VERTICAL)
    columnList = ['From','Name','To','Name']
    mainSizer.Add(self.buildTraceListCtrl(self,TRACEABILITY_LISTTRACES_ID,columnList,self.traces),1,wx.EXPAND)
    mainSizer.Add(self.buildAddDeleteCloseButtonSizer(self,TRACEABILITY_BUTTONADD_ID,TRACEABILITY_BUTTONDELETE_ID,wx.HORIZONTAL),0,wx.EXPAND | wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)
