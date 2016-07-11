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
from cairis.core.ARM import *
from cairis.core.ComponentView import ComponentView
from ComponentViewDialog import ComponentViewDialog
from DialogClassParameters import DialogClassParameters
from cairis.core.ComponentViewParameters import ComponentViewParameters
from DimensionBaseDialog import DimensionBaseDialog

class ArchitecturalPatternsDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,COMPONENTVIEWS_ID,'Architectural Patternss',(930,300),'component_view.png')
    self.theMainWindow = parent
    self.rmFrame = parent
    idList = [COMPONENTVIEWS_LISTCOMPONENTVIEWS_ID,COMPONENTVIEWS_BUTTONADD_ID,COMPONENTVIEWS_BUTTONDELETE_ID]
    columnList = ['Model','Interfaces DER Ratio','Channels DER Ratio','Untrusted Surface DER Ratio']
    self.buildControls(idList,columnList,self.dbProxy.getComponentViews,'component_view')
    listCtrl = self.FindWindowById(COMPONENTVIEWS_LISTCOMPONENTVIEWS_ID)
    listCtrl.SetColumnWidth(0,150)
    listCtrl.SetColumnWidth(1,200)
    listCtrl.SetColumnWidth(2,200)
    listCtrl.SetColumnWidth(3,200)

  def addObjectRow(self,componentListCtrl,listRow,objt):
    componentListCtrl.InsertStringItem(listRow,objt.name())
    asm = objt.attackSurfaceMetric()
    componentListCtrl.SetStringItem(listRow,1,str(asm[0]))
    componentListCtrl.SetStringItem(listRow,2,str(asm[1]))
    componentListCtrl.SetStringItem(listRow,3,str(asm[2]))

  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters(COMPONENTVIEW_ID,'Add architectural pattern',ComponentViewDialog,COMPONENTVIEW_BUTTONCOMMIT_ID,self.dbProxy.addComponentView,True)
      self.addObject(addParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add architectural pattern',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.selectedLabel]
    try:
      updateParameters = DialogClassParameters(COMPONENTVIEW_ID,'Edit architectural pattern',ComponentViewDialog,COMPONENTVIEW_BUTTONCOMMIT_ID,self.dbProxy.updateComponentView,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit architectural pattern',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No component view','Delete architectural pattern',self.dbProxy.deleteComponentView)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete architectural pattern',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy
