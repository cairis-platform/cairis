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
from ThreatDialog import ThreatDialog
from DialogClassParameters import DialogClassParameters
from DirectoryDialog import DirectoryDialog
import DimensionBaseDialog
from cairis.core.ARM import *

__author__ = 'Shamal Faily'

class ThreatsDialog(DimensionBaseDialog.DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.DimensionBaseDialog.__init__(self,parent,THREATS_ID,'Threats',(800,300),'threat.png')
    idList = [THREATS_THREATLIST_ID,THREATS_BUTTONADD_ID,THREATS_BUTTONDELETE_ID]
    columnList = ['Name','Type']
    self.buildControls(idList,columnList,self.dbProxy.getThreats,'threat')
    wx.EVT_BUTTON(self,CC_DIRECTORYIMPORT_ID,self.onImport)
    listCtrl = self.FindWindowById(THREATS_THREATLIST_ID)
    listCtrl.SetColumnWidth(0,300)
    listCtrl.SetColumnWidth(1,300)


  def addObjectRow(self,threatListCtrl,listRow,threat):
    threatListCtrl.InsertStringItem(listRow,threat.name())
    threatListCtrl.SetStringItem(listRow,1,threat.type())

  def onAdd(self,evt):
    try:
      attackers = self.dbProxy.getDimensions('attacker')
      assets = self.dbProxy.getDimensions('asset')
      if (len(attackers) == 0):
        dlg = wx.MessageDialog(self,'Cannot add a threat as no attackers have been defined','Add threat',wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        return
      elif (len(assets) == 0):
        dlg = wx.MessageDialog(self,'Cannot add a threat as no assets have been defined','Add threat',wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        return
      addParameters = DialogClassParameters(THREAT_ID,'Add threat',ThreatDialog,THREAT_BUTTONCOMMIT_ID,self.dbProxy.addThreat,True)
      self.addObject(addParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add threat',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onImport(self,evt):
    try:
      assets = self.dbProxy.getDimensions('asset')
      if (len(assets) == 0):
        dlg = wx.MessageDialog(self,'Cannot import a threat as no assets have been defined','Add threat',wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        return
      dirDlg = DirectoryDialog(self,'threat')
      if (dirDlg.ShowModal() == DIRECTORYDIALOG_BUTTONIMPORT_ID):
        objt = dirDlg.object()
        importParameters = DialogClassParameters(THREAT_ID,'Import threat',ThreatDialog,THREAT_BUTTONCOMMIT_ID,self.dbProxy.addThreat,False)
        self.importObject(objt,importParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Import threat',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    try:
      selectedObjt = self.objts[self.selectedLabel]
      updateParameters = DialogClassParameters(THREAT_ID,'Edit threat',ThreatDialog,THREAT_BUTTONCOMMIT_ID,self.dbProxy.updateThreat,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Update threat',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No threat','Delete threat',self.dbProxy.deleteThreat)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete threat',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy
