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
from cairis.core.Borg import Borg
from SecurityPatternEnvironmentDialog import SecurityPatternEnvironmentDialog
import cairis.core.AssetParametersFactory
from cairis.core.ARM import *

class SecurityPatternListCtrl(wx.ListCtrl):

  def __init__(self,parent,winId):
    wx.ListCtrl.__init__(self,parent,winId,style=wx.LC_REPORT)
    self.theParentDialog = parent
    self.theTraceMenu = wx.Menu()
    self.theTraceMenu.Append(TRACE_MENUTRACE_GENERATESPECIFIC_ID,'Situate pattern')
    wx.EVT_MENU(self,TRACE_MENUTRACE_GENERATESPECIFIC_ID,self.onSituate)
    self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onRightClick)


  def onRightClick(self,evt):
    self.PopupMenu(self.theTraceMenu)

  def onSituate(self,evt):
    spObjt = self.theParentDialog.objts[self.theParentDialog.selectedLabel]
    patternId = spObjt.id()
    try:
      dlg = SecurityPatternEnvironmentDialog(self,patternId)
      if (dlg.ShowModal() == SPENVIRONMENT_BUTTONCOMMIT_ID):
        self.situatePattern(patternId,dlg.assetEnvironments())
      dlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Situate security pattern',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def situatePattern(self,patternId,assetEnvs):
    assetParametersList = []
    for assetName,envs in assetEnvs.iteritems():
      assetParametersList.append(cairis.core.AssetParametersFactory.buildFromTemplate(assetName,envs))
    b = Borg()
    b.dbProxy.addSituatedAssets(patternId,assetParametersList)
    self.theParentDialog.theMainWindow.updateObjectSelection()
