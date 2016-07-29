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
from cairis.core.DomainParameters import DomainParameters
from DomainNotebook import DomainNotebook

__author__ = 'Shamal Faily'

class DomainDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,DOMAIN_ID,'Domain',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(350,400))
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theModuleId = -1
    self.theModuleName = ''
    self.theShortCode = ''
    self.theDescription = ''
    self.theType = ''
    self.isGiven = True
    self.theDomains = ''
    self.buildControls()
    self.commitVerb = 'Add'

  def buildControls(self):
    mainSizer = wx.BoxSizer(wx.VERTICAL)

    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Name',(87,30),DOMAIN_TEXTNAME_ID),0,wx.EXPAND)
    self.notebook = DomainNotebook(self)
    mainSizer.Add(self.notebook,1,wx.EXPAND)

    mainSizer.Add(WidgetFactory.buildAddCancelButtonSizer(self,DOMAIN_BUTTONCOMMIT_ID),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

    wx.EVT_BUTTON(self,DOMAIN_BUTTONCOMMIT_ID,self.onCommit)

  def load(self,reqMod):
    self.theModuleId = reqMod.id()
    nameCtrl = self.FindWindowById(DOMAIN_TEXTNAME_ID)
    typeCtrl = self.notebook.FindWindowById(DOMAIN_COMBOTYPE_ID)
    givenCtrl = self.notebook.FindWindowById(DOMAIN_CHECKGIVEN_ID)
    shortCodeCtrl = self.notebook.FindWindowById(DOMAIN_TEXTSHORTCODE_ID)
    descriptionCtrl = self.notebook.FindWindowById(DOMAIN_TEXTDESCRIPTION_ID)
    domainsCtrl = self.notebook.FindWindowById(DOMAIN_LISTDOMAINS_ID)
    buttonCtrl = self.FindWindowById(DOMAIN_BUTTONCOMMIT_ID)
    buttonCtrl.SetLabel('Edit')
  
    self.theModuleName = reqMod.name()
    self.theType = reqMod.type()
    self.isGiven = reqMod.given()
    self.theShortCode = reqMod.shortCode()
    self.theDescription = reqMod.description()
    self.theDomains = reqMod.domains()

    nameCtrl.SetValue(self.theModuleName)
    typeCtrl.SetValue(self.theType)
    givenCtrl.SetValue(self.isGiven)
    shortCodeCtrl.SetValue(self.theShortCode)
    descriptionCtrl.SetValue(self.theDescription)
    domainsCtrl.load(self.theDomains)

    if (self.theType == 'Biddable'):
      givenCtrl.Disable()
    
    self.commitVerb = 'Edit'
    
  def onCommit(self,evt):
    commitLabel = self.commitVerb + ' Domain'
    nameCtrl = self.FindWindowById(DOMAIN_TEXTNAME_ID)
    typeCtrl = self.notebook.FindWindowById(DOMAIN_COMBOTYPE_ID)
    givenCtrl = self.notebook.FindWindowById(DOMAIN_CHECKGIVEN_ID)
    shortCodeCtrl = self.notebook.FindWindowById(DOMAIN_TEXTSHORTCODE_ID)
    descriptionCtrl = self.notebook.FindWindowById(DOMAIN_TEXTDESCRIPTION_ID)
    domainsCtrl = self.notebook.FindWindowById(DOMAIN_LISTDOMAINS_ID)
    

    self.theModuleName = nameCtrl.GetValue()
    self.theType = typeCtrl.GetValue()
    self.isGiven = givenCtrl.GetValue()
    self.theShortCode = shortCodeCtrl.GetValue()
    self.theDescription = descriptionCtrl.GetValue()
    self.theDomains = domainsCtrl.dimensions()

    if len(self.theModuleName) == 0:
      dlg = wx.MessageDialog(self,'No domain name',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theType) == 0:
      dlg = wx.MessageDialog(self,'No domain type',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif len(self.theShortCode) == 0:
      dlg = wx.MessageDialog(self,'No short code',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theDescription) == 0):
      dlg = wx.MessageDialog(self,'No description',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(DOMAIN_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = DomainParameters(self.theModuleName,self.theShortCode,self.theDescription,self.theType,self.isGiven,self.theDomains)
    parameters.setId(self.theModuleId)
    return parameters
