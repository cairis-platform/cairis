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
import cairis.core.MySQLDatabaseProxy

class AssetAssociationDialog(wx.Dialog):
  def __init__(self,parent,dp,envName,assetProperties,headNav = 0,headAdornment = '',headNry = '',headRole='',tailRole='',tailNry='',tailAdornment='',tailNav = 0,tailName = ''):
    wx.Dialog.__init__(self,parent,ASSETASSOCIATION_ID,'Add Asset Association',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,500))
    self.dbProxy = dp
    self.theAssetProperties = assetProperties
    self.theCurrentEnvironment = envName
    self.theHeadNav = int(headNav)
    self.theHeadAdornment = headAdornment
    self.theHeadNry = headNry
    self.theHeadRole = headRole
    self.theTailRole = tailRole
    self.theTailNry = tailNry
    self.theTailAdornment = tailAdornment
    self.theTailNav = int(tailNav)
    self.theTailName = tailName
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    assets = self.dbProxy.environmentAssets(self.theCurrentEnvironment)
    associationTypes = ['Inheritance','Association','Aggregation','Composition','Dependency']
    multiplicityTypes = ['1','*','1..*']
    navs = ['0','1','-1']

    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Navigation',(87,30),ASSETASSOCIATION_COMBOHEADNAV_ID,navs),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Adornment',(87,30),ASSETASSOCIATION_COMBOHEADTYPE_ID,associationTypes),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'nry',(87,30),ASSETASSOCIATION_COMBOHEADMULTIPLICITY_ID,multiplicityTypes),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Role',(87,30),ASSETASSOCIATION_TEXTHEADROLE_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Role',(87,30),ASSETASSOCIATION_TEXTTAILROLE_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'nry',(87,30),ASSETASSOCIATION_COMBOTAILMULTIPLICITY_ID,multiplicityTypes),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Adornment',(87,30),ASSETASSOCIATION_COMBOTAILTYPE_ID,associationTypes),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Navigation',(87,30),ASSETASSOCIATION_COMBOTAILNAV_ID,navs),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Tail',(87,30),ASSETASSOCIATION_COMBOTAILASSET_ID,assets),0,wx.EXPAND)

    mainSizer.Add(WidgetFactory.buildAddCancelButtonSizer(self,ASSETASSOCIATION_BUTTONCOMMIT_ID),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

    wx.EVT_BUTTON(self,ASSETASSOCIATION_BUTTONCOMMIT_ID,self.onCommit)
    self.commitLabel = 'Add'
    if (len(self.theTailName) > 0):
      self.commitLabel = 'Edit'
      self.SetLabel('Edit Asset Association')
      headNavCtrl = self.FindWindowById(ASSETASSOCIATION_COMBOHEADNAV_ID)
      headNavCtrl.SetValue(str(self.theHeadNav))
      headTypeCtrl = self.FindWindowById(ASSETASSOCIATION_COMBOHEADTYPE_ID)
      headTypeCtrl.SetValue(self.theHeadAdornment)
      headNryCtrl = self.FindWindowById(ASSETASSOCIATION_COMBOHEADMULTIPLICITY_ID)
      headNryCtrl.SetValue(self.theHeadNry)
      headRoleCtrl = self.FindWindowById(ASSETASSOCIATION_TEXTHEADROLE_ID)
      headRoleCtrl.SetValue(self.theHeadRole)
      tailRoleCtrl = self.FindWindowById(ASSETASSOCIATION_TEXTTAILROLE_ID)
      tailRoleCtrl.SetValue(self.theTailRole)
      tailNryCtrl = self.FindWindowById(ASSETASSOCIATION_COMBOTAILMULTIPLICITY_ID)
      tailNryCtrl.SetValue(self.theTailNry)
      tailTypeCtrl = self.FindWindowById(ASSETASSOCIATION_COMBOTAILTYPE_ID)
      tailTypeCtrl.SetValue(self.theTailAdornment)
      tailNavCtrl = self.FindWindowById(ASSETASSOCIATION_COMBOTAILNAV_ID)
      tailNavCtrl.SetValue(str(self.theTailNav))
      tailCtrl = self.FindWindowById(ASSETASSOCIATION_COMBOTAILASSET_ID)
      tailCtrl.SetValue(self.theTailName)
      buttonCtrl = self.FindWindowById(ASSETASSOCIATION_BUTTONCOMMIT_ID)
      buttonCtrl.SetLabel('Edit')
      

  def onCommit(self,evt):
    headNavCtrl = self.FindWindowById(ASSETASSOCIATION_COMBOHEADNAV_ID)
    headTypeCtrl = self.FindWindowById(ASSETASSOCIATION_COMBOHEADTYPE_ID)
    headNryCtrl = self.FindWindowById(ASSETASSOCIATION_COMBOHEADMULTIPLICITY_ID)
    headRoleCtrl = self.FindWindowById(ASSETASSOCIATION_TEXTHEADROLE_ID)
    tailRoleCtrl = self.FindWindowById(ASSETASSOCIATION_TEXTTAILROLE_ID)
    tailNryCtrl = self.FindWindowById(ASSETASSOCIATION_COMBOTAILMULTIPLICITY_ID)
    tailTypeCtrl = self.FindWindowById(ASSETASSOCIATION_COMBOTAILTYPE_ID)
    tailNavCtrl = self.FindWindowById(ASSETASSOCIATION_COMBOTAILNAV_ID)
    tailCtrl = self.FindWindowById(ASSETASSOCIATION_COMBOTAILASSET_ID)

    self.theHeadNav = int(headNavCtrl.GetValue())
    self.theHeadAdornment = headTypeCtrl.GetValue()
    self.theHeadNry = headNryCtrl.GetValue()
    self.theHeadRole = headRoleCtrl.GetValue()
    self.theTailRole = tailRoleCtrl.GetValue()
    self.theTailNry = tailNryCtrl.GetValue()
    self.theTailAdornment = tailTypeCtrl.GetValue()
    self.theTailNav = int(tailNavCtrl.GetValue())
    self.theTailName = tailCtrl.GetValue()

    if (len(self.theHeadAdornment) == 0):
      dlg = wx.MessageDialog(self,'No head type selected',self.commitLabel + ' Asset Association',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theHeadNry) == 0):
      dlg = wx.MessageDialog(self,'No head multiplicity selected',self.commitLabel + ' Asset Association',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theTailNry) == 0):
      dlg = wx.MessageDialog(self,'No tail multiplicity selected',self.commitLabel + ' Asset Association',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theTailAdornment) == 0):
      dlg = wx.MessageDialog(self,'No tail type selected',self.commitLabel + ' Asset Association',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theTailName) == 0):
      dlg = wx.MessageDialog(self,'No tail asset selected',self.commitLabel + ' Asset Association',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      assocInconsistencies = self.dbProxy.reportAssociationTargetDependencies(self.theAssetProperties,self.theTailName,self.theCurrentEnvironment)
      if (assocInconsistencies > 0):
        incMsg = ''
        for msgLine in assocInconsistencies:
          incMsg += msgLine + '\n'
        incMsg += 'Do you want to continue?'
        incDlg = wx.MessageDialog(self,incMsg,'Asset inconsistency',wx.YES_NO)
        if (incDlg.ShowModal() == wx.ID_NO):
          incDlg.Destroy()
          self.EndModal(wx.ID_CANCEL)
          return
        else:
          incDlg.Destroy()
      self.EndModal(ASSETASSOCIATION_BUTTONCOMMIT_ID)

  def headAdornment(self): return self.theHeadAdornment
  def headNavigation(self): return self.theHeadNav
  def headMultiplicity(self): return self.theHeadNry
  def headRole(self): return self.theHeadRole
  def tailRole(self): return self.theTailRole
  def tailMultiplicity(self): return self.theTailNry
  def tailAdornment(self): return self.theTailAdornment
  def tailNavigation(self): return self.theTailNav
  def tailAsset(self): return self.theTailName
