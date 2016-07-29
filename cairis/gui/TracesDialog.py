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
from cairis.core.ObjectFactory import *
from cairis.core.armid import *
import cairis.core.Trace
import TraceDialog
import DialogClassParameters
import TraceDialogParameters
import DimensionBaseDialog
from cairis.core.ARM import *

__author__ = 'Shamal Faily'

class TracesDialog(DimensionBaseDialog.DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.DimensionBaseDialog.__init__(self,parent,TRACES_ID,'Traces',(800,300))
    self.traces = self.dbProxy.riskAnalysisModel()
    idList = [TRACES_LISTTRACES_ID,TRACES_BUTTONADD_ID,TRACES_BUTTONDELETE_ID]
    columnList = ['From','Description','To','Description']
    self.buildControls(idList,columnList,0,'trace')

  def addObjectRow(self,listCtrl,listRow,trace):
    listCtrl.InsertStringItem(listRow,trace.fromObject())
    listCtrl.SetStringItem(listRow,1,trace.fromName())
    listCtrl.SetStringItem(listRow,2,trace.toObject())
    listCtrl.SetStringItem(listRow,3,trace.toName())

  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters.DialogClassParameters(TRACE_ID,'Add trace',TraceDialog.TraceDialog,TRACE_BUTTONCOMMIT_ID,self.dbProxy.addTrace,True)
      self.addObject(addParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add trace',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedIdx = evt.GetIndex()
    selectedObjt = self.traces[selectedIdx]
    try:
      updateParameters = TraceDialogParameters.TraceDialogParameters(TRACE_ID,'Edit trace',TraceDialog.TraceDialog,TRACE_BUTTONCOMMIT_ID,self.dbProxy.updateTrace,False,selectedObjt.fromObject(),selectedObjt.fromId(),selectedObjt.toObject(),selectedObjt.toId())
      self.updateObject(selectedObjt,updateParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit trace',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy


  def onDelete(self,evt):
    if len(self.selectedLabel) == 0:
      dlg = wx.MessageDialog(self,'No trace','Delete trace',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
    else:
      objtToGo = self.traces[self.selectedIdx]
      del self.traces[self.selectedIdx]
      self.dbProxy.deleteTrace(objtToGo.fromId(),objtToGo.toId())
      listCtrl = self.FindWindowById(self.listId)
      listCtrl.DeleteItem(self.selectedIdx)
      self.selectedLabel = ''
    return

  def addObjectToDialog(self,objtId,listId,dialogParameters):
    listCtrl = self.FindWindowById(self.listId)
    listRow = listCtrl.GetItemCount()
    newObjt = cairis.core.ObjectFactory.build(objtId,dialogParameters)
    self.addObjectRow(listCtrl,listRow,newObjt)
    self.traces.append(newObjt)

  def updateDialogObject(self,objtId,listId,dialogParameters):
    objtToGo = self.traces[self.selectedIdx]
    del self.traces[self.selectedIdx]
    listCtrl = self.FindWindowById(self.listId)
    listCtrl.DeleteItem(self.selectedIdx)
    updatedObjt = cairis.core.ObjectFactory.build(-1,dialogParameters)
    self.addObjectRow(listCtrl,self.selectedIdx,updatedObjt)
    self.traces.insert(self.selectedIdx,updatedObjt)
