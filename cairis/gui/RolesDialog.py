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
from cairis.core.Role import Role
from RoleDialog import RoleDialog
from DialogClassParameters import DialogClassParameters
from cairis.core.ARM import *
from DimensionBaseDialog import DimensionBaseDialog

__author__ = 'Shamal Faily'

class RolesDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,ROLES_ID,'Roles',(800,300),'role.png')
    idList = [ROLES_LISTROLES_ID,ROLES_BUTTONADD_ID,ROLES_BUTTONDELETE_ID]
    columnList = ['Name','Short Code','Type']
    self.buildControls(idList,columnList,self.dbProxy.getRoles,'role')
    listCtrl = self.FindWindowById(ROLES_LISTROLES_ID)
    listCtrl.SetColumnWidth(0,150)
    listCtrl.SetColumnWidth(1,100)
    listCtrl.SetColumnWidth(2,400)


  def addObjectRow(self,listCtrl,listRow,role):
    listCtrl.InsertStringItem(listRow,role.name())
    listCtrl.SetStringItem(listRow,1,role.shortCode())
    listCtrl.SetStringItem(listRow,2,role.type())

  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters(ROLE_ID,'Add role',RoleDialog,ROLE_BUTTONCOMMIT_ID,self.dbProxy.addRole,True)
      self.addObject(addParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add role',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.selectedLabel]
    try:
      updateParameters = DialogClassParameters(ROLE_ID,'Edit role',RoleDialog,ROLE_BUTTONCOMMIT_ID,self.dbProxy.updateRole,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit role',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onDelete(self,evt):
    try:
      self.deleteObject('No role','Delete role',self.dbProxy.deleteRole)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete role',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return
