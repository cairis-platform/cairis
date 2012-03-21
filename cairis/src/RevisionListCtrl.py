#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/RevisionListCtrl.py $ $Id: RevisionListCtrl.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
from datetime import datetime
from RevisionEntryDialog import RevisionEntryDialog

class RevisionListCtrl(wx.ListCtrl):
  def __init__(self,parent):
    wx.ListCtrl.__init__(self,parent,armid.PROJECTSETTINGS_LISTREVISIONS_ID,size=wx.DefaultSize,style=wx.LC_REPORT | wx.LC_SORT_ASCENDING)
    self.InsertColumn(0,'No')
    self.SetColumnWidth(0,100)
    self.InsertColumn(1,'Date')
    self.SetColumnWidth(1,100)
    self.InsertColumn(2,'Remarks')
    self.SetColumnWidth(2,100)
    self.theSelectedIdx = -1
    self.theLastRevision = 0
    self.theMenu = wx.Menu()
    self.theMenu.Append(armid.CONTRIBUTORLISTCTRL_MENUADD_ID,'Add')
    self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK,self.OnRightDown)
    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    wx.EVT_MENU(self.theMenu,armid.CONTRIBUTORLISTCTRL_MENUADD_ID,self.onAddEntry)

  def OnItemSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()

  def OnItemDeselected(self,evt):
    self.theSelectedIdx = -1

  def OnRightDown(self,evt):
    self.PopupMenu(self.theMenu)

  def onAddEntry(self,evt):
    dlg = RevisionEntryDialog(self)
    if (dlg.ShowModal() == armid.REVISIONENTRY_BUTTONCOMMIT_ID):
      revRemarks = dlg.remarks()
      self.theLastRevision += 1
      revNo = self.theLastRevision
      revDate = datetime.now().strftime("%y-%m-%d %H:%M:%S")
      idx = self.GetItemCount()
      self.InsertStringItem(idx,str(revNo))
      self.SetStringItem(idx,1,revDate)
      self.SetStringItem(idx,2,revRemarks)

  def load(self,entries):
    for revNo,revDate,revRemarks in entries:
      idx = self.GetItemCount()
      self.InsertStringItem(idx,str(revNo))
      self.theLastRevision = revNo
      self.SetStringItem(idx,1,revDate)
      self.SetStringItem(idx,2,revRemarks)

  def dimensions(self):
    entries = []
    for x in range(self.GetItemCount()):
      revNo = self.GetItemText(x)
      revDate = self.GetItem(x,1)
      revRemarks = self.GetItem(x,2)
      entries.append((int(revNo),revDate.GetText(),revRemarks.GetText()))
    return entries
