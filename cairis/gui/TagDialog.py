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

class TagDialog(wx.Dialog):
  def __init__(self,parent,tags):
    wx.Dialog.__init__(self,parent,-1,'Edit tags',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=wx.DefaultSize)
    mainSizer = wx.BoxSizer(wx.VERTICAL)

    tagBuf = ''
    for idx,tag in enumerate(tags):
      tagBuf += tag 
      if idx < (len(tags) - 1):
        tagBuf += '\n' 

    self.tagEntryCtrl = wx.TextCtrl(self,-1,tagBuf,style=wx.TE_MULTILINE)
    mainSizer.Add(self.tagEntryCtrl,1,wx.EXPAND)
    buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(buttonSizer,0,wx.CENTER)
    updateButton = wx.Button(self,wx.ID_OK,'Update')
    buttonSizer.Add(updateButton)
    cancelButton = wx.Button(self,wx.ID_CANCEL,'Cancel')
    buttonSizer.Add(cancelButton)
    self.SetSizer(mainSizer)

  def tags(self):
    return self.tagEntryCtrl.GetValue().split('\n')
