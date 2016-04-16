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

class DomainEntryDialog(wx.Dialog):
  def __init__(self,parent):
    wx.Dialog.__init__(self,parent,DOMAINENTRY_ID,'Add domain interface',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(300,300))
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theDomain = ''
    self.theConnectionDomain = ''
    self.thePhenomena = ''
    mainSizer = wx.BoxSizer(wx.VERTICAL)

    domList = self.dbProxy.getDimensionNames('domain')
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Domain',(87,30),DOMAINENTRY_COMBODOMAIN_ID,domList),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Phenomena',(87,30),DOMAINENTRY_TEXTPHENOMENA_ID),0,wx.EXPAND)
    cdList = [''] + domList
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Connection Domain',(87,30),DOMAINENTRY_COMBOCONNECTIONDOMAIN_ID,cdList),0,wx.EXPAND)
    mainSizer.Add(wx.StaticText(self,-1),1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildAddCancelButtonSizer(self,DOMAINENTRY_BUTTONCOMMIT_ID),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

    wx.EVT_BUTTON(self,DOMAINENTRY_BUTTONCOMMIT_ID,self.onCommit)
    self.commitLabel = 'Add'

  def onCommit(self,evt):
    domainCtrl = self.FindWindowById(DOMAINENTRY_COMBODOMAIN_ID)
    connectionDomainCtrl = self.FindWindowById(DOMAINENTRY_COMBOCONNECTIONDOMAIN_ID)
    phenomenaCtrl = self.FindWindowById(DOMAINENTRY_TEXTPHENOMENA_ID)
    self.theDomain = domainCtrl.GetValue()
    self.theConnectionDomain = connectionDomainCtrl.GetValue()
    self.thePhenomena = phenomenaCtrl.GetValue()
    if (len(self.theDomain) == 0):
      dlg = wx.MessageDialog(self,'No domain','Add domain interface',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    if (len(self.thePhenomena) == 0):
      dlg = wx.MessageDialog(self,'No phenomena','Add domain interface',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(DOMAINENTRY_BUTTONCOMMIT_ID)

  def domain(self): return self.theDomain
  def phenomena(self): return self.thePhenomena
  def connectionDomain(self): return self.theConnectionDomain
