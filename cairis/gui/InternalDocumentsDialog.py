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
import cairis.core.InternalDocument
from InternalDocumentDialog import InternalDocumentDialog
from DialogClassParameters import DialogClassParameters
from cairis.core.ARM import *
from DimensionBaseDialog import DimensionBaseDialog

class InternalDocumentsDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,INTERNALDOCUMENTS_ID,'Internal Documents',(930,300),'persona.png')
    self.theMainWindow = parent
    idList = [INTERNALDOCUMENTS_DOCLIST_ID,INTERNALDOCUMENTS_BUTTONADD_ID,INTERNALDOCUMENTS_BUTTONDELETE_ID]
    columnList = ['Name']
    self.buildControls(idList,columnList,self.dbProxy.getInternalDocuments,'internal_document')
    listCtrl = self.FindWindowById(INTERNALDOCUMENTS_DOCLIST_ID)
    listCtrl.SetColumnWidth(0,300)


  def addObjectRow(self,listCtrl,listRow,objt):
    listCtrl.InsertStringItem(listRow,objt.name())

  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters(INTERNALDOCUMENT_ID,'Add Internal Document',InternalDocumentDialog,INTERNALDOCUMENT_BUTTONCOMMIT_ID,self.dbProxy.addInternalDocument,True)
      self.addObject(addParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add internal document',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.selectedLabel]
    objtId = selectedObjt.id()
    try:
      updateParameters = DialogClassParameters(INTERNALDOCUMENT_ID,'Edit Internal Document',InternalDocumentDialog,INTERNALDOCUMENT_BUTTONCOMMIT_ID,self.dbProxy.updateInternalDocument,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit internal document',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No internal document','Delete internal document',self.dbProxy.deleteInternalDocument)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete external document',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy
