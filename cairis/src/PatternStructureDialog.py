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

class PatternStructureDialog(wx.Dialog):
  def __init__(self,parent,headName = '',headAdornment = '',headNry = '',headRole='',tailRole='',tailNry='',tailAdornment='',tailName = ''):
    wx.Dialog.__init__(self,parent,armid.PATTERNSTRUCTURE_ID,'Add Pattern Structure',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,475))
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theHeadName = headName
    self.theHeadAdornment = headAdornment
    self.theHeadNry = headNry
    self.theHeadRole = headRole
    self.theTailRole = tailRole
    self.theTailNry = tailNry
    self.theTailAdornment = tailAdornment
    self.theTailName = tailName
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    assets = self.dbProxy.getDimensionNames('template_asset')
    associationTypes = ['Inheritance','Association','Aggregation','Composition','Dependency']
    multiplicityTypes = ['1','*','1..*']

    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Head',(87,30),armid.PATTERNSTRUCTURE_COMBOHEADASSET_ID,assets),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Adornment',(87,30),armid.PATTERNSTRUCTURE_COMBOHEADTYPE_ID,associationTypes),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'nry',(87,30),armid.PATTERNSTRUCTURE_COMBOHEADMULTIPLICITY_ID,multiplicityTypes),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Role',(87,30),armid.PATTERNSTRUCTURE_TEXTHEADROLE_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Role',(87,30),armid.PATTERNSTRUCTURE_TEXTTAILROLE_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'nry',(87,30),armid.PATTERNSTRUCTURE_COMBOTAILMULTIPLICITY_ID,multiplicityTypes),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Adornment',(87,30),armid.PATTERNSTRUCTURE_COMBOTAILTYPE_ID,associationTypes),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Tail',(87,30),armid.PATTERNSTRUCTURE_COMBOTAILASSET_ID,assets),0,wx.EXPAND)

    mainSizer.Add(WidgetFactory.buildAddCancelButtonSizer(self,armid.PATTERNSTRUCTURE_BUTTONCOMMIT_ID),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

    wx.EVT_BUTTON(self,armid.PATTERNSTRUCTURE_BUTTONCOMMIT_ID,self.onCommit)
    self.commitLabel = 'Add'
    if (len(self.theTailName) > 0):
      self.commitLabel = 'Edit'
      self.SetLabel('Edit Asset Association')
      headCtrl = self.FindWindowById(armid.PATTERNSTRUCTURE_COMBOHEADASSET_ID)
      headCtrl.SetStringSelection(self.theHeadName)
      headTypeCtrl = self.FindWindowById(armid.PATTERNSTRUCTURE_COMBOHEADTYPE_ID)
      headTypeCtrl.SetStringSelection(self.theTailAdornment)
      headNryCtrl = self.FindWindowById(armid.PATTERNSTRUCTURE_COMBOHEADMULTIPLICITY_ID)
      headNryCtrl.SetStringSelection(self.theTailNry)
      headRoleCtrl = self.FindWindowById(armid.PATTERNSTRUCTURE_TEXTHEADROLE_ID)
      headRoleCtrl.SetValue(self.theTailRole)
      tailRoleCtrl = self.FindWindowById(armid.PATTERNSTRUCTURE_TEXTTAILROLE_ID)
      tailRoleCtrl.SetValue(self.theHeadRole)
      tailNryCtrl = self.FindWindowById(armid.PATTERNSTRUCTURE_COMBOTAILMULTIPLICITY_ID)
      tailNryCtrl.SetStringSelection(self.theHeadNry)
      tailTypeCtrl = self.FindWindowById(armid.PATTERNSTRUCTURE_COMBOTAILTYPE_ID)
      tailTypeCtrl.SetStringSelection(self.theHeadAdornment)
      tailCtrl = self.FindWindowById(armid.PATTERNSTRUCTURE_COMBOTAILASSET_ID)
      tailCtrl.SetStringSelection(self.theTailName)
      buttonCtrl = self.FindWindowById(armid.PATTERNSTRUCTURE_BUTTONCOMMIT_ID)
      buttonCtrl.SetLabel('Edit')
      

  def onCommit(self,evt):
    headCtrl = self.FindWindowById(armid.PATTERNSTRUCTURE_COMBOHEADASSET_ID)
    headTypeCtrl = self.FindWindowById(armid.PATTERNSTRUCTURE_COMBOHEADTYPE_ID)
    headNryCtrl = self.FindWindowById(armid.PATTERNSTRUCTURE_COMBOHEADMULTIPLICITY_ID)
    headRoleCtrl = self.FindWindowById(armid.PATTERNSTRUCTURE_TEXTHEADROLE_ID)
    tailRoleCtrl = self.FindWindowById(armid.PATTERNSTRUCTURE_TEXTTAILROLE_ID)
    tailNryCtrl = self.FindWindowById(armid.PATTERNSTRUCTURE_COMBOTAILMULTIPLICITY_ID)
    tailTypeCtrl = self.FindWindowById(armid.PATTERNSTRUCTURE_COMBOTAILTYPE_ID)
    tailCtrl = self.FindWindowById(armid.PATTERNSTRUCTURE_COMBOTAILASSET_ID)

    self.theHeadName = headCtrl.GetStringSelection()
    self.theTailAdornment = headTypeCtrl.GetStringSelection()
    self.theHeadNry = tailNryCtrl.GetStringSelection()
    self.theHeadRole = tailRoleCtrl.GetValue()
    self.theTailRole = headRoleCtrl.GetValue()
    self.theTailNry = headNryCtrl.GetStringSelection()
    self.theHeadAdornment = tailTypeCtrl.GetStringSelection()
    self.theTailName = tailCtrl.GetStringSelection()

    if (len(self.theHeadName) == 0):
      dlg = wx.MessageDialog(self,'No head asset selected',self.commitLabel + ' Pattern Structure',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theHeadAdornment) == 0):
      dlg = wx.MessageDialog(self,'No head type selected',self.commitLabel + ' Pattern Structure',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theHeadNry) == 0):
      dlg = wx.MessageDialog(self,'No head multiplicity selected',self.commitLabel + ' Pattern Structure',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theTailNry) == 0):
      dlg = wx.MessageDialog(self,'No tail multiplicity selected',self.commitLabel + ' Pattern Structure',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theTailAdornment) == 0):
      dlg = wx.MessageDialog(self,'No tail type selected',self.commitLabel + ' Pattern Structure',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theTailName) == 0):
      dlg = wx.MessageDialog(self,'No tail asset selected',self.commitLabel + ' Pattern Structure',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(armid.PATTERNSTRUCTURE_BUTTONCOMMIT_ID)

  def headAsset(self): return self.theHeadName
  def headAdornment(self): return self.theHeadAdornment
  def headMultiplicity(self): return self.theHeadNry
  def headRole(self): return self.theHeadRole
  def tailRole(self): return self.theTailRole
  def tailMultiplicity(self): return self.theTailNry
  def tailAdornment(self): return self.theTailAdornment
  def tailAsset(self): return self.theTailName
