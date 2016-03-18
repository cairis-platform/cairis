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
from TagDialog import TagDialog

class TagCtrl(wx.TextCtrl):
  def __init__(self,parent,winId):
    wx.TextCtrl.__init__(self,parent,winId,'',style=wx.TE_READONLY)
    self.theTags = []
    self.Bind(wx.EVT_LEFT_DCLICK,self.onDoubleClick)

  def onDoubleClick(self,evt):
    dlg = TagDialog(self,self.theTags)
    if (dlg.ShowModal() == wx.ID_OK):
      self.theTags = dlg.tags()
    self.SetValue(",".join(self.theTags))

  def set(self,tags):
    self.theTags = tags
    self.SetValue(",".join(self.theTags))

  def tags(self):
    return self.theTags
