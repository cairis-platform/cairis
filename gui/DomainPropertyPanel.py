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
from BasePanel import BasePanel
import DomainProperty
from Borg import Borg

class DomainPropertyPanel(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,armid.DOMAINPROPERTY_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    
  def buildControls(self,isCreate,isUpdateable=True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(self.buildTextSizer('Name',(87,30),armid.DOMAINPROPERTY_TEXTNAME_ID),0,wx.EXPAND)
    mainSizer.Add(self.buildTagCtrlSizer((87,30),armid.DOMAINPROPERTY_TAGS_ID),0,wx.EXPAND)
    typeList = ['Hypothesis','Invariant']
    mainSizer.Add(self.buildComboSizerList('Type',(87,30),armid.DOMAINPROPERTY_COMBOTYPE_ID,typeList),0,wx.EXPAND)
    mainSizer.Add(self.buildTextSizer('Originator',(87,30),armid.DOMAINPROPERTY_TEXTORIGINATOR_ID),0,wx.EXPAND)
    mainSizer.Add(self.buildMLTextSizer('Description',(87,30),armid.DOMAINPROPERTY_TEXTDESCRIPTION_ID),1,wx.EXPAND)
    mainSizer.Add(self.buildCommitButtonSizer(armid.DOMAINPROPERTY_BUTTONCOMMIT_ID,isCreate),0,wx.CENTER)
    self.SetSizer(mainSizer)

  def loadControls(self,dp,isReadOnly=False):
    nameCtrl = self.FindWindowById(armid.DOMAINPROPERTY_TEXTNAME_ID)
    tagsCtrl = self.FindWindowById(armid.DOMAINPROPERTY_TAGS_ID)
    tagsCtrl.set(dp.tags())

    typeCtrl = self.FindWindowById(armid.DOMAINPROPERTY_COMBOTYPE_ID)
    origCtrl = self.FindWindowById(armid.DOMAINPROPERTY_TEXTORIGINATOR_ID)
    descCtrl = self.FindWindowById(armid.DOMAINPROPERTY_TEXTDESCRIPTION_ID)
    nameCtrl.SetValue(dp.name())
    typeCtrl.SetValue(dp.type())
    origCtrl.SetValue(dp.originator())
    descCtrl.SetValue(dp.description())
