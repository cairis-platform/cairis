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


#$URL$
import wx
from cairis.core.armid import *
from cairis.core.Borg import Borg
from BasePanel import BasePanel

class UseCaseContributionPanel(BasePanel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,USECASECONTRIBUTION_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    ucs = self.dbProxy.getDimensionNames('usecase')
    mainSizer.Add(self.buildComboSizerList('Use Case',(87,30),REFERENCECONTRIBUTION_COMBOSOURCE_ID,ucs),0,wx.EXPAND)
    charSynopses = self.dbProxy.getDimensionNames('characteristic_synopsis')
    mainSizer.Add(self.buildRadioButtonSizer('Referent',(87,30),[(REFERENCECONTRIBUTION_RADIOREFERENCE_ID,'Reference'),(REFERENCECONTRIBUTION_RADIOCHARACTERISTIC_ID,'Characteristic')]))
    refs = self.dbProxy.getDimensionNames('reference_synopsis')
    mainSizer.Add(self.buildComboSizerList('Reference',(87,30),REFERENCECONTRIBUTION_COMBODESTINATION_ID,refs),0,wx.EXPAND)
    mainSizer.Add(self.buildComboSizerList('Means/End',(87,30),REFERENCECONTRIBUTION_COMBOMEANSEND_ID,['means','end']),0,wx.EXPAND)
    contType = ['Make','SomePositive','Help','Hurt','SomeNegative','Break']
    mainSizer.Add(self.buildComboSizerList('Contribution',(87,30),REFERENCECONTRIBUTION_COMBOCONTRIBUTION_ID,contType),0,wx.EXPAND)
    mainSizer.Add(self.buildCommitButtonSizer(REFERENCECONTRIBUTION_BUTTONCOMMIT_ID,True),0,wx.ALIGN_CENTER)
    wx.EVT_RADIOBUTTON(self,REFERENCECONTRIBUTION_RADIOREFERENCE_ID,self.onReferenceSelected)
    wx.EVT_RADIOBUTTON(self,REFERENCECONTRIBUTION_RADIOCHARACTERISTIC_ID,self.onCharacteristicSelected)
    self.SetSizer(mainSizer)


  def load(self,objt,rType):
    srcCtrl = self.FindWindowById(REFERENCECONTRIBUTION_COMBOSOURCE_ID)
    destCtrl = self.FindWindowById(REFERENCECONTRIBUTION_COMBODESTINATION_ID)
    meCtrl = self.FindWindowById(REFERENCECONTRIBUTION_COMBOMEANSEND_ID)
    contCtrl = self.FindWindowById(REFERENCECONTRIBUTION_COMBOCONTRIBUTION_ID)

    srcCtrl.SetValue(objt.source())
    if (objt.meansEnd() != ''):
      if (rType == 'characteristic'):
        charRadio = self.FindWindowById(REFERENCECONTRIBUTION_RADIOCHARACTERISTIC_ID)
        charRadio.SetValue(True)
        chars = self.dbProxy.getDimensionNames('characteristic_synopsis')
        destCtrl.SetItems(chars)
      else:
        refRadio = self.FindWindowById(REFERENCECONTRIBUTION_RADIOCHARACTERISTIC_ID)
        refRadio.SetValue(True)
        refs = self.dbProxy.getDimensionNames('reference_synopsis')
        destCtrl.SetItems(refs)
      destCtrl.SetValue(objt.destination())
      meCtrl.SetValue(objt.meansEnd())
      contCtrl.SetValue(objt.contribution())

  def onReferenceSelected(self,evt):
    refCtrl = self.FindWindowById(REFERENCECONTRIBUTION_COMBODESTINATION_ID)
    refs = self.dbProxy.getDimensionNames('reference_synopsis')
    refCtrl.SetItems(refs)
    refCtrl.SetValue('')

  def onCharacteristicSelected(self,evt):
    refCtrl = self.FindWindowById(REFERENCECONTRIBUTION_COMBODESTINATION_ID)
    refs = self.dbProxy.getDimensionNames('characteristic_synopsis')
    refCtrl.SetItems(refs)
    refCtrl.SetValue('')
