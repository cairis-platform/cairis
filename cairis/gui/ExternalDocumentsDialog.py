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
import cairis.core.ExternalDocument
from ExternalDocumentDialog import ExternalDocumentDialog
from DialogClassParameters import DialogClassParameters
from cairis.core.ARM import *
from DimensionBaseDialog import DimensionBaseDialog

__author__ = 'Shamal Faily'

class ExternalDocumentsDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,EXTERNALDOCUMENTS_ID,'External Documents',(930,300),'persona.png')
    self.theMainWindow = parent
    idList = [EXTERNALDOCUMENTS_DOCLIST_ID,EXTERNALDOCUMENTS_BUTTONADD_ID,EXTERNALDOCUMENTS_BUTTONDELETE_ID]
    columnList = ['Name']
    self.buildControls(idList,columnList,self.dbProxy.getExternalDocuments,'external_document')
    listCtrl = self.FindWindowById(EXTERNALDOCUMENTS_DOCLIST_ID)
    listCtrl.SetColumnWidth(0,300)


  def addObjectRow(self,listCtrl,listRow,objt):
    listCtrl.InsertStringItem(listRow,objt.name())

  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters(EXTERNALDOCUMENT_ID,'Add External Document',ExternalDocumentDialog,EXTERNALDOCUMENT_BUTTONCOMMIT_ID,self.dbProxy.addExternalDocument,True)
      self.addObject(addParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add external document',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.selectedLabel]
    objtId = selectedObjt.id()
    try:
      updateParameters = DialogClassParameters(EXTERNALDOCUMENT_ID,'Edit External Document',ExternalDocumentDialog,EXTERNALDOCUMENT_BUTTONCOMMIT_ID,self.dbProxy.updateExternalDocument,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit external document',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No external document','Delete external document',self.dbProxy.deleteExternalDocument)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete external document',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy
