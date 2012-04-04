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
from RequirementNotebook import RequirementNotebook

class RequirementDialog(wx.Dialog):
  def __init__(self,parent,assets,reqName= '',reqDesc = '',reqType = '',reqRationale = '',reqFC ='',reqAsset =''):
    wx.Dialog.__init__(self,parent,armid.PATTERNREQUIREMENT_ID,'Add Pattern Requirement',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,475))
    self.theTemplateAssets = assets
    self.theRequirementName = reqName
    self.theRequirementDescription = reqDesc
    self.theRequirementType = reqType
    self.theRequirementRationale = reqRationale
    self.theRequirementFitCriterion = reqFC
    self.theRequirementAsset = reqAsset
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    
    mainSizer.Add(RequirementNotebook(self,self.theTemplateAssets),1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildAddCancelButtonSizer(self,armid.PATTERNREQUIREMENT_BUTTONCOMMIT_ID),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

    wx.EVT_BUTTON(self,armid.PATTERNREQUIREMENT_BUTTONCOMMIT_ID,self.onCommit)
    self.commitLabel = 'Add'
    if (len(self.theRequirementDescription) > 0):
      self.commitLabel = 'Edit'
      self.SetLabel('Edit Requirement')
      typeCtrl = self.FindWindowById(armid.PATTERNREQUIREMENT_COMBOTYPE_ID)
      typeCtrl.SetStringSelection(self.theRequirementType)
      assetCtrl = self.FindWindowById(armid.PATTERNREQUIREMENT_COMBOASSET_ID)
      assetCtrl.SetStringSelection(self.theRequirementAsset)
      nameCtrl = self.FindWindowById(armid.PATTERNREQUIREMENT_TEXTNAME_ID)
      nameCtrl.SetValue(self.theRequirementName)
      descCtrl = self.FindWindowById(armid.PATTERNREQUIREMENT_TEXTDESCRIPTION_ID)
      descCtrl.SetValue(self.theRequirementDescription)
      rationaleCtrl = self.FindWindowById(armid.PATTERNREQUIREMENT_TEXTRATIONALE_ID)
      rationaleCtrl.SetValue(self.theRequirementRationale)
      fcCtrl = self.FindWindowById(armid.PATTERNREQUIREMENT_TEXTFITCRITERION_ID)
      fcCtrl.SetValue(self.theRequirementFitCriterion)
      buttonCtrl = self.FindWindowById(armid.PATTERNREQUIREMENT_BUTTONCOMMIT_ID)
      buttonCtrl.SetLabel('Edit')
      

  def onCommit(self,evt):
    typeCtrl = self.FindWindowById(armid.PATTERNREQUIREMENT_COMBOTYPE_ID)
    assetCtrl = self.FindWindowById(armid.PATTERNREQUIREMENT_COMBOASSET_ID)
    nameCtrl = self.FindWindowById(armid.PATTERNREQUIREMENT_TEXTNAME_ID)
    descCtrl = self.FindWindowById(armid.PATTERNREQUIREMENT_TEXTDESCRIPTION_ID)
    rationaleCtrl = self.FindWindowById(armid.PATTERNREQUIREMENT_TEXTRATIONALE_ID)
    fcCtrl = self.FindWindowById(armid.PATTERNREQUIREMENT_TEXTFITCRITERION_ID)

    self.theRequirementType = typeCtrl.GetStringSelection()
    self.theRequirementAsset = assetCtrl.GetStringSelection()
    self.theRequirementName = nameCtrl.GetValue()
    self.theRequirementDescription = descCtrl.GetValue()
    self.theRequirementRationale = rationaleCtrl.GetValue()
    self.theRequirementFitCriterion = fcCtrl.GetValue()

    if (len(self.theRequirementType) == 0):
      dlg = wx.MessageDialog(self,'No type selected',self.commitLabel + ' Pattern Requirement',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theRequirementAsset) == 0):
      dlg = wx.MessageDialog(self,'No asset selected',self.commitLabel + ' Pattern Requirement',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theRequirementName) == 0):
      dlg = wx.MessageDialog(self,'No name entered',self.commitLabel + ' Pattern Requirement',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theRequirementDescription) == 0):
      dlg = wx.MessageDialog(self,'No description entered',self.commitLabel + ' Pattern Requirement',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theRequirementRationale) == 0):
      dlg = wx.MessageDialog(self,'No rationale entered',self.commitLabel + ' Pattern Requirement',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theRequirementFitCriterion) == 0):
      dlg = wx.MessageDialog(self,'No fit criterion entered',self.commitLabel + ' Pattern Requirement',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(armid.PATTERNREQUIREMENT_BUTTONCOMMIT_ID)

  def type(self): return self.theRequirementType
  def asset(self): return self.theRequirementAsset
  def name(self): return self.theRequirementName
  def description(self): return self.theRequirementDescription
  def rationale(self): return self.theRequirementRationale
  def fitCriterion(self): return self.theRequirementFitCriterion
