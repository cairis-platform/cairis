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
from BasePanel import BasePanel
import cairis.core.Code
from CodeNotebook import CodeNotebook

class CodePanel(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,CODE_ID)
    self.theId = None
    
  def buildControls(self,isCreate,lbl=''):
    mainSizer = wx.BoxSizer(wx.VERTICAL)

    nb = CodeNotebook(self)
    mainSizer.Add(nb,1,wx.EXPAND)
    if lbl != 'View Code':
      mainSizer.Add(self.buildCommitButtonSizer(CODE_BUTTONCOMMIT_ID,isCreate),0,wx.CENTER)
    else:
      nameCtrl = self.FindWindowById(CODE_TEXTNAME_ID)
      typeCtrl = self.FindWindowById(CODE_COMBOTYPE_ID)
      descCtrl = self.FindWindowById(CODE_TEXTDESCRIPTION_ID)
      incCritCtrl = self.FindWindowById(CODE_TEXTINCLUSIONCRITERIA_ID)
      codeEgCtrl = self.FindWindowById(CODE_TEXTEXAMPLE_ID)
      nameCtrl.Disable()
      typeCtrl.Disable()
      descCtrl.Disable()
      incCritCtrl.Disable()
      codeEgCtrl.Disable()
      closeCtrl = self.FindWindowById(wx.ID_CLOSE)
      closeCtrl.Enable()

    self.SetSizer(mainSizer)

  def loadControls(self,objt,isReadOnly=False):
    self.theId = objt.id()
    nameCtrl = self.FindWindowById(CODE_TEXTNAME_ID)
    typeCtrl = self.FindWindowById(CODE_COMBOTYPE_ID)
    descCtrl = self.FindWindowById(CODE_TEXTDESCRIPTION_ID)
    incCritCtrl = self.FindWindowById(CODE_TEXTINCLUSIONCRITERIA_ID)
    codeEgCtrl = self.FindWindowById(CODE_TEXTEXAMPLE_ID)

    nameCtrl.SetValue(objt.name())
    typeCtrl.SetValue(objt.type())
    descCtrl.SetValue(objt.description())
    incCritCtrl.SetValue(objt.inclusionCriteria())
    codeEgCtrl.SetValue(objt.example())
