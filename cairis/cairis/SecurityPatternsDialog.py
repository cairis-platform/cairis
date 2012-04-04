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
import Asset
from SecurityPatternDialog import SecurityPatternDialog
from DialogClassParameters import DialogClassParameters
import ARM
from DimensionBaseDialog import DimensionBaseDialog

class SecurityPatternsDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,armid.SECURITYPATTERNS_ID,'Security Patterns',(930,300),'countermeasure.png')
    self.theMainWindow = parent
    idList = [armid.SECURITYPATTERNS_PATTERNLIST_ID,armid.SECURITYPATTERNS_BUTTONADD_ID,armid.SECURITYPATTERNS_BUTTONDELETE_ID]
    columnList = ['Name']
    self.buildControls(idList,columnList,self.dbProxy.getSecurityPatterns,'securitypattern')
    listCtrl = self.FindWindowById(armid.SECURITYPATTERNS_PATTERNLIST_ID)
    listCtrl.SetColumnWidth(0,300)


  def addObjectRow(self,listCtrl,listRow,pattern):
    listCtrl.InsertStringItem(listRow,pattern.name())

  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters(armid.SECURITYPATTERN_ID,'Add Security Pattern',SecurityPatternDialog,armid.SECURITYPATTERN_BUTTONCOMMIT_ID,self.dbProxy.addSecurityPattern,True)
      self.addObject(addParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add security pattern',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.selectedLabel]
    assetId = selectedObjt.id()
    try:
      updateParameters = DialogClassParameters(armid.SECURITYPATTERN_ID,'Edit Security Pattern',SecurityPatternDialog,armid.SECURITYPATTERN_BUTTONCOMMIT_ID,self.dbProxy.updateSecurityPattern,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit security pattern',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No security pattern','Delete security pattern',self.dbProxy.deleteSecurityPattern)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete security pattern',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy
