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
import wx.combo

__author__ = 'Shamal Faily'

class ListCtrlComboPopup(wx.ListCtrl, wx.combo.ComboPopup):
  def __init__(self):
    self.PostCreate(wx.PreListCtrl())
    wx.combo.ComboPopup.__init__(self)

  def OnMotion(self, evt):
    item, flags = self.HitTest(evt.GetPosition())
    if (item >= 0):
      self.Select(item)
      self.curitem = item

  def OnLeftDown(self, evt):
    self.value = self.curitem
    self.Dismiss()

  def Create(self, parent):
    wx.ListCtrl.Create(self,parent,style = wx.LC_LIST | wx.LC_SINGLE_SEL | wx.SIMPLE_BORDER)
    self.Bind(wx.EVT_MOTION, self.OnMotion)
    self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
    return True

   
