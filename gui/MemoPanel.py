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
import Memo

class MemoPanel(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,armid.MEMO_ID)
    self.theId = None
    
  def buildControls(self,isCreate,lbl=''):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(self.buildTextSizer('Name',(87,30),armid.MEMO_TEXTNAME_ID),0,wx.EXPAND)
    mainSizer.Add(self.buildMLTextSizer('Description',(87,80),armid.MEMO_TEXTDESCRIPTION_ID),1,wx.EXPAND)
    mainSizer.Add(self.buildCommitButtonSizer(armid.MEMO_BUTTONCOMMIT_ID,isCreate),0,wx.CENTER)
    self.SetSizer(mainSizer)

  def loadControls(self,objt,isReadOnly=False):
    self.theId = objt.id()
    nameCtrl = self.FindWindowById(armid.MEMO_TEXTNAME_ID)
    descCtrl = self.FindWindowById(armid.MEMO_TEXTDESCRIPTION_ID)

    nameCtrl.SetValue(objt.name())
    descCtrl.SetValue(objt.description())
