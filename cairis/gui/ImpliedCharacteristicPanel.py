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
from cairis.core.ARM import NoImpliedCharacteristic
from BasePanel import BasePanel
from cairis.core.Borg import Borg
from ImpliedCharacteristicElementsListCtrl import ImpliedCharacteristicElementsListCtrl
from CodeNetworkModel import CodeNetworkModel
from CodeNetworkView import CodeNetworkView

class ImpliedCharacteristicPanel(BasePanel):
  def __init__(self,parent,pName,fromCode,toCode,rtName):
    BasePanel.__init__(self,parent,IMPLIEDCHARACTERISTIC_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    
    charName = ''
    qualName = 'Unknown'
    varName = 'Intrinsic'

    try:
      charName,qualName,varName = self.dbProxy.impliedCharacteristic(pName,fromCode,toCode,rtName)
    except NoImpliedCharacteristic, e:
      self.dbProxy.initialiseImpliedCharacteristic(pName,fromCode,toCode,rtName)

    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.codeNetView = CodeNetworkView(self,IMPLIEDCHARACTERISTIC_IMAGENETWORK_ID)
    mainSizer.Add(self.codeNetView,1,wx.EXPAND)
    codeNet = CodeNetworkModel(self.dbProxy.personaCodeNetwork(pName,fromCode,toCode),pName)
    codeNet.graph()
    self.codeNetView.reloadImage()
    mainSizer.Add(self.buildTextSizer('Characteristic',(87,30),IMPLIEDCHARACTERISTIC_TEXTCHARACTERISTIC_ID),0,wx.EXPAND)
    mainSizer.Add(self.buildTextSizer('Qualifier',(87,30),IMPLIEDCHARACTERISTIC_TEXTQUALIFIER_ID),0,wx.EXPAND)

    intentionSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(intentionSizer,0,wx.EXPAND)

    intentionSizer.Add(self.buildTextSizer('Intention',(87,30),IMPLIEDCHARACTERISTIC_TEXTINTENTION_ID),1,wx.EXPAND)
    intentionSizer.Add(self.buildComboSizerList('Type',(87,30),IMPLIEDCHARACTERISTIC_COMBOINTENTIONTYPE_ID,['goal','softgoal']),1,wx.EXPAND)
    

    elSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(elSizer,1,wx.EXPAND)

    lhsBox = wx.StaticBox(self,-1,fromCode)
    lhsSizer = wx.StaticBoxSizer(lhsBox,wx.VERTICAL)
    elSizer.Add(lhsSizer,1,wx.EXPAND)
    lhsEls = self.dbProxy.impliedCharacteristicElements(pName,fromCode,toCode,rtName,1)
    lhsSizer.Add(ImpliedCharacteristicElementsListCtrl(self,IMPLIEDCHARACTERISTIC_LISTLHS_ID,lhsEls),1,wx.EXPAND)


    rhsBox = wx.StaticBox(self,-1,toCode)
    rhsSizer = wx.StaticBoxSizer(rhsBox,wx.VERTICAL)
    elSizer.Add(rhsSizer,1,wx.EXPAND)
    rhsEls = self.dbProxy.impliedCharacteristicElements(pName,fromCode,toCode,rtName,0)
    rhsSizer.Add(ImpliedCharacteristicElementsListCtrl(self,IMPLIEDCHARACTERISTIC_LISTRHS_ID,rhsEls),1,wx.EXPAND)
    mainSizer.Add(self.buildComboSizerList('Characteristic Type',(87,30),IMPLIEDCHARACTERISTIC_COMBOTYPE_ID,['Intrinsic','Contextual']),0,wx.EXPAND)

    mainSizer.Add(self.buildCommitButtonSizer(IMPLIEDCHARACTERISTIC_BUTTONCOMMIT_ID,False),0,wx.CENTER)
    self.SetSizer(mainSizer)

    charCtrl = self.FindWindowById(IMPLIEDCHARACTERISTIC_TEXTCHARACTERISTIC_ID)
    charCtrl.SetValue(charName)
    qualCtrl = self.FindWindowById(IMPLIEDCHARACTERISTIC_TEXTQUALIFIER_ID)
    qualCtrl.SetValue(qualName)
    varCtrl = self.FindWindowById(IMPLIEDCHARACTERISTIC_COMBOTYPE_ID)
    varCtrl.SetValue(varName)

    itValues = self.dbProxy.impliedCharacteristicIntention(charName,pName,fromCode,toCode,rtName)
    intCtrl = self.FindWindowById(IMPLIEDCHARACTERISTIC_TEXTINTENTION_ID)
    intCtrl.SetValue(itValues[0])
    itCtrl = self.FindWindowById(IMPLIEDCHARACTERISTIC_COMBOINTENTIONTYPE_ID)
    itCtrl.SetValue(itValues[1])

