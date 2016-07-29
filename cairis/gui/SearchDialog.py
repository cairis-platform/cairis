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
from cairis.core.ARM import *
from SearchPanel import SearchPanel
from cairis.core.Borg import Borg

__author__ = 'Shamal Faily'

class SearchDialog(wx.Dialog):
  def __init__(self,parent):
    wx.Dialog.__init__(self,parent,SEARCHMODEL_ID,'Search model',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(700,500))
    b = Borg()
    self.dbProxy = b.dbProxy
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = SearchPanel(self)
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,SEARCHMODEL_BUTTONFIND_ID,self.onFind)
    wx.EVT_BUTTON(self,SEARCHMODEL_BUTTONCLOSE_ID, self.onClose)

  def onFind(self,evt):
    ssCtrl = self.FindWindowById(SEARCHMODEL_TEXTSEARCHSTRING_ID)
    ssValue = ssCtrl.GetValue()

    if (len(ssValue) == 0) or (ssValue == ' '):
      dlg = wx.MessageDialog(self,'Search string empty','Search model',wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return

    listCtrl = self.FindWindowById(SEARCHMODEL_LISTRESULTS_ID)
    listCtrl.DeleteAllItems()
    searchOptionsCtrl = self.FindWindowById(SEARCHOPTIONSPANEL_ID)
    searchOptions = searchOptionsCtrl.optionFlags()

    try:
      searchResults = self.dbProxy.searchModel(ssValue,searchOptions)
      for idx,result in enumerate(searchResults):
        listCtrl.InsertStringItem(idx,result[0])
        listCtrl.SetStringItem(idx,1,result[1])
        listCtrl.SetStringItem(idx,2,result[2])
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Search model',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onClose(self, event):
    self.EndModal(SEARCHMODEL_BUTTONCLOSE_ID)
