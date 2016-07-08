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
import cairis.core.Code
from CodeDialog import CodeDialog
from DialogClassParameters import DialogClassParameters
from cairis.core.ARM import *
from DimensionBaseDialog import DimensionBaseDialog

class CodesDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,CODES_ID,'Codes',(930,300),'persona.png')
    self.theMainWindow = parent
    idList = [CODES_DOCLIST_ID,CODES_BUTTONADD_ID,CODES_BUTTONDELETE_ID]
    columnList = ['Name','Type','Description']
    self.buildControls(idList,columnList,self.dbProxy.getCodes,'code')
    listCtrl = self.FindWindowById(CODES_DOCLIST_ID)
    listCtrl.SetColumnWidth(0,100)
    listCtrl.SetColumnWidth(1,100)
    listCtrl.SetColumnWidth(2,300)


  def addObjectRow(self,listCtrl,listRow,objt):
    listCtrl.InsertStringItem(listRow,objt.name())
    listCtrl.SetStringItem(listRow,1,objt.type())
    listCtrl.SetStringItem(listRow,2,objt.description())

  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters(CODE_ID,'Add Code',CodeDialog,CODE_BUTTONCOMMIT_ID,self.dbProxy.addCode,True)
      self.addObject(addParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add code',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.selectedLabel]
    objtId = selectedObjt.id()
    try:
      updateParameters = DialogClassParameters(CODE_ID,'Edit Code',CodeDialog,CODE_BUTTONCOMMIT_ID,self.dbProxy.updateCode,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit code',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No code','Delete code',self.dbProxy.deleteCode)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete code',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy
