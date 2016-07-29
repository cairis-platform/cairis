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
from cairis.core.ARM import *
from cairis.core.Borg import Borg
from cairis.core.RoleParameters import RoleParameters
from RolePanel import RolePanel

__author__ = 'Shamal Faily'

class RoleDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,parameters.id(),parameters.label(),style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(475,400))
    self.theRoleId = -1
    self.theName = ''
    self.theType = ''
    self.theShortCode = ''
    self.theDescription = ''
    self.panel = 0
    self.buildControls(parameters)
    self.theCommitVerb = 'Create'

  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = RolePanel(self)
    self.panel.buildControls(parameters.createFlag())
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,ROLE_BUTTONCOMMIT_ID,self.onCommit)

  def load(self,role):
    self.theRoleId = role.id()
    self.panel.loadControls(role)
    self.theCommitVerb = 'Edit'
   

  def onCommit(self,evt):
    nameCtrl = self.FindWindowById(ROLE_TEXTNAME_ID)
    typeCtrl = self.FindWindowById(ROLE_COMBOTYPE_ID)
    scCtrl = self.FindWindowById(ROLE_TEXTSHORTCODE_ID)
    descCtrl = self.FindWindowById(ROLE_TEXTDESCRIPTION_ID)

    self.theName = nameCtrl.GetValue()
    if (self.theCommitVerb == 'Create'):
      b = Borg()
      try:
        b.dbProxy.nameCheck(self.theName,'role')
      except ARMException,errorText:
        dlg = wx.MessageDialog(self,str(errorText),'Add role',wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
        return

    self.theType = typeCtrl.GetValue()
    self.theShortCode = scCtrl.GetValue()
    self.theDescription = descCtrl.GetValue()

    commitLabel = self.theCommitVerb + ' role'

    if len(self.theName) == 0:
      dlg = wx.MessageDialog(self,'Role name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theType) == 0:
      dlg = wx.MessageDialog(self,'Role type cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theShortCode) == 0:
      dlg = wx.MessageDialog(self,'Short code cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif len(self.theDescription) == 0:
      dlg = wx.MessageDialog(self,'Role description cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(ROLE_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = RoleParameters(self.theName,self.theType,self.theShortCode,self.theDescription,[])
    parameters.setId(self.theRoleId)
    return parameters
