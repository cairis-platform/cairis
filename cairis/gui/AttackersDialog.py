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
from AttackerDialog import AttackerDialog
from DialogClassParameters import DialogClassParameters
from DimensionBaseDialog import DimensionBaseDialog
from cairis.core.ARM import *

__author__ = 'Shamal Faily'

class AttackersDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,ATTACKERS_ID,'Attackers',(800,300),'attacker.png')
    idList = [ATTACKERS_ATTACKERLIST_ID,ATTACKERS_BUTTONADD_ID,ATTACKERS_BUTTONDELETE_ID]
    columnList = ['Name','Description']
    self.buildControls(idList,columnList,self.dbProxy.getAttackers,'attacker')
    listCtrl = self.FindWindowById(ATTACKERS_ATTACKERLIST_ID)
    listCtrl.SetColumnWidth(0,150)
    listCtrl.SetColumnWidth(1,600)
    
  def addObjectRow(self,attackerListCtrl,listRow,attacker):
    attackerListCtrl.InsertStringItem(listRow,attacker.name())
    attackerListCtrl.SetStringItem(listRow,1,attacker.description())

  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters(ATTACKER_ID,'Add attacker',AttackerDialog,ATTACKER_BUTTONCOMMIT_ID,self.dbProxy.addAttacker,creationFlag=True)
      self.addObject(addParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add attacker',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.selectedLabel]
    try:
      updateParameters = DialogClassParameters(ATTACKER_ID,'Edit attacker',AttackerDialog,ATTACKER_BUTTONCOMMIT_ID,self.dbProxy.updateAttacker,creationFlag=False)
      self.updateObject(selectedObjt,updateParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit attacker',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onDelete(self,evt):
    try:
      self.deleteObject('No attacker','Delete attacker',self.dbProxy.deleteAttacker)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete attacker',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return
