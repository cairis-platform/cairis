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
import ARM
from Component import Component
from ComponentDialog import ComponentDialog
from DialogClassParameters import DialogClassParameters
from ComponentParameters import ComponentParameters
from DimensionBaseDialog import DimensionBaseDialog

class ComponentsDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,armid.COMPONENTS_ID,'Components',(930,300),'component.png')
    self.rmFrame = parent
    idList = [armid.COMPONENTS_LISTCOMPONENTS_ID,armid.COMPONENTS_BUTTONADD_ID,armid.COMPONENTS_BUTTONDELETE_ID]
    columnList = ['Name','Description']
    self.buildControls(idList,columnList,self.dbProxy.getComponents,'component')
    listCtrl = self.FindWindowById(armid.COMPONENTS_LISTCOMPONENTS_ID)
    listCtrl.SetColumnWidth(0,150)
    listCtrl.SetColumnWidth(1,600)

  def addObjectRow(self,componentListCtrl,listRow,component):
    componentListCtrl.InsertStringItem(listRow,component.name())
    componentListCtrl.SetStringItem(listRow,1,component.description())

  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters(armid.COMPONENT_ID,'Add component',ComponentDialog,armid.COMPONENT_BUTTONCOMMIT_ID,self.dbProxy.addComponent,True)
      self.addObject(addParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add component',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.selectedLabel]
    try:
      updateParameters = DialogClassParameters(armid.COMPONENT_ID,'Edit component',ComponentDialog,armid.COMPONENT_BUTTONCOMMIT_ID,self.dbProxy.updateComponent,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit component',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No component','Delete component',self.dbProxy.deleteComponent)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete component',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy
