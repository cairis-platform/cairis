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
import armid
import ConceptReference
from ConceptReferenceDialog import ConceptReferenceDialog
from DialogClassParameters import DialogClassParameters
import ARM
from DimensionBaseDialog import DimensionBaseDialog

class ConceptReferencesDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,armid.CONCEPTREFERENCES_ID,'Concept References',(930,300),'persona.png')
    self.theMainWindow = parent
    idList = [armid.CONCEPTREFERENCES_REFLIST_ID,armid.CONCEPTREFERENCES_BUTTONADD_ID,armid.CONCEPTREFERENCES_BUTTONDELETE_ID]
    columnList = ['Name']
    self.buildControls(idList,columnList,self.dbProxy.getConceptReferences,'concept_reference')
    listCtrl = self.FindWindowById(armid.CONCEPTREFERENCES_REFLIST_ID)
    listCtrl.SetColumnWidth(0,800)


  def addObjectRow(self,listCtrl,listRow,objt):
    listCtrl.InsertStringItem(listRow,objt.name())

  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters(armid.CONCEPTREFERENCE_ID,'Add Concept Reference',ConceptReferenceDialog,armid.CONCEPTREFERENCE_BUTTONCOMMIT_ID,self.dbProxy.addConceptReference,True)
      self.addObject(addParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add concept reference',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.selectedLabel]
    objtId = selectedObjt.id()
    try:
      updateParameters = DialogClassParameters(armid.CONCEPTREFERENCE_ID,'Edit Concept Reference',ConceptReferenceDialog,armid.CONCEPTREFERENCE_BUTTONCOMMIT_ID,self.dbProxy.updateConceptReference,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit concept reference',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No concept reference','Delete concept reference',self.dbProxy.deleteConceptReference)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete concept reference',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy
