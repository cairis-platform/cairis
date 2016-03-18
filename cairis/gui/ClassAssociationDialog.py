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
import WidgetFactory
from Borg import Borg
from ClassAssociationParameters import ClassAssociationParameters

class ClassAssociationDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,armid.CLASSASSOCIATION_ID,'Asset association',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,600))
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theClassAssociationId = -1
    self.theEnvironmentName = ''
    self.theHeadAsset = ''
    self.theHeadNav = 0
    self.theHeadType = ''
    self.theHeadMultiplicity = ''
    self.theHeadRole = ''
    self.theTailRole = ''
    self.theTailMultiplicity = ''
    self.theTailType = ''
    self.theTailNav = 0
    self.theTailAsset = ''
    self.buildControls(parameters)
    self.commitVerb = 'Add'

  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    associationSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(associationSizer,0,wx.EXPAND)
    environments = self.dbProxy.getDimensionNames('environment')
    assets = []
    navs = ['0','1','-1']

    associationTypes = []
    associationTypes = ['Inheritance','Association','Aggregation','Composition','Dependency']
    multiplicityTypes = ['1','*','1..*']

    associationSizer.Add(WidgetFactory.buildComboSizerList(self,'Environment',(87,30),armid.CLASSASSOCIATION_COMBOENVIRONMENT_ID,environments),0,wx.EXPAND)
    associationSizer.Add(WidgetFactory.buildComboSizerList(self,'Head',(87,30),armid.CLASSASSOCIATION_COMBOHEADASSET_ID,assets),0,wx.EXPAND)
    associationSizer.Add(WidgetFactory.buildComboSizerList(self,'Navigation',(87,30),armid.CLASSASSOCIATION_COMBOHEADNAV_ID,navs),0,wx.EXPAND)
    associationSizer.Add(WidgetFactory.buildComboSizerList(self,'Adornment',(87,30),armid.CLASSASSOCIATION_COMBOHEADTYPE_ID,associationTypes),0,wx.EXPAND)
    associationSizer.Add(WidgetFactory.buildComboSizerList(self,'nry',(87,30),armid.CLASSASSOCIATION_COMBOHEADMULTIPLICITY_ID,multiplicityTypes),0,wx.EXPAND)
    associationSizer.Add(WidgetFactory.buildTextSizer(self,'Role',(87,30),armid.CLASSASSOCIATION_TEXTHEADROLE_ID),0,wx.EXPAND)
    associationSizer.Add(WidgetFactory.buildTextSizer(self,'Role',(87,30),armid.CLASSASSOCIATION_TEXTTAILROLE_ID),0,wx.EXPAND)
    associationSizer.Add(WidgetFactory.buildComboSizerList(self,'nry',(87,30),armid.CLASSASSOCIATION_COMBOTAILMULTIPLICITY_ID,multiplicityTypes),0,wx.EXPAND)
    associationSizer.Add(WidgetFactory.buildComboSizerList(self,'Adornment',(87,30),armid.CLASSASSOCIATION_COMBOTAILTYPE_ID,associationTypes),0,wx.EXPAND)
    associationSizer.Add(WidgetFactory.buildComboSizerList(self,'Navigation',(87,30),armid.CLASSASSOCIATION_COMBOTAILNAV_ID,navs),0,wx.EXPAND)
    associationSizer.Add(WidgetFactory.buildComboSizerList(self,'Tail',(87,30),armid.CLASSASSOCIATION_COMBOTAILASSET_ID,assets),0,wx.EXPAND)
    mainSizer.Add(wx.StaticText(self,-1),1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildAddCancelButtonSizer(self,armid.CLASSASSOCIATION_BUTTONCOMMIT_ID),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

    wx.EVT_BUTTON(self,armid.CLASSASSOCIATION_BUTTONCOMMIT_ID,self.onCommit)
    wx.EVT_COMBOBOX(self,armid.CLASSASSOCIATION_COMBOENVIRONMENT_ID,self.onEnvironmentChange)

  def load(self,association):
    self.theClassAssociationId = association.id()
    envCtrl = self.FindWindowById(armid.CLASSASSOCIATION_COMBOENVIRONMENT_ID)
    headCtrl = self.FindWindowById(armid.CLASSASSOCIATION_COMBOHEADASSET_ID)
    headNavCtrl = self.FindWindowById(armid.CLASSASSOCIATION_COMBOHEADNAV_ID)
    headTypeCtrl = self.FindWindowById(armid.CLASSASSOCIATION_COMBOHEADTYPE_ID)
    headMultiplicityCtrl = self.FindWindowById(armid.CLASSASSOCIATION_COMBOHEADMULTIPLICITY_ID)
    headRoleCtrl = self.FindWindowById(armid.CLASSASSOCIATION_TEXTHEADROLE_ID)
    tailRoleCtrl = self.FindWindowById(armid.CLASSASSOCIATION_TEXTTAILROLE_ID)
    tailMultiplicityCtrl = self.FindWindowById(armid.CLASSASSOCIATION_COMBOTAILMULTIPLICITY_ID)
    tailTypeCtrl = self.FindWindowById(armid.CLASSASSOCIATION_COMBOTAILTYPE_ID)
    tailNavCtrl = self.FindWindowById(armid.CLASSASSOCIATION_COMBOTAILNAV_ID)
    tailCtrl = self.FindWindowById(armid.CLASSASSOCIATION_COMBOTAILASSET_ID)
    buttonCtrl = self.FindWindowById(armid.CLASSASSOCIATION_BUTTONCOMMIT_ID)
    buttonCtrl.SetLabel('Edit')
  
    self.theEnvironmentName = association.environment()
    self.theHeadAsset = association.headAsset()
    self.theHeadNav = association.headNavigation()
    self.theHeadType = association.headType()
    self.theHeadMultiplicity = association.headMultiplicity()
    self.theHeadRole = association.headRole()
    self.theTailRole = association.tailRole()
    self.theTailMultiplicity = association.tailMultiplicity()
    self.theTailType = association.tailType()
    self.theTailNav = association.tailNavigation()
    self.theTailAsset = association.tailAsset()

    envCtrl.SetValue(self.theEnvironmentName)
    headCtrl.SetValue(self.theHeadAsset)
    headNavCtrl.SetValue(str(self.theHeadNav))
    headTypeCtrl.SetValue(self.theHeadType)
    headMultiplicityCtrl.SetValue(self.theHeadMultiplicity)
    headRoleCtrl.SetValue(self.theHeadRole)
    tailRoleCtrl.SetValue(self.theTailRole)
    tailMultiplicityCtrl.SetValue(self.theTailMultiplicity)
    tailTypeCtrl.SetValue(self.theTailType)
    tailNavCtrl.SetValue(str(self.theTailNav))
    tailCtrl.SetValue(self.theTailAsset)
    self.commitVerb = 'Edit'
    
  def onCommit(self,evt):
    commitLabel = self.commitVerb + ' association'
    envCtrl = self.FindWindowById(armid.CLASSASSOCIATION_COMBOENVIRONMENT_ID)
    headCtrl = self.FindWindowById(armid.CLASSASSOCIATION_COMBOHEADASSET_ID)
    headNavCtrl = self.FindWindowById(armid.CLASSASSOCIATION_COMBOHEADNAV_ID)
    headTypeCtrl = self.FindWindowById(armid.CLASSASSOCIATION_COMBOHEADTYPE_ID)
    headMultiplicityCtrl = self.FindWindowById(armid.CLASSASSOCIATION_COMBOHEADMULTIPLICITY_ID)
    headRoleCtrl = self.FindWindowById(armid.CLASSASSOCIATION_TEXTHEADROLE_ID)
    tailRoleCtrl = self.FindWindowById(armid.CLASSASSOCIATION_TEXTTAILROLE_ID)
    tailMultiplicityCtrl = self.FindWindowById(armid.CLASSASSOCIATION_COMBOTAILMULTIPLICITY_ID)
    tailTypeCtrl = self.FindWindowById(armid.CLASSASSOCIATION_COMBOTAILTYPE_ID)
    tailNavCtrl = self.FindWindowById(armid.CLASSASSOCIATION_COMBOTAILNAV_ID)
    tailCtrl = self.FindWindowById(armid.CLASSASSOCIATION_COMBOTAILASSET_ID)

    self.theEnvironmentName = envCtrl.GetValue()
    self.theHeadAsset = headCtrl.GetValue()
    self.theHeadNav = int(headNavCtrl.GetValue())
    self.theHeadType = headTypeCtrl.GetValue()
    self.theHeadMultiplicity = headMultiplicityCtrl.GetValue()
    self.theHeadRole = headRoleCtrl.GetValue()
    self.theTailRole = tailRoleCtrl.GetValue()
    self.theTailMultiplicity = tailMultiplicityCtrl.GetValue()
    self.theTailType = tailTypeCtrl.GetValue()
    self.theTailNav = int(tailNavCtrl.GetValue())
    self.theTailAsset = tailCtrl.GetValue()

    if len(self.theEnvironmentName) == 0:
      dlg = wx.MessageDialog(self,'No environment selected',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif len(self.theHeadAsset) == 0:
      dlg = wx.MessageDialog(self,'No head asset selected',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif len(self.theHeadType) == 0:
      dlg = wx.MessageDialog(self,'No head adornment selected',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theHeadMultiplicity) == 0):
      dlg = wx.MessageDialog(self,'No head multiplicity selected',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theTailMultiplicity) == 0):
      dlg = wx.MessageDialog(self,'No tail multiplicity selected',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif len(self.theTailType) == 0:
      dlg = wx.MessageDialog(self,'No tail adornment selected',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif len(self.theTailAsset) == 0:
      dlg = wx.MessageDialog(self,'No tail asset selected',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(armid.CLASSASSOCIATION_BUTTONCOMMIT_ID)

  def onEnvironmentChange(self,evt):
    envCtrl = self.FindWindowById(armid.CLASSASSOCIATION_COMBOENVIRONMENT_ID)
    headCtrl = self.FindWindowById(armid.CLASSASSOCIATION_COMBOHEADASSET_ID)
    headNavCtrl = self.FindWindowById(armid.CLASSASSOCIATION_COMBOHEADNAV_ID)
    headTypeCtrl = self.FindWindowById(armid.CLASSASSOCIATION_COMBOHEADTYPE_ID)
    headMultiplicityCtrl = self.FindWindowById(armid.CLASSASSOCIATION_COMBOHEADMULTIPLICITY_ID)
    headRoleCtrl = self.FindWindowById(armid.CLASSASSOCIATION_TEXTHEADROLE_ID)
    tailRoleCtrl = self.FindWindowById(armid.CLASSASSOCIATION_TEXTHEADROLE_ID)
    tailMultiplicityCtrl = self.FindWindowById(armid.CLASSASSOCIATION_COMBOTAILMULTIPLICITY_ID)
    tailTypeCtrl = self.FindWindowById(armid.CLASSASSOCIATION_COMBOHEADTYPE_ID)
    tailNavCtrl = self.FindWindowById(armid.CLASSASSOCIATION_COMBOTAILNAV_ID)
    tailCtrl = self.FindWindowById(armid.CLASSASSOCIATION_COMBOTAILASSET_ID)

    headCtrl.SetValue('')
    headNavCtrl.SetValue('')
    headTypeCtrl.SetValue('')
    headMultiplicityCtrl.SetValue('')
    headRoleCtrl.SetValue('')
    tailRoleCtrl.SetValue('')
    tailMultiplicityCtrl.SetValue('')
    tailTypeCtrl.SetValue('')
    tailNavCtrl.SetValue('')
    tailCtrl.SetValue('')

    envName = envCtrl.GetStringSelection()
    if (envName != ''):
      assets = self.dbProxy.environmentAssets(envName)
      headCtrl.SetItems(assets) 
      tailCtrl.SetItems(assets) 

  def parameters(self):
    parameters = ClassAssociationParameters(self.theEnvironmentName,self.theHeadAsset,'asset',self.theHeadNav,self.theHeadType,self.theHeadMultiplicity,self.theHeadRole,self.theTailRole,self.theTailMultiplicity,self.theTailType,self.theTailNav,'asset',self.theTailAsset)
    parameters.setId(self.theClassAssociationId)
    return parameters
