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
