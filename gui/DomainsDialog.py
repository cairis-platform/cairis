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
import Domain
from DomainDialog import DomainDialog
from DialogClassParameters import DialogClassParameters
from DimensionBaseDialog import DimensionBaseDialog

import ARM

class DomainsDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,armid.DOMAINS_ID,'Domains',(930,300),'domain.png')
    self.rmFrame = parent
    idList = [armid.DOMAINS_DOMAINLIST_ID,armid.DOMAINS_BUTTONADD_ID,armid.DOMAINS_BUTTONDELETE_ID]
    columnList = ['Name','Type','Short Code','Description']
    self.buildControls(idList,columnList,self.dbProxy.getDomains,'domain')
    listCtrl = self.FindWindowById(armid.DOMAINS_DOMAINLIST_ID)
    listCtrl.SetColumnWidth(0,150)
    listCtrl.SetColumnWidth(1,100)
    listCtrl.SetColumnWidth(2,100)
    listCtrl.SetColumnWidth(3,300)


  def addObjectRow(self,listCtrl,listRow,objt):
    listCtrl.InsertStringItem(listRow,objt.name())
    listCtrl.SetStringItem(listRow,1,objt.type())
    listCtrl.SetStringItem(listRow,2,objt.shortCode())
    listCtrl.SetStringItem(listRow,3,objt.description())

  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters(armid.DOMAIN_ID,'Add Domain',DomainDialog,armid.DOMAIN_BUTTONCOMMIT_ID,self.dbProxy.addDomain,True)
      self.addObject(addParameters)
      self.rmFrame.updateDomainSelection(self.selectedLabel)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add Domain',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.selectedLabel]
    assetId = selectedObjt.id()
    try:
      updateParameters = DialogClassParameters(armid.DOMAIN_ID,'Edit Domain',DomainDialog,armid.DOMAIN_BUTTONCOMMIT_ID,self.dbProxy.updateDomain,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Domain',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No Domain','Delete Domain',self.dbProxy.deleteDomain)
      self.rmFrame.updateDomainSelection()
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete Domain',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy
