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
from DomainListCtrl import DomainListCtrl

class DetailsPage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)
    typeList = ['Causal','Biddable','Lexical']

    givenBox = wx.StaticBox(self,-1,'Given Domain')
    givenSizer = wx.StaticBoxSizer(givenBox,wx.HORIZONTAL)
    topSizer.Add(givenSizer,0,wx.EXPAND)
    self.givenCtrl = wx.CheckBox(self,armid.DOMAIN_CHECKGIVEN_ID)
    self.givenCtrl.SetValue(True)
    givenSizer.Add(self.givenCtrl,0,wx.EXPAND)
    topSizer.Add(WidgetFactory.buildComboSizerList(self,'Type',(87,30),armid.DOMAIN_COMBOTYPE_ID,typeList),0,wx.EXPAND)
    topSizer.Add(WidgetFactory.buildTextSizer(self,'Short Code',(87,30),armid.DOMAIN_TEXTSHORTCODE_ID),0,wx.EXPAND)
    topSizer.Add(WidgetFactory.buildMLTextSizer(self,'Description',(87,30),armid.DOMAIN_TEXTDESCRIPTION_ID),1,wx.EXPAND)
    self.SetSizer(topSizer)
    self.Bind(wx.EVT_COMBOBOX, self.onDomainTypeChange,id = armid.DOMAIN_COMBOTYPE_ID)

  def onDomainTypeChange(self,evt):
    typeCtrl = self.FindWindowById(armid.DOMAIN_COMBOTYPE_ID)
    dType = typeCtrl.GetValue()
    if (dType == 'Biddable'):
      self.givenCtrl.SetValue(True)
      self.givenCtrl.Disable()
    else:
      self.givenCtrl.Enable()
    
class DomainAssociationPage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    dBox = wx.StaticBox(self,-1)
    dBoxSizer = wx.StaticBoxSizer(dBox,wx.HORIZONTAL)
    topSizer.Add(dBoxSizer,1,wx.EXPAND)
    self.domainCtrl = DomainListCtrl(self,armid.DOMAIN_LISTDOMAINS_ID)
    dBoxSizer.Add(self.domainCtrl,1,wx.EXPAND)
    self.SetSizer(topSizer)

class DomainNotebook(wx.Notebook):
  def __init__(self,parent):
    wx.Notebook.__init__(self,parent,armid.DOMAIN_NOTEBOOKDOMAIN_ID)
    p1 = DetailsPage(self)
    p2 = DomainAssociationPage(self)
    self.AddPage(p1,'Details')
    self.AddPage(p2,'Associations')
