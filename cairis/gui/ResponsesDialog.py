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
import cairis.core.Risk
from ResponseDialog import ResponseDialog
from DialogClassParameters import DialogClassParameters
from ResponseDialogParameters import ResponseDialogParameters
from AcceptEnvironmentPanel import AcceptEnvironmentPanel
from TransferEnvironmentPanel import TransferEnvironmentPanel
from MitigateEnvironmentPanel import MitigateEnvironmentPanel
from DimensionBaseDialog import DimensionBaseDialog
from cairis.core.ARM import *

__author__ = 'Shamal Faily'

class ResponsesDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,RESPONSES_ID,'Responses',(800,300),'response.png')
    self.theMainWindow = parent
    idList = [RESPONSES_LISTRESPONSES_ID,RESPONSES_BUTTONADD_ID,RESPONSES_BUTTONDELETE_ID]
    columnList = ['Name','Type']
    self.buildControls(idList,columnList,self.dbProxy.getResponses,'response')
    listCtrl = self.FindWindowById(RESPONSES_LISTRESPONSES_ID)
    listCtrl.SetColumnWidth(0,300)


  def addObjectRow(self,mitListCtrl,listRow,response):
    mitListCtrl.InsertStringItem(listRow,response.name())
    mitListCtrl.SetStringItem(listRow,1,response.__class__.__name__)

  def onAdd(self,evt):
    try:
      riskDict = self.dbProxy.getDimensionNames('risk')
      if (len(riskDict) == 0):
        dlg = wx.MessageDialog(self,'Cannot mitigate for non-existing risks','Add response',wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        return
      responseTypes = ['Accept','Transfer','Mitigate']
      from DimensionNameDialog import DimensionNameDialog
      rtDlg = DimensionNameDialog(self,'response',responseTypes,'Select',(300,200))
      if (rtDlg.ShowModal() == DIMNAME_BUTTONACTION_ID):
        responseType = rtDlg.dimensionName()
        responsePanel = MitigateEnvironmentPanel
        if (responseType == 'Accept'):
          responsePanel = AcceptEnvironmentPanel
        elif (responseType == 'Transfer'):
          responsePanel = TransferEnvironmentPanel
        addParameters = ResponseDialogParameters(RESPONSE_ID,'Add response',ResponseDialog,RESPONSE_BUTTONCOMMIT_ID,self.dbProxy.addResponse,True,responsePanel,responseType)
        self.addObject(addParameters)
      rtDlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add response',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    try:
      selectedObjt = self.objts[self.selectedLabel]
      responseType = selectedObjt.responseType()
      responsePanel = MitigateEnvironmentPanel
      if (responseType == 'Accept'):
        responsePanel = AcceptEnvironmentPanel
      elif (responseType == 'Transfer'):
        responsePanel = TransferEnvironmentPanel
      updateParameters = ResponseDialogParameters(RESPONSE_ID,'Edit response',ResponseDialog,RESPONSE_BUTTONCOMMIT_ID,self.dbProxy.updateResponse,False,responsePanel,responseType)
      self.updateObject(selectedObjt,updateParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit response',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.dbProxy.associateGrid(self.theMainWindow.FindWindowById(ID_REQGRID))
      self.deleteObject('No response','Delete response',self.dbProxy.deleteResponse)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete response',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
