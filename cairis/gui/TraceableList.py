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
import wx
from cairis.core.Borg import Borg
from TraceExplorer import TraceExplorer
from cairis.core.ARM import *

class TraceableList(wx.ListCtrl):

  def __init__(self,parent,winId,dimensionName):
    wx.ListCtrl.__init__(self,parent,winId,style=wx.LC_REPORT)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theTraceMenu = wx.Menu()
    self.theTraceMenu.Append(TRACE_MENUTRACE_TO_ID,'Supported by')
    self.theTraceMenu.Append(TRACE_MENUTRACE_FROM_ID,'Contributes to')
    wx.EVT_MENU(self,TRACE_MENUTRACE_FROM_ID,self.onAddContributionLink)
    wx.EVT_MENU(self,TRACE_MENUTRACE_TO_ID,self.onAddSupportLink)
    self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onRightClick)
    self.theDimensionName = dimensionName
    self.theParentDialog = parent

  def onRightClick(self,evt):
    selectItem = self.theTraceMenu.FindItemById(TRACE_MENUTRACE_FROM_ID)
    if (evt.GetIndex() == -1):
      selectItem.Enable(False)  
    else:
      selectItem.Enable(True)  
    self.PopupMenu(self.theTraceMenu)

  def selectedId(self):
    if (self.__class__.__name__ != 'ComponentListCtrl' and len(self.theParentDialog.objts) == 0):
      dlg = wx.MessageDialog(self,'No objects defined','Edit links', wx.OK | wx.ICON_EXCLAMATION)
      dlg.ShowModal()
      dlg.Destroy() 
      return -1
    else:
      selectedLabel = ''
      if self.__class__.__name__ != 'UseCaseListCtrl' and self.__class__.__name__ != 'ComponentListCtrl':
        selectedLabel = self.theParentDialog.selectedLabel
      else:
        selectedLabel = self.theSelectedLabel
      if (self.__class__.__name__ != 'ComponentListCtrl'):
        selectedObjt = self.theParentDialog.objts[selectedLabel]
      else:
        selectedObjt = self.theComponents[self.theSelectedIdx]

      return selectedObjt.id()

  def onAddContributionLink(self,evt):
    fromId = self.selectedId()
    if (fromId != -1):
      try:
        dlg = TraceExplorer(self,self.theDimensionName,True)
        if (dlg.ShowModal() == TRACE_BUTTONADD_ID):
          traceToDimension = dlg.toDimension()
          linkTable = self.theDimensionName + '_' + traceToDimension
          toId = dlg.toId()
          self.dbProxy.addTrace(linkTable,fromId,toId)
        dlg.Destroy()
      except ARMException,errorText:
        dlg = wx.MessageDialog(self,str(errorText),'Add Contribution Link',wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
        return

  def onAddSupportLink(self,evt):
    toId = self.selectedId()
    if (toId != -1):
      try:
        dlg = TraceExplorer(self,self.theDimensionName,False)
        if (dlg.ShowModal() == TRACE_BUTTONADD_ID):
          traceFromDimension = dlg.toDimension()
          linkTable = traceFromDimension + '_' + self.theDimensionName
          fromId = dlg.toId()
          self.dbProxy.addTrace(linkTable,fromId,toId)
        dlg.Destroy()
      except ARMException,errorText:
        dlg = wx.MessageDialog(self,str(errorText),'Add support link',wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
        return
