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
from ComponentView import ComponentView
from ComponentViewDialog import ComponentViewDialog
from DialogClassParameters import DialogClassParameters
from ComponentViewParameters import ComponentViewParameters
from DimensionBaseDialog import DimensionBaseDialog

class ComponentViewsDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,armid.COMPONENTVIEWS_ID,'Component Views',(930,300),'component_view.png')
    self.rmFrame = parent
    idList = [armid.COMPONENTVIEWS_LISTCOMPONENTVIEWS_ID,armid.COMPONENTVIEWS_BUTTONADD_ID,armid.COMPONENTVIEWS_BUTTONDELETE_ID]
    columnList = ['Model','Description']
    self.buildControls(idList,columnList,self.dbProxy.getComponentViews,'component_view')
    listCtrl = self.FindWindowById(armid.COMPONENTVIEWS_LISTCOMPONENTVIEWS_ID)
    listCtrl.SetColumnWidth(0,150)
    listCtrl.SetColumnWidth(1,600)

  def addObjectRow(self,componentListCtrl,listRow,component):
    componentListCtrl.InsertStringItem(listRow,component.name())
    componentListCtrl.SetStringItem(listRow,1,component.synopsis())

  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters(armid.COMPONENTVIEW_ID,'Add component view',ComponentViewDialog,armid.COMPONENTVIEW_BUTTONCOMMIT_ID,self.dbProxy.addComponentView,True)
      self.addObject(addParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add component view',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.selectedLabel]
    try:
      updateParameters = DialogClassParameters(armid.COMPONENTVIEW_ID,'Edit component view',ComponentViewDialog,armid.COMPONENTVIEW_BUTTONCOMMIT_ID,self.dbProxy.updateComponentView,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit component view',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No component view','Delete component view',self.dbProxy.deleteComponentView)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete component view',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy
