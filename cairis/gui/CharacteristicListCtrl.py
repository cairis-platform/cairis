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

from ObjectListCtrl import ObjectListCtrl
from ReferenceSynopsisDialog import ReferenceSynopsisDialog
from Borg import Borg

class CharacteristicListCtrl(ObjectListCtrl):
  def __init__(self,parent,winId,pName = ''):
    ObjectListCtrl.__init__(self,parent,winId)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theSelectedIdx = -1
    self.thePersonaName = pName
    self.theMenu = wx.Menu()
    self.theMenu.Append(armid.CLC_MENU_REFERENCESYNOPSIS_ID,'Characteristic Synopsis')
    wx.EVT_MENU(self,armid.CLC_MENU_REFERENCESYNOPSIS_ID,self.onCharacteristicSynopsis)

    self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onRightClick)
    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)

    self.rsItem = self.theMenu.FindItemById(armid.CLC_MENU_REFERENCESYNOPSIS_ID)
    self.rsItem.Enable(False)

  def onRightClick(self,evt):
    self.PopupMenu(self.theMenu)

  def OnItemSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    self.rsItem.Enable(True)

  def OnItemDeselected(self,evt):
    self.theSelectedIdx = -1
    self.rsItem.Enable(False)

  def onCharacteristicSynopsis(self,evt):
    refName = self.GetItemText(self.theSelectedIdx)
    rs = self.dbProxy.getCharacteristicSynopsis(refName)
    if (self.thePersonaName != ''):
      cDetails = ('persona',self.thePersonaName)
    else:
      cDetails = None 
    dlg = ReferenceSynopsisDialog(self,rs,cDetails)
    if (dlg.ShowModal() == armid.REFERENCESYNOPSIS_BUTTONCOMMIT_ID):
      if (rs.id() == -1):
        self.dbProxy.addCharacteristicSynopsis(dlg.parameters()) 
      else: 
        self.dbProxy.updateCharacteristicSynopsis(dlg.parameters()) 
