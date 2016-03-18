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
import armid
from BasePanel import BasePanel
from Borg import Borg

class ReferenceContributionPanel(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,armid.REFERENCECONTRIBUTION_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    refSynopses = self.dbProxy.getDimensionNames('reference_synopsis')
    mainSizer.Add(self.buildComboSizerList('Source',(87,30),armid.REFERENCECONTRIBUTION_COMBOSOURCE_ID,refSynopses),0,wx.EXPAND)
    charSynopses = self.dbProxy.getDimensionNames('characteristic_synopsis')
    mainSizer.Add(self.buildComboSizerList('Destination',(87,30),armid.REFERENCECONTRIBUTION_COMBODESTINATION_ID,charSynopses),0,wx.EXPAND)
    mainSizer.Add(self.buildComboSizerList('Means/End',(87,30),armid.REFERENCECONTRIBUTION_COMBOMEANSEND_ID,['means','end']),0,wx.EXPAND)
    contType = ['Make','SomePositive','Help','Hurt','SomeNegative','Break']
    mainSizer.Add(self.buildComboSizerList('Contribution',(87,30),armid.REFERENCECONTRIBUTION_COMBOCONTRIBUTION_ID,contType),0,wx.EXPAND)
    mainSizer.Add(self.buildCommitButtonSizer(armid.REFERENCECONTRIBUTION_BUTTONCOMMIT_ID,True),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)


  def load(self,objt):
    srcCtrl = self.FindWindowById(armid.REFERENCECONTRIBUTION_COMBOSOURCE_ID)
    destCtrl = self.FindWindowById(armid.REFERENCECONTRIBUTION_COMBODESTINATION_ID)
    meCtrl = self.FindWindowById(armid.REFERENCECONTRIBUTION_COMBOMEANSEND_ID)
    contCtrl = self.FindWindowById(armid.REFERENCECONTRIBUTION_COMBOCONTRIBUTION_ID)

    srcCtrl.SetValue(objt.source())
    destCtrl.SetValue(objt.destination())
    if (objt.meansEnd() != ''):
      meCtrl.SetValue(objt.meansEnd())
      contCtrl.SetValue(objt.contribution())
