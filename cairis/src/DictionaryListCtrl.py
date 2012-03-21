#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/DictionaryListCtrl.py $ $Id: DictionaryListCtrl.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
from DictionaryEntryDialog import DictionaryEntryDialog

class DictionaryListCtrl(wx.ListCtrl):
  def __init__(self,parent):
    wx.ListCtrl.__init__(self,parent,armid.PROJECTSETTINGS_LISTDICTIONARY_ID,size=wx.DefaultSize,style=wx.LC_REPORT | wx.LC_SORT_ASCENDING)
    self.keys = []
    self.InsertColumn(0,'Name')
    self.SetColumnWidth(0,150)
    self.InsertColumn(1,'Definition')
    self.SetColumnWidth(1,300)
    self.theSelectedIdx = -1
    self.theMenu = wx.Menu()
    self.theMenu.Append(armid.DICTIONARYLISTCTRL_MENUADD_ID,'Add')
    self.theMenu.Append(armid.DICTIONARYLISTCTRL_MENUDELETE_ID,'Delete')
    self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK,self.OnRightDown)
    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.onEntryActivated)
    wx.EVT_MENU(self.theMenu,armid.DICTIONARYLISTCTRL_MENUADD_ID,self.onAddEntry)
    wx.EVT_MENU(self.theMenu,armid.DICTIONARYLISTCTRL_MENUDELETE_ID,self.onDeleteEntry)

  def OnItemSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()

  def OnItemDeselected(self,evt):
    self.theSelectedIdx = -1

  def OnRightDown(self,evt):
    self.PopupMenu(self.theMenu)

  def onAddEntry(self,evt):
    dlg = DictionaryEntryDialog(self)
    if (dlg.ShowModal() == armid.DICTIONARYENTRY_BUTTONCOMMIT_ID):
      name = dlg.name()
      definition = dlg.definition()
      idx = self.GetItemCount()
      self.InsertStringItem(idx,name)
      self.SetStringItem(idx,1,definition)

  def onDeleteEntry(self,evt):
    if (self.theSelectedIdx == -1):
      errorText = 'No entry selected'
      errorLabel = 'Delete definition'
      dlg = wx.MessageDialog(self,errorText,errorLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
    else:
      selectedValue = self.GetItemText(self.theSelectedIdx)
      self.DeleteItem(self.theSelectedIdx)

  def onEntryActivated(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    name = self.GetItemText(self.theSelectedIdx)
    definition = self.GetItem(self.theSelectedIdx,1)
     
    dlg = DictionaryEntryDialog(self,name,definition.GetText())
    if (dlg.ShowModal() == armid.DICTIONARYENTRY_BUTTONCOMMIT_ID):
      self.SetStringItem(self.theSelectedIdx,0,dlg.name())
      self.SetStringItem(self.theSelectedIdx,1,dlg.definition())

  def load(self,entries):
    self.keys = entries.keys()
    self.keys.sort()
    
    for name in self.keys:
      idx = self.GetItemCount()
      self.InsertStringItem(idx,name)
      self.SetStringItem(idx,1,entries[name])

  def dimensions(self):
    entries = []
    for x in range(self.GetItemCount()):
      name = self.GetItemText(x)
      definition = self.GetItem(x,1)
      entries.append((name,definition.GetText()))
    return entries
