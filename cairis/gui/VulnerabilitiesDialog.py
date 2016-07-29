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
import cairis.core.Vulnerability
import VulnerabilityDialog
from DialogClassParameters import DialogClassParameters
from DirectoryDialog import DirectoryDialog
import DimensionBaseDialog
from cairis.core.ARM import *

__author__ = 'Shamal Faily'

class VulnerabilitiesDialog(DimensionBaseDialog.DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.DimensionBaseDialog.__init__(self,parent,VULNERABILITIES_ID,'Vulnerabilities',(800,300),'vulnerability.png')
    idList = [VULNERABILITIES_VULNERABILITYLIST_ID,VULNERABILITIES_BUTTONADD_ID,VULNERABILITIES_BUTTONDELETE_ID]
    columnList = ['Name','Type']
    self.buildControls(idList,columnList,self.dbProxy.getVulnerabilities,'vulnerability')
    wx.EVT_BUTTON(self,CC_DIRECTORYIMPORT_ID,self.onImport)

    listCtrl = self.FindWindowById(VULNERABILITIES_VULNERABILITYLIST_ID)
    listCtrl.SetColumnWidth(0,300)
    listCtrl.SetColumnWidth(1,200)


  def addObjectRow(self,vulnerabilityListCtrl,listRow,vulnerability):
    vulnerabilityListCtrl.InsertStringItem(listRow,vulnerability.name())
    vulnerabilityListCtrl.SetStringItem(listRow,1,vulnerability.type())


  def onAdd(self,evt):
    try:
      assets = self.dbProxy.getDimensions('asset')
      if (len(assets) == 0):
        dlg = wx.MessageDialog(self,'Cannot add a vulnerability as no assets have been defined','Add vulnerability',wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        return
      addParameters = DialogClassParameters(VULNERABILITY_ID,'Add vulnerability',VulnerabilityDialog.VulnerabilityDialog,VULNERABILITY_BUTTONCOMMIT_ID,self.dbProxy.addVulnerability,True)
      self.addObject(addParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add vulnerability',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onImport(self,evt):
    try:
      assets = self.dbProxy.getDimensions('asset')
      if (len(assets) == 0):
        dlg = wx.MessageDialog(self,'Cannot import a vulnerability as no assets have been defined','Add vulnerability',wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        return
      dirDlg = DirectoryDialog(self,'vulnerability')
      if (dirDlg.ShowModal() == DIRECTORYDIALOG_BUTTONIMPORT_ID):
        objt = dirDlg.object()
        importParameters = DialogClassParameters(VULNERABILITY_ID,'Import vulnerability',VulnerabilityDialog.VulnerabilityDialog,VULNERABILITY_BUTTONCOMMIT_ID,self.dbProxy.addVulnerability,False)
        self.importObject(objt,importParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Import vulnerability',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    try:
      selectedObjt = self.objts[self.selectedLabel]
      updateParameters = DialogClassParameters(VULNERABILITY_ID,'Edit vulnerability',VulnerabilityDialog.VulnerabilityDialog,VULNERABILITY_BUTTONCOMMIT_ID,self.dbProxy.updateVulnerability,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit vulnerability',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No vulnerability','Delete vulnerability',self.dbProxy.deleteVulnerability)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete vulnerability',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy
