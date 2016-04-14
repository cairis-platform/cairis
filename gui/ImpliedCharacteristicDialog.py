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
import ARM
from ImpliedCharacteristicPanel import ImpliedCharacteristicPanel
from ImpliedCharacteristicParameters import ImpliedCharacteristicParameters
from Borg import Borg

class ImpliedCharacteristicDialog(wx.Dialog):
  def __init__(self,parent,pName,fromCode,toCode,rtName):
    wx.Dialog.__init__(self,parent,-1,'Edit Implied Characteristic',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,500))
    self.thePersonaName = pName
    self.theFromCode = fromCode
    self.theToCode = toCode
    self.theRelationshipType = rtName

    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = ImpliedCharacteristicPanel(self,pName,fromCode,toCode,rtName)
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.IMPLIEDCHARACTERISTIC_BUTTONCOMMIT_ID,self.onCommit)

  def onCommit(self,evt):

    charCtrl = self.FindWindowById(armid.IMPLIEDCHARACTERISTIC_TEXTCHARACTERISTIC_ID)
    qualCtrl = self.FindWindowById(armid.IMPLIEDCHARACTERISTIC_TEXTQUALIFIER_ID)
    varCtrl = self.FindWindowById(armid.IMPLIEDCHARACTERISTIC_COMBOTYPE_ID)
    intCtrl = self.FindWindowById(armid.IMPLIEDCHARACTERISTIC_TEXTINTENTION_ID)
    itCtrl = self.FindWindowById(armid.IMPLIEDCHARACTERISTIC_COMBOINTENTIONTYPE_ID)

    charName = charCtrl.GetValue()
    qualName = qualCtrl.GetValue()
    charType = varCtrl.GetValue()
    intName = intCtrl.GetValue()
    intType = itCtrl.GetValue()

    lhsCodesCtrl = self.FindWindowById(armid.IMPLIEDCHARACTERISTIC_LISTLHS_ID)
    rhsCodesCtrl = self.FindWindowById(armid.IMPLIEDCHARACTERISTIC_LISTRHS_ID)

    lhsCodes = lhsCodesCtrl.dimensions()
    rhsCodes = rhsCodesCtrl.dimensions()
    p = ImpliedCharacteristicParameters(self.thePersonaName,self.theFromCode,self.theToCode,self.theRelationshipType,charName,qualName,lhsCodes,rhsCodes,charType)
    p.setIntention(intName)
    p.setIntentionType(intType)
   
    b = Borg()
    b.dbProxy.updateImpliedCharacteristic(p)
    self.EndModal(wx.ID_CLOSE)
