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
import cairis.core.AssetParametersFactory
from cairis.core.Borg import Borg
from DimensionNameDialog import DimensionNameDialog

from cairis.core.ARM import *

class TemplateAssetListCtrl(wx.ListCtrl):

  def __init__(self,parent,winId):
    wx.ListCtrl.__init__(self,parent,winId,style=wx.LC_REPORT)
    self.theParentDialog = parent
    self.theTraceMenu = wx.Menu()
    self.theTraceMenu.Append(TRACE_MENUTRACE_GENERATESPECIFIC_ID,'Situate')
    self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onRightClick)
    wx.EVT_MENU(self,TRACE_MENUTRACE_GENERATESPECIFIC_ID,self.onSituate)


  def onRightClick(self,evt):
    self.PopupMenu(self.theTraceMenu)

  def onSituate(self,evt):
    tAsset = self.theParentDialog.objts[self.theParentDialog.selectedLabel]
    taId = tAsset.id()
    taName = tAsset.name()
    try:
      b = Borg()
      dbProxy = b.dbProxy
      envs = dbProxy.getEnvironmentNames()
      cDlg = DimensionNameDialog(self,'environment',envs,'Select')
      if (cDlg.ShowModal() == DIMNAME_BUTTONACTION_ID):
        sitEnvs = cDlg.dimensionNames()
        assetId = dbProxy.addAsset(cairis.core.AssetParametersFactory.buildFromTemplate(taName,sitEnvs))
# NB: we don't add anything to asset_template_asset, as we only use this table when the derived asset is part of a situated pattern
        cDlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Situate template asset',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return
