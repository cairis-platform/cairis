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
import cairis.core.Dependency
from DependencyDialog import DependencyDialog
from DialogClassParameters import DialogClassParameters
from cairis.core.ARM import *
from DimensionBaseDialog import DimensionBaseDialog

__author__ = 'Shamal Faily'

class DependenciesDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,DEPENDENCIES_ID,'Dependencies',(1080,300),'dependencyassociation.png')
    idList = [DEPENDENCIES_DEPENDENCYLIST_ID,DEPENDENCIES_BUTTONADD_ID,DEPENDENCIES_BUTTONDELETE_ID]
    columnList = ['Environment','Depender','Dependee','Noun','Dependency']
    self.buildControls(idList,columnList,self.dbProxy.getDependencies,'dependency')
    listCtrl = self.FindWindowById(DEPENDENCIES_DEPENDENCYLIST_ID)
    listCtrl.SetColumnWidth(0,150)
    listCtrl.SetColumnWidth(1,150)
    listCtrl.SetColumnWidth(2,150)
    listCtrl.SetColumnWidth(3,150)
    listCtrl.SetColumnWidth(4,150)


  def addObjectRow(self,listCtrl,listRow,dependency):
    listCtrl.InsertStringItem(listRow,dependency.environment())
    listCtrl.SetStringItem(listRow,1,dependency.depender())
    listCtrl.SetStringItem(listRow,2,dependency.dependee())
    listCtrl.SetStringItem(listRow,3,dependency.dependencyType())
    listCtrl.SetStringItem(listRow,4,dependency.dependency())

  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters(DEPENDENCY_ID,'Add depencency',DependencyDialog,DEPENDENCY_BUTTONCOMMIT_ID,self.dbProxy.addDependency,True)
      self.addObject(addParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add dependency',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def dependencyLabel(self):
    listCtrl = self.FindWindowById(DEPENDENCIES_DEPENDENCYLIST_ID)
    env = listCtrl.GetItemText(self.selectedIdx)
    depender = listCtrl.GetItem(self.selectedIdx,1)
    dependee = listCtrl.GetItem(self.selectedIdx,2)
    dependencyType = listCtrl.GetItem(self.selectedIdx,3)
    dependency = listCtrl.GetItem(self.selectedIdx,4)
    return env + '/' + depender.GetText() + '/' + dependee.GetText() + '/' + dependency.GetText()

  def deprecatedLabel(self):
    listCtrl = self.FindWindowById(DEPENDENCIES_DEPENDENCYLIST_ID)
    env = listCtrl.GetItemText(self.selectedIdx)
    depender = listCtrl.GetItem(self.selectedIdx,1)
    dependee = listCtrl.GetItem(self.selectedIdx,2)
    dependency = listCtrl.GetItem(self.selectedIdx,4)
    return env + '/' + depender.GetText() + '/' + dependee.GetText() + '/' + dependency.GetText()
  
  def onUpdate(self,evt):
    selectedObjt = self.objts[self.dependencyLabel()]
    goalId = selectedObjt.id()
    try:
      updateParameters = DialogClassParameters(DEPENDENCY_ID,'Edit depencency',DependencyDialog,DEPENDENCY_BUTTONCOMMIT_ID,self.dbProxy.updateDependency,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit dependency',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No dependency','Delete dependency',self.dbProxy.deleteDependency)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete dependency',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy
