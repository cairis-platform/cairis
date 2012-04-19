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
from Borg import Borg
from WeaknessAnalysisDialog import WeaknessAnalysisDialog
from DimensionNameDialog import DimensionNameDialog
import AssetParametersFactory
from ARM import *

class ComponentViewListCtrl(wx.ListCtrl):

  def __init__(self,parent,winId):
    wx.ListCtrl.__init__(self,parent,winId,style=wx.LC_REPORT)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theParentDialog = parent
    self.theTraceMenu = wx.Menu()
    self.theTraceMenu.Append(armid.TRACE_MENUTRACE_GENERATESPECIFIC_ID,'Situate view')
    wx.EVT_MENU(self,armid.TRACE_MENUTRACE_GENERATESPECIFIC_ID,self.onSituate)
    self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onRightClick)


  def onRightClick(self,evt):
    self.PopupMenu(self.theTraceMenu)

  def onSituate(self,evt):
    cvObjt = self.theParentDialog.objts[self.theParentDialog.selectedLabel]
    cvName = cvObjt.name()
    try:
      environments = self.dbProxy.getDimensionNames('environment',False)
      cDlg = DimensionNameDialog(self,'environment',environments,'Select')
      if (cDlg.ShowModal() == armid.DIMNAME_BUTTONACTION_ID):
        envName = cDlg.dimensionName()
        dlg = WeaknessAnalysisDialog(self,cvName,envName)
        if (dlg.ShowModal() == armid.WEAKNESSANALYSIS_BUTTONCOMMIT_ID):
          self.situateComponentView(cvName,envName,dlg.targets())
        dlg.Destroy()
      cDlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Situate component view',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def situateComponentView(self,cvName,envName,targets):
    assetParametersList = []
    componentAssets = self.dbProxy.componentAssets(cvName)
    
    acDict = {}
    for assetName,componentName in componentAssets:
      assetParametersList.append(AssetParametersFactory.buildFromTemplate(assetName,[envName]))
      if assetName not in acDict:
        acDict[assetName] = componentName
    self.dbProxy.situateComponentView(cvName,envName,acDict,assetParametersList,targets)
    self.theParentDialog.theMainWindow.updateObjectSelection()
