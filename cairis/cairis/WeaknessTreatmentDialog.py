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
from WeaknessTreatmentPanel import WeaknessTreatmentPanel

class WeaknessTreatmentDialog(wx.Dialog):
  def __init__(self,parent,targetName,cvName,reqName = '',assetName = '',effValue = '',tRat = ''):
    wx.Dialog.__init__(self,parent,-1,'Edit ' + targetName + ' treatment',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,300))
    self.theRequirementName = reqName
    self.theAssetName = assetName
    self.theEffectivenessValue = effValue
    self.theRationale = tRat
    
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = WeaknessTreatmentPanel(self,cvName)
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.WEAKNESSTREATMENT_BUTTONCOMMIT_ID,self.onCommit)

    if reqName != '':
      self.panel.loadControls(reqName,assetName,effValue)

  def onCommit(self,evt):
    reqCtrl = self.FindWindowById(armid.WEAKNESSTREATMENT_COMBOREQGOAL_ID)
    assetCtrl = self.FindWindowById(armid.WEAKNESSTREATMENT_COMBOASSET_ID)
    effCtrl = self.FindWindowById(armid.WEAKNESSTREATMENT_COMBOEFFECTIVENESS_ID)
    ratCtrl = self.FindWindowById(armid.WEAKNESSTREATMENT_TEXTRATIONALE_ID)

    self.theRequirementName = reqCtrl.GetValue()
    self.theAssetName = assetCtrl.GetValue()
    self.theEffectivenessValue = effCtrl.GetValue()
    self.theRationale = ratCtrl.GetValue()

    commitLabel = 'Edit weakness treatment'
    if len(self.theRequirementName) == 0:
      dlg = wx.MessageDialog(self,'Requirement name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theAssetName) == 0:
      dlg = wx.MessageDialog(self,'Asset name be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theEffectivenessValue) == 0:
      dlg = wx.MessageDialog(self,'Effectiveness cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theRationale) == 0:
      dlg = wx.MessageDialog(self,'Rationale cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(armid.WEAKNESSTREATMENT_BUTTONCOMMIT_ID)

  def requirement(self): return self.theRequirementName
  def asset(self): return self.theAssetName
  def effectiveness(self): return self.theEffectivenessValue
  def rationale(self): return self.theRationale
