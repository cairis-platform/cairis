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
from EnvironmentListCtrl import EnvironmentListCtrl
from Borg import Borg

class RiskEnvironmentListCtrl(EnvironmentListCtrl):
  def __init__(self,parent,winId,dp):
    EnvironmentListCtrl.__init__(self,parent,winId,dp)
    self.theCurrentRisk = ''

  def setRisk(self,riskName):
    self.theCurrentRisk = riskName

  def onAddDimension(self,evt):
    currentDimensions = self.dimensions()
    dimensions = self.dbProxy.riskEnvironmentNames(self.theCurrentRisk)
    remainingDimensions = [x for x in dimensions if x not in currentDimensions]
    from DimensionNameDialog import DimensionNameDialog
    dlg = DimensionNameDialog(self,self.theDimensionTable,remainingDimensions,'Add')
    if (dlg.ShowModal() == armid.DIMNAME_BUTTONACTION_ID):
      for additionalDimension in dlg.dimensionNames():
        idx = self.GetItemCount()
        self.InsertStringItem(idx,additionalDimension)

