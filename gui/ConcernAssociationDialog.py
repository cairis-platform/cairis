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
import MySQLDatabaseProxy

class ConcernAssociationDialog(wx.Dialog):
  def __init__(self,parent,dp,envName,source='',sourceMultiplicity='',link='',target='',targetMultiplicity=''):
    wx.Dialog.__init__(self,parent,armid.CONCERNASSOCIATION_ID,'Add Concern Association',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,400))
    self.dbProxy = dp
    self.theCurrentEnvironment = envName
    self.theSource = source
    self.theSourceMultiplicity = sourceMultiplicity
    self.theLink = link
    self.theTarget = target
    self.theTargetMultiplicity = targetMultiplicity
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    assets = self.dbProxy.environmentAssets(self.theCurrentEnvironment)
    mTypes = ['1','*','1..*']
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'n',(87,30),armid.CONCERNASSOCIATION_COMBOSOURCEMULTIPLICITY_ID,mTypes),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Source',(87,30),armid.CONCERNASSOCIATION_COMBOSOURCE_ID,assets),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Link',(87,60),armid.CONCERNASSOCIATION_TEXTLINK_ID),0,wx.EXPAND,1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'n',(87,30),armid.CONCERNASSOCIATION_COMBOTARGETMULTIPLICITY_ID,mTypes),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Target',(87,30),armid.CONCERNASSOCIATION_COMBOTARGET_ID,assets),0,wx.EXPAND)
    mainSizer.Add(wx.StaticText(self,-1),1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildAddCancelButtonSizer(self,armid.CONCERNASSOCIATION_BUTTONCOMMIT_ID),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

    wx.EVT_BUTTON(self,armid.CONCERNASSOCIATION_BUTTONCOMMIT_ID,self.onCommit)
    self.commitLabel = 'Add'
    if (len(self.theSource) > 0):
      self.commitLabel = 'Edit'
      self.SetLabel('Edit Concern Association')
      smCtrl = self.FindWindowById(armid.CONCERNASSOCIATION_COMBOSOURCEMULTIPLICITY_ID)
      smCtrl.SetStringSelection(self.theSourceMultiplicity)
      sCtrl = self.FindWindowById(armid.CONCERNASSOCIATION_COMBOSOURCE_ID)
      sCtrl.SetStringSelection(self.theSource)
      lCtrl = self.FindWindowById(armid.CONCERNASSOCIATION_TEXTLINK_ID)
      lCtrl.SetValue(self.theLink)
      tmCtrl = self.FindWindowById(armid.CONCERNASSOCIATION_COMBOTARGETMULTIPLICITY_ID)
      tmCtrl.SetStringSelection(self.theTargetMultiplicity)
      tCtrl = self.FindWindowById(armid.CONCERNASSOCIATION_COMBOTARGET_ID)
      tCtrl.SetStringSelection(self.theTarget)
      buttonCtrl = self.FindWindowById(armid.CONCERNASSOCIATION_BUTTONCOMMIT_ID)
      buttonCtrl.SetLabel('Edit')
      

  def onCommit(self,evt):
    sCtrl = self.FindWindowById(armid.CONCERNASSOCIATION_COMBOSOURCE_ID)
    smCtrl = self.FindWindowById(armid.CONCERNASSOCIATION_COMBOSOURCEMULTIPLICITY_ID)
    lCtrl = self.FindWindowById(armid.CONCERNASSOCIATION_TEXTLINK_ID)
    tCtrl = self.FindWindowById(armid.CONCERNASSOCIATION_COMBOTARGET_ID)
    tmCtrl = self.FindWindowById(armid.CONCERNASSOCIATION_COMBOTARGETMULTIPLICITY_ID)

    self.theSource = sCtrl.GetStringSelection()
    self.theSourceMultiplicity = smCtrl.GetStringSelection()
    self.theLink = lCtrl.GetValue()
    self.theTarget = tCtrl.GetStringSelection()
    self.theTargetMultiplicity = tmCtrl.GetStringSelection()

    if (len(self.theSource) == 0):
      dlg = wx.MessageDialog(self,'No source selected',self.commitLabel + ' Concern Association',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theSourceMultiplicity) == 0):
      dlg = wx.MessageDialog(self,'No source multiplicity selected',self.commitLabel + ' Concern Association',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theLink) == 0):
      dlg = wx.MessageDialog(self,'No link entered',self.commitLabel + ' Concern Association',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theTarget) == 0):
      dlg = wx.MessageDialog(self,'No target selected',self.commitLabel + ' Concern Association',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theTargetMultiplicity) == 0):
      dlg = wx.MessageDialog(self,'No target multiplicity selected',self.commitLabel + ' Concern Association',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(armid.CONCERNASSOCIATION_BUTTONCOMMIT_ID)

  def source(self): return self.theSource
  def sourceMultiplicity(self): return self.theSourceMultiplicity
  def link(self): return self.theLink
  def target(self): return self.theTarget
  def targetMultiplicity(self): return self.theTargetMultiplicity
