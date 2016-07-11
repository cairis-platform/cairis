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
import WidgetFactory
from cairis.core.Borg import Borg
from cairis.core.DependencyParameters import DependencyParameters

class DependencyDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,DEPENDENCY_ID,'Dependency',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(900,400))
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theId = (-1,-1)
    self.theEnvironmentName = ''
    self.theDepender = ''
    self.theDependee = ''
    self.theDependencyType = ''
    self.theDependency = ''
    self.theRationale = ''
    self.buildControls(parameters)
    self.commitVerb = 'Add'

  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    associationSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(associationSizer,0,wx.EXPAND)
    environments = self.dbProxy.getDimensionNames('environment')
    roles = self.dbProxy.getDimensionNames('role')
    self.dependencyTypes = ['goal','task','asset']
    self.dependencies = []
    associationSizer.Add(WidgetFactory.buildComboSizerList(self,'Environment',(150,30),DEPENDENCY_COMBOENVIRONMENT_ID,environments),0,wx.EXPAND)
    associationSizer.Add(WidgetFactory.buildComboSizerList(self,'Depender',(200,30),DEPENDENCY_COMBODEPENDER_ID,roles),0,wx.EXPAND)
    associationSizer.Add(WidgetFactory.buildComboSizerList(self,'Dependee',(200,30),DEPENDENCY_COMBODEPENDEE_ID,roles),0,wx.EXPAND)
    associationSizer.Add(WidgetFactory.buildComboSizerList(self,'Type',(87,30),DEPENDENCY_COMBODTYPE_ID,self.dependencyTypes),0,wx.EXPAND)
    associationSizer.Add(WidgetFactory.buildComboSizerList(self,'Dependency',(200,30),DEPENDENCY_COMBODEPENDENCY_ID,self.dependencies),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildMLTextSizer(self,'Rationale',(87,60),DEPENDENCY_TEXTRATIONALE_ID),1,wx.EXPAND,1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildAddCancelButtonSizer(self,DEPENDENCY_BUTTONCOMMIT_ID),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

    wx.EVT_BUTTON(self,DEPENDENCY_BUTTONCOMMIT_ID,self.onCommit)
    wx.EVT_COMBOBOX(self,DEPENDENCY_COMBOENVIRONMENT_ID,self.onEnvironmentChange)
    wx.EVT_COMBOBOX(self,DEPENDENCY_COMBODTYPE_ID,self.onDependencyTypeChange)

  def load(self,dependency):
    self.theId = dependency.id()
    envCtrl = self.FindWindowById(DEPENDENCY_COMBOENVIRONMENT_ID)
    dependerCtrl = self.FindWindowById(DEPENDENCY_COMBODEPENDER_ID)
    dependeeCtrl = self.FindWindowById(DEPENDENCY_COMBODEPENDEE_ID)
    dTypeCtrl = self.FindWindowById(DEPENDENCY_COMBODTYPE_ID)
    dependencyCtrl = self.FindWindowById(DEPENDENCY_COMBODEPENDENCY_ID)
    rationaleCtrl = self.FindWindowById(DEPENDENCY_TEXTRATIONALE_ID)
    buttonCtrl = self.FindWindowById(DEPENDENCY_BUTTONCOMMIT_ID)
    buttonCtrl.SetLabel('Edit')
  
    self.theEnvironmentName = dependency.environment()
    self.theDepender = dependency.depender()
    self.theDependee = dependency.dependee()
    self.theDependencyType = dependency.dependencyType()
    self.theDependency = dependency.dependency()
    self.theRationale = dependency.rationale()

    envCtrl.SetValue(self.theEnvironmentName)
    dependerCtrl.SetValue(self.theDepender)
    dependeeCtrl.SetValue(self.theDependee)
    dTypeCtrl.SetValue(self.theDependencyType)
    dependencyCtrl.SetValue(self.theDependency)
    rationaleCtrl.SetValue(self.theRationale)

    self.commitVerb = 'Edit'
    
  def onCommit(self,evt):
    commitLabel = self.commitVerb + ' association'
    envCtrl = self.FindWindowById(DEPENDENCY_COMBOENVIRONMENT_ID)
    dependerCtrl = self.FindWindowById(DEPENDENCY_COMBODEPENDER_ID)
    dependeeCtrl = self.FindWindowById(DEPENDENCY_COMBODEPENDEE_ID)
    dTypeCtrl = self.FindWindowById(DEPENDENCY_COMBODTYPE_ID)
    dependencyCtrl = self.FindWindowById(DEPENDENCY_COMBODEPENDENCY_ID)
    rationaleCtrl = self.FindWindowById(DEPENDENCY_TEXTRATIONALE_ID)

    self.theEnvironmentName = envCtrl.GetValue()
    self.theDepender = dependerCtrl.GetValue()
    self.theDependee = dependeeCtrl.GetValue()
    self.theDependencyType = dTypeCtrl.GetValue()
    self.theDependency = dependencyCtrl.GetValue()
    self.theRationale = rationaleCtrl.GetValue()

    if len(self.theEnvironmentName) == 0:
      dlg = wx.MessageDialog(self,'No environment selected',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif len(self.theDepender) == 0:
      dlg = wx.MessageDialog(self,'No depender selected',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif len(self.theDependee) == 0:
      dlg = wx.MessageDialog(self,'No dependee selected',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif len(self.theDependencyType) == 0:
      dlg = wx.MessageDialog(self,'No dependency type selected',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif len(self.theDependency) == 0:
      dlg = wx.MessageDialog(self,'No dependency selected',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif len(self.theRationale) == 0:
      dlg = wx.MessageDialog(self,'No rationale entered',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(DEPENDENCY_BUTTONCOMMIT_ID)

  def onEnvironmentChange(self,evt):
    envCtrl = self.FindWindowById(DEPENDENCY_COMBOENVIRONMENT_ID)
    dTypeCtrl = self.FindWindowById(DEPENDENCY_COMBODTYPE_ID)
    dependencyCtrl = self.FindWindowById(DEPENDENCY_COMBODEPENDENCY_ID)
    dependencyCtrl.SetItems([])
    dependencyCtrl.SetValue('')
    self.theEnvironmentName = envCtrl.GetStringSelection()
    depType = dTypeCtrl.GetValue()
    if (depType != ''):
      dependencyCtrl.SetItems([])
      dependencyCtrl.SetValue('')
      dependencyCtrl.SetItems(self.dbProxy.getDimensionNames(depType,self.theEnvironmentName))

  def onDependencyTypeChange(self,evt):
    dependencyCtrl = self.FindWindowById(DEPENDENCY_COMBODEPENDENCY_ID)
    dTypeCtrl = self.FindWindowById(DEPENDENCY_COMBODTYPE_ID)

    depType = dTypeCtrl.GetValue()
    if (depType != ''):
      dependencyCtrl.SetItems([])
      dependencyCtrl.SetValue('')
      dependencyCtrl.SetItems(self.dbProxy.getDimensionNames(depType,self.theEnvironmentName))

  def parameters(self):
    parameters = DependencyParameters(self.theEnvironmentName,self.theDepender,self.theDependee,self.theDependencyType,self.theDependency,self.theRationale)
    parameters.setId(self.theId)
    return parameters
