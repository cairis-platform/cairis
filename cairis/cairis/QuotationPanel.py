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
from QuotationNotebook import QuotationNotebook
import Memo

class QuotationPanel(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,armid.QUOTATION_ID)
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(QuotationNotebook(self),1,wx.EXPAND)
    mainSizer.Add(self.buildCommitButtonSizer(armid.QUOTATION_BUTTONCOMMIT_ID,False),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)
