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
from QuotationListCtrl import QuotationListCtrl
from Borg import Borg

class QuotationsPanel(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,armid.QUOTATIONS_ID)
    b = Borg()
    self.dbProxy = b.dbProxy

    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(QuotationListCtrl(self,armid.QUOTATIONS_LISTQUOTATIONS_ID),1,wx.EXPAND)

    buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
    okButton = wx.Button(self,wx.ID_OK,"Ok")
    buttonSizer.Add(okButton)
    mainSizer.Add(buttonSizer,0,wx.EXPAND)
    self.SetSizer(mainSizer)
