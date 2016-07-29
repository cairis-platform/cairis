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

__author__ = 'Shamal Faily'

class PatternStructureDialog(wx.Dialog):
  def __init__(self,parent,headName = '',headAdornment = '',headNav = '',headNry = '',headRole='',tailRole='',tailNry='',tailNav = '',tailAdornment='',tailName = ''):
    wx.Dialog.__init__(self,parent,PATTERNSTRUCTURE_ID,'Add Structure',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,575))
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theHeadName = headName
    self.theHeadAdornment = headAdornment
    self.theHeadNav = headNav
    self.theHeadNry = headNry
    self.theHeadRole = headRole
    self.theTailRole = tailRole
    self.theTailNry = tailNry
    self.theTailNav = tailNav
    self.theTailAdornment = tailAdornment
    self.theTailName = tailName
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    assets = self.dbProxy.getDimensionNames('template_asset')
    associationTypes = ['Inheritance','Association','Aggregation','Composition','Dependency']
    multiplicityTypes = ['1','*','1..*']
    navTypes = ['1','0']

    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Head',(87,30),PATTERNSTRUCTURE_COMBOHEADASSET_ID,assets),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Adornment',(87,30),PATTERNSTRUCTURE_COMBOHEADTYPE_ID,associationTypes),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Nav',(87,30),PATTERNSTRUCTURE_COMBOHEADNAV_ID,navTypes),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'nry',(87,30),PATTERNSTRUCTURE_COMBOHEADMULTIPLICITY_ID,multiplicityTypes),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Role',(87,30),PATTERNSTRUCTURE_TEXTHEADROLE_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Role',(87,30),PATTERNSTRUCTURE_TEXTTAILROLE_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'nry',(87,30),PATTERNSTRUCTURE_COMBOTAILMULTIPLICITY_ID,multiplicityTypes),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Nav',(87,30),PATTERNSTRUCTURE_COMBOTAILNAV_ID,navTypes),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Adornment',(87,30),PATTERNSTRUCTURE_COMBOTAILTYPE_ID,associationTypes),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Tail',(87,30),PATTERNSTRUCTURE_COMBOTAILASSET_ID,assets),0,wx.EXPAND)

    mainSizer.Add(WidgetFactory.buildAddCancelButtonSizer(self,PATTERNSTRUCTURE_BUTTONCOMMIT_ID),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

    wx.EVT_BUTTON(self,PATTERNSTRUCTURE_BUTTONCOMMIT_ID,self.onCommit)
    self.commitLabel = 'Add'
    if (len(self.theTailName) > 0):
      self.commitLabel = 'Edit'
      self.SetLabel('Edit Asset Association')
      headCtrl = self.FindWindowById(PATTERNSTRUCTURE_COMBOHEADASSET_ID)
      headCtrl.SetStringSelection(self.theHeadName)
      headTypeCtrl = self.FindWindowById(PATTERNSTRUCTURE_COMBOHEADTYPE_ID)
      headTypeCtrl.SetStringSelection(self.theTailAdornment)
      headNavCtrl = self.FindWindowById(PATTERNSTRUCTURE_COMBOHEADNAV_ID)
      headNavCtrl.SetStringSelection(self.theTailNav)
      headNryCtrl = self.FindWindowById(PATTERNSTRUCTURE_COMBOHEADMULTIPLICITY_ID)
      headNryCtrl.SetStringSelection(self.theTailNry)
      headRoleCtrl = self.FindWindowById(PATTERNSTRUCTURE_TEXTHEADROLE_ID)
      headRoleCtrl.SetValue(self.theTailRole)
      tailRoleCtrl = self.FindWindowById(PATTERNSTRUCTURE_TEXTTAILROLE_ID)
      tailRoleCtrl.SetValue(self.theHeadRole)
      tailNryCtrl = self.FindWindowById(PATTERNSTRUCTURE_COMBOTAILMULTIPLICITY_ID)
      tailNryCtrl.SetStringSelection(self.theHeadNry)
      tailNavCtrl = self.FindWindowById(PATTERNSTRUCTURE_COMBOTAILNAV_ID)
      tailNavCtrl.SetStringSelection(self.theHeadNav)
      tailTypeCtrl = self.FindWindowById(PATTERNSTRUCTURE_COMBOTAILTYPE_ID)
      tailTypeCtrl.SetStringSelection(self.theHeadAdornment)
      tailCtrl = self.FindWindowById(PATTERNSTRUCTURE_COMBOTAILASSET_ID)
      tailCtrl.SetStringSelection(self.theTailName)
      buttonCtrl = self.FindWindowById(PATTERNSTRUCTURE_BUTTONCOMMIT_ID)
      buttonCtrl.SetLabel('Edit')
      

  def onCommit(self,evt):
    headCtrl = self.FindWindowById(PATTERNSTRUCTURE_COMBOHEADASSET_ID)
    headTypeCtrl = self.FindWindowById(PATTERNSTRUCTURE_COMBOHEADTYPE_ID)
    headNavCtrl = self.FindWindowById(PATTERNSTRUCTURE_COMBOHEADNAV_ID)
    headNryCtrl = self.FindWindowById(PATTERNSTRUCTURE_COMBOHEADMULTIPLICITY_ID)
    headRoleCtrl = self.FindWindowById(PATTERNSTRUCTURE_TEXTHEADROLE_ID)
    tailRoleCtrl = self.FindWindowById(PATTERNSTRUCTURE_TEXTTAILROLE_ID)
    tailNryCtrl = self.FindWindowById(PATTERNSTRUCTURE_COMBOTAILMULTIPLICITY_ID)
    tailNavCtrl = self.FindWindowById(PATTERNSTRUCTURE_COMBOTAILNAV_ID)
    tailTypeCtrl = self.FindWindowById(PATTERNSTRUCTURE_COMBOTAILTYPE_ID)
    tailCtrl = self.FindWindowById(PATTERNSTRUCTURE_COMBOTAILASSET_ID)

    self.theHeadName = headCtrl.GetStringSelection()
    self.theTailAdornment = headTypeCtrl.GetStringSelection()
    self.theTailNav = headNavCtrl.GetStringSelection()
    self.theHeadNry = tailNryCtrl.GetStringSelection()
    self.theHeadRole = tailRoleCtrl.GetValue()
    self.theTailRole = headRoleCtrl.GetValue()
    self.theTailNry = headNryCtrl.GetStringSelection()
    self.theHeadNav = tailNavCtrl.GetStringSelection()
    self.theHeadAdornment = tailTypeCtrl.GetStringSelection()
    self.theTailName = tailCtrl.GetStringSelection()

    if (len(self.theHeadName) == 0):
      dlg = wx.MessageDialog(self,'No head asset selected',self.commitLabel + ' Structure',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theHeadAdornment) == 0):
      dlg = wx.MessageDialog(self,'No head type selected',self.commitLabel + ' Structure',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theHeadNav) == 0):
      dlg = wx.MessageDialog(self,'No head nav selected',self.commitLabel + ' Structure',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theHeadNry) == 0):
      dlg = wx.MessageDialog(self,'No head multiplicity selected',self.commitLabel + ' Structure',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theTailNry) == 0):
      dlg = wx.MessageDialog(self,'No tail multiplicity selected',self.commitLabel + ' Structure',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theTailNav) == 0):
      dlg = wx.MessageDialog(self,'No tail nav selected',self.commitLabel + ' Structure',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theTailAdornment) == 0):
      dlg = wx.MessageDialog(self,'No tail type selected',self.commitLabel + ' Structure',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theTailName) == 0):
      dlg = wx.MessageDialog(self,'No tail asset selected',self.commitLabel + ' Structure',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(PATTERNSTRUCTURE_BUTTONCOMMIT_ID)

  def headAsset(self): return self.theHeadName
  def headAdornment(self): return self.theHeadAdornment
  def headNavigation(self): return self.theHeadNav
  def headMultiplicity(self): return self.theHeadNry
  def headRole(self): return self.theHeadRole
  def tailRole(self): return self.theTailRole
  def tailMultiplicity(self): return self.theTailNry
  def tailNavigation(self): return self.theTailNav
  def tailAdornment(self): return self.theTailAdornment
  def tailAsset(self): return self.theTailName
