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
from TemplateRequirementNotebook import TemplateRequirementNotebook

class TemplateRequirementPanel(BasePanel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,armid.TEMPLATEREQUIREMENT_ID)

  def buildControls(self,isCreate,isUpdateable=True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(TemplateRequirementNotebook(self),1,wx.EXPAND)
    mainSizer.Add(self.buildCommitButtonSizer(armid.TEMPLATEREQUIREMENT_BUTTONCOMMIT_ID,isCreate),0,wx.CENTER)
    self.SetSizer(mainSizer)

  def loadControls(self,req):
    nameCtrl = self.FindWindowById(armid.TEMPLATEREQUIREMENT_TEXTNAME_ID)
    assetCtrl = self.FindWindowById(armid.TEMPLATEREQUIREMENT_COMBOASSET_ID)
    descCtrl = self.FindWindowById(armid.TEMPLATEREQUIREMENT_TEXTDESCRIPTION_ID)
    typeCtrl = self.FindWindowById(armid.TEMPLATEREQUIREMENT_COMBOTYPE_ID)
    ratCtrl = self.FindWindowById(armid.TEMPLATEREQUIREMENT_TEXTRATIONALE_ID)
    fcCtrl = self.FindWindowById(armid.TEMPLATEREQUIREMENT_TEXTFITCRITERION_ID)

    nameCtrl.SetValue(req.name())
    assetCtrl.SetValue(req.asset())
    descCtrl.SetValue(req.description())
    typeCtrl.SetValue(req.type())
    ratCtrl.SetValue(req.rationale())
    fcCtrl.SetValue(req.fitCriterion())
