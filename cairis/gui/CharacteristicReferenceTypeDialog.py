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

__author__ = 'Shamal Faily'

class CharacteristicReferenceTypeDialog(wx.Dialog):
  def __init__(self,parent,ciName,elName,currentValue):
    wx.Dialog.__init__(self,parent,CHARACTERISTICREFERENCETYPE_ID,'Edit Characteristic Reference Type',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(300,400))

    self.theElementName = elName
    self.theValue = currentValue
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Characteristic Reference Type',(87,30),CHARACTERISTICREFERENCETYPE_COMBOVALUE_ID,['grounds','warrant','rebuttal']),0,wx.EXPAND)
    
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Characteristic Intention',(87,30),CHARACTERISTICREFERENCETYPE_TEXTCHARINTENT_ID),0,wx.EXPAND)
    ciCtrl = self.FindWindowById(CHARACTERISTICREFERENCETYPE_TEXTCHARINTENT_ID)
    ciCtrl.Disable()

    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Intention',(87,30),CHARACTERISTICREFERENCETYPE_TEXTINTENTION_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Intention Type',(87,30),CHARACTERISTICREFERENCETYPE_COMBOINTTYPE_ID,['goal','softgoal']),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Means/End',(87,30),CHARACTERISTICREFERENCETYPE_COMBOMEANSEND_ID,['means','end']),0,wx.EXPAND)
    contType = ['Make','SomePositive','Help','Hurt','SomeNegative','Break']
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Contribution',(87,30),CHARACTERISTICREFERENCETYPE_COMBOCONTRIBUTION_ID,contType),0,wx.EXPAND)
  
    mainSizer.Add(wx.StaticText(self,-1,''),1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildCommitButtonSizer(self,CHARACTERISTICREFERENCETYPE_BUTTONCOMMIT_ID,False),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,CHARACTERISTICREFERENCETYPE_BUTTONCOMMIT_ID,self.onCommit)
    self.valueCtrl = self.FindWindowById(CHARACTERISTICREFERENCETYPE_COMBOVALUE_ID)
    self.valueCtrl.SetValue(currentValue)

    self.ciCtrl = self.FindWindowById(CHARACTERISTICREFERENCETYPE_TEXTCHARINTENT_ID)
    self.ciCtrl.SetValue(ciName)

    self.intCtrl = self.FindWindowById(CHARACTERISTICREFERENCETYPE_TEXTINTENTION_ID)
    self.intTypeCtrl = self.FindWindowById(CHARACTERISTICREFERENCETYPE_COMBOINTTYPE_ID)
    self.meCtrl = self.FindWindowById(CHARACTERISTICREFERENCETYPE_COMBOMEANSEND_ID)
    self.contCtrl = self.FindWindowById(CHARACTERISTICREFERENCETYPE_COMBOCONTRIBUTION_ID)

    b = Borg()
    intDetails = b.dbProxy.impliedCharacteristicElementIntention(ciName,elName)
    intName = intDetails[0]
    intDim = intDetails[1] 
    meName = intDetails[2]
    contName = intDetails[3]

    if intName != '':
      self.intCtrl.SetValue(intName)
      self.intTypeCtrl.SetValue(intDim)
      self.meCtrl.SetValue(meName)
      self.contCtrl.SetValue(contName) 

  def onCommit(self,evt):
    self.theValue = self.valueCtrl.GetValue()

    ciName = self.ciCtrl.GetValue()
    intName = self.intCtrl.GetValue()
    intDim = self.intTypeCtrl.GetValue()
    meName = self.meCtrl.GetValue()
    contName = self.contCtrl.GetValue()

    b = Borg()
    b.dbProxy.updateImpliedCharacteristicElementIntention(ciName,self.theElementName,intName,intDim,meName,contName)

    self.EndModal(CHARACTERISTICREFERENCETYPE_BUTTONCOMMIT_ID)

  def value(self): return self.theValue
