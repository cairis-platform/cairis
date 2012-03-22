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
import ClassAssociation
from ClassAssociationDialog import ClassAssociationDialog
from DialogClassParameters import DialogClassParameters
import ARM
from DimensionBaseDialog import DimensionBaseDialog

class ClassAssociationsDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,armid.CLASSASSOCIATIONS_ID,'ClassAssociations',(930,300),'classassociations.png')
    idList = [armid.CLASSASSOCIATIONS_CLASSASSOCIATIONLIST_ID,armid.CLASSASSOCIATIONS_BUTTONADD_ID,armid.CLASSASSOCIATIONS_BUTTONDELETE_ID]
    columnList = ['Environment/Head/Tail','Type','nry','Role','Role','nry','Type']
    self.buildControls(idList,columnList,self.dbProxy.getClassAssociations,'classassociation')
    listCtrl = self.FindWindowById(armid.CLASSASSOCIATIONS_CLASSASSOCIATIONLIST_ID)
    listCtrl.SetColumnWidth(0,200)
    listCtrl.SetColumnWidth(1,100)
    listCtrl.SetColumnWidth(2,50)
    listCtrl.SetColumnWidth(3,100)
    listCtrl.SetColumnWidth(4,100)
    listCtrl.SetColumnWidth(5,50)
    listCtrl.SetColumnWidth(6,100)


  def addObjectRow(self,listCtrl,listRow,association):
    label = association.environment() + '/' + association.headAsset() + '/' + association.tailAsset()
    listCtrl.InsertStringItem(listRow,label)
    listCtrl.SetStringItem(listRow,1,association.headType())
    listCtrl.SetStringItem(listRow,2,association.headMultiplicity())
    listCtrl.SetStringItem(listRow,3,association.headRole())
    listCtrl.SetStringItem(listRow,4,association.tailRole())
    listCtrl.SetStringItem(listRow,5,association.tailMultiplicity())
    listCtrl.SetStringItem(listRow,6,association.tailType())

  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters(armid.CLASSASSOCIATION_ID,'Add class association',ClassAssociationDialog,armid.CLASSASSOCIATION_BUTTONCOMMIT_ID,self.dbProxy.addClassAssociation,True)
      self.addObject(addParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add class association',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.selectedLabel]
    assetId = selectedObjt.id()
    try:
      updateParameters = DialogClassParameters(armid.CLASSASSOCIATION_ID,'Edit class association',ClassAssociationDialog,armid.CLASSASSOCIATION_BUTTONCOMMIT_ID,self.dbProxy.updateClassAssociation,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit class association',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No class association','Delete class association',self.dbProxy.deleteClassAssociation)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete class association',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy
