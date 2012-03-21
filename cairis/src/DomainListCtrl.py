#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/DomainListCtrl.py $ $Id: DomainListCtrl.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
from DomainEntryDialog import DomainEntryDialog

class DomainListCtrl(wx.ListCtrl):
  def __init__(self,parent,winId):
    wx.ListCtrl.__init__(self,parent,winId,size=wx.DefaultSize,style=wx.LC_REPORT | wx.LC_SORT_ASCENDING)
    self.InsertColumn(0,'Domain')
    self.SetColumnWidth(0,100)
    self.InsertColumn(1,'Phenomena')
    self.SetColumnWidth(1,300)
    self.InsertColumn(2,'Connection Domain')
    self.SetColumnWidth(2,100)
    self.theSelectedIdx = -1
    self.theMenu = wx.Menu()
    self.theMenu.Append(armid.DOMAINLISTCTRL_MENUADD_ID,'Add')
    self.theMenu.Append(armid.DOMAINLISTCTRL_MENUDELETE_ID,'Delete')
    self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK,self.OnRightDown)
    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    wx.EVT_MENU(self.theMenu,armid.DOMAINLISTCTRL_MENUADD_ID,self.onAddEntry)
    wx.EVT_MENU(self.theMenu,armid.DOMAINLISTCTRL_MENUDELETE_ID,self.onDeleteEntry)

  def OnItemSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()

  def OnItemDeselected(self,evt):
    self.theSelectedIdx = -1

  def OnRightDown(self,evt):
    self.PopupMenu(self.theMenu)

  def onAddEntry(self,evt):
    dlg = DomainEntryDialog(self)
    if (dlg.ShowModal() == armid.DOMAINENTRY_BUTTONCOMMIT_ID):
      domainName = dlg.domain()
      domainPhenomena = dlg.phenomena()
      connectionDomain = dlg.connectionDomain()
      idx = self.GetItemCount()
      self.InsertStringItem(idx,domainName)
      self.SetStringItem(idx,1,domainPhenomena)
      self.SetStringItem(idx,2,connectionDomain)

  def onDeleteEntry(self,evt):
    if (self.theSelectedIdx == -1):
      errorText = 'No entry selected'
      errorLabel = 'Delete domain association'
      dlg = wx.MessageDialog(self,errorText,errorLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
    else:
      selectedValue = self.GetItemText(self.theSelectedIdx)
      self.DeleteItem(self.theSelectedIdx)


  def load(self,entries):
    for association in entries:
      idx = self.GetItemCount()
      self.InsertStringItem(idx,association.tailDomain())
      self.SetStringItem(idx,1,association.phenomena())
      self.SetStringItem(idx,2,association.connectionDomain())

  def dimensions(self):
    entries = []
    for x in range(self.GetItemCount()):
      domainName = self.GetItemText(x)
      domainPhenomena = self.GetItem(x,1)
      connectionDomain = self.GetItem(x,2)
      entries.append((domainName,domainPhenomena.GetText(),connectionDomain.GetText()))
    return entries
