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
from ImpliedProcessDialog import ImpliedProcessDialog
from DialogClassParameters import DialogClassParameters
from cairis.core.ARM import *
from DimensionBaseDialog import DimensionBaseDialog

__author__ = 'Shamal Faily'

class ImpliedProcessesDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,IMPLIEDPROCESSES_ID,'Implied Processes',(800,300),'code.png')
    idList = [IMPLIEDPROCESSES_IMPLIEDPROCESSLIST_ID,IMPLIEDPROCESSES_BUTTONADD_ID,IMPLIEDPROCESSES_BUTTONDELETE_ID]
    columnList = ['Name','Persona','Description']
    self.buildControls(idList,columnList,self.dbProxy.getImpliedProcesses,'persona_implied_process')
    listCtrl = self.FindWindowById(IMPLIEDPROCESSES_IMPLIEDPROCESSLIST_ID)
    listCtrl.SetColumnWidth(0,100)
    listCtrl.SetColumnWidth(1,100)
    listCtrl.SetColumnWidth(2,400)


  def addObjectRow(self,listCtrl,listRow,ip):
    listCtrl.InsertStringItem(listRow,ip.name())
    listCtrl.SetStringItem(listRow,1,ip.persona())
    listCtrl.SetStringItem(listRow,2,ip.description())

  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters(IMPLIEDPROCESS_ID,'Add implied process',ImpliedProcessDialog,IMPLIEDPROCESS_BUTTONCOMMIT_ID,self.dbProxy.addImpliedProcess,True)
      self.addObject(addParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add implied process',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.selectedLabel]
    try:
      updateParameters = DialogClassParameters(IMPLIEDPROCESS_ID,'Edit implied process',ImpliedProcessDialog,IMPLIEDPROCESS_BUTTONCOMMIT_ID,self.dbProxy.updateImpliedProcess,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit implied process',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onDelete(self,evt):
    try:
      self.deleteObject('No implied process','Delete implied process',self.dbProxy.deleteImpliedProcess)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete implied process',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return
