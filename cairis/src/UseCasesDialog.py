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


#$URL$ $Id: UseCasesDialog.py 469 2011-05-14 22:36:20Z shaf $
import wx
import armid
from UseCaseDialog import UseCaseDialog
import ARM
from DimensionBaseDialog import DimensionBaseDialog
from DialogClassParameters import DialogClassParameters

class UseCasesDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,armid.USECASES_ID,'Use Cases',(400,350),'usecase.png')
    idList = [armid.USECASES_USECASELIST_ID,armid.USECASES_BUTTONADD_ID,armid.USECASES_BUTTONDELETE_ID]
    columnList = ['Name']
    self.buildControls(idList,columnList,self.dbProxy.getUseCases,'usecase')
    self.listCtrl = self.FindWindowById(armid.USECASES_USECASELIST_ID)
    self.listCtrl.SetColumnWidth(0,300)


  def addObjectRow(self,listCtrl,listRow,objt):
    listCtrl.InsertStringItem(listRow,objt.name())

  def onAdd(self,evt):
    try:
      addLabel = 'Add Use Case' 
      addParameters = DialogClassParameters(armid.USECASE_ID,addLabel,UseCaseDialog,armid.USECASE_BUTTONCOMMIT_ID,self.dbProxy.addUseCase,True)
      self.addObject(addParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add Use Case',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.listCtrl.theSelectedLabel]
    updateLabel = 'Edit Use Case'
    try:
      updateParameters = DialogClassParameters(armid.USECASE_ID,updateLabel,UseCaseDialog,armid.USECASE_BUTTONCOMMIT_ID,self.dbProxy.updateUseCase,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),updateLabel,wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onDelete(self,evt):
    try:
      self.deleteObject('No use case','Delete use case',self.dbProxy.deleteUseCase)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete Use Case',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return
