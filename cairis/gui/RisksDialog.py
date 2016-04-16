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
from RiskDialog import RiskDialog
from DialogClassParameters import DialogClassParameters
from DimensionBaseDialog import DimensionBaseDialog
from cairis.core.ARM import *

class RisksDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,RISKS_ID,'Risks',(800,300),'risk.png')
    idList = [RISKS_LISTRISKS_ID,RISKS_BUTTONADD_ID,RISKS_BUTTONDELETE_ID]
    columnList = ['Name']
    self.buildControls(idList,columnList,self.dbProxy.getRisks,'risk')
    listCtrl = self.FindWindowById(RISKS_LISTRISKS_ID)
    listCtrl.SetColumnWidth(0,600)


  def addObjectRow(self,riskListCtrl,listRow,risk):
    riskListCtrl = self.FindWindowById(RISKS_LISTRISKS_ID)
    riskListCtrl.InsertStringItem(listRow,risk.name())

  def onAdd(self,evt):
    try:
      threats = self.dbProxy.getDimensions('threat')
      vulnerabilities = self.dbProxy.getDimensions('vulnerability')
      if (len(threats) == 0):
        dlg = wx.MessageDialog(self,'Cannot add a risk as no threats have been defined','Add risk',wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        return
      elif (len(vulnerabilities) == 0):
        dlg = wx.MessageDialog(self,'Cannot add a risk as no vulnerabilities have been defined','Add risk',wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        return
      addParameters = DialogClassParameters(RISK_ID,'Add risk',RiskDialog,RISK_BUTTONCOMMIT_ID,self.dbProxy.addRisk,True)
      self.addObject(addParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add risk',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()

  def onUpdate(self,evt):
    try:
      selectedObjt = self.objts[self.selectedLabel]
      updateParameters = DialogClassParameters(VULNERABILITY_ID,'Edit risk',RiskDialog,RISK_BUTTONCOMMIT_ID,self.dbProxy.updateRisk,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit risk',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No risk','Delete risk',self.dbProxy.deleteRisk)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete risk',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy
