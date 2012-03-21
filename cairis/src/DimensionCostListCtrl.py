#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/DimensionCostListCtrl.py $ $Id: DimensionCostListCtrl.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
import ARM
from ResponseCostDialog import ResponseCostDialog

class DimensionCostListCtrl(wx.ListCtrl):
  def __init__(self,parent,winId,dimName,boxSize=wx.DefaultSize):
    wx.ListCtrl.__init__(self,parent,winId,size=boxSize,style=wx.LC_REPORT)
    self.dimName = dimName
    self.InsertColumn(0,self.dimName)
    self.SetColumnWidth(0,300)
    self.InsertColumn(1,'Cost')
    self.SetColumnWidth(1,150)
    self.theDimMenu = wx.Menu()
    self.theDimMenu.Append(armid.COSTLISTCTRL_MENUADD_ID,'Add')
    self.theDimMenu.Append(armid.COSTLISTCTRL_MENUDELETE_ID,'Delete')
    self.theSelectedIdx = -1
    self.Bind(wx.EVT_RIGHT_DOWN,self.OnRightDown)
    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    wx.EVT_MENU(self.theDimMenu,armid.COSTLISTCTRL_MENUADD_ID,self.onAddResponse)
    wx.EVT_MENU(self.theDimMenu,armid.COSTLISTCTRL_MENUDELETE_ID,self.onDeleteResponse)

  def OnItemSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()

  def OnItemDeselected(self,evt):
    self.theSelectedIdx = -1

  def OnRightDown(self,evt):
    self.PopupMenu(self.theDimMenu)

  def onAddResponse(self,evt):
    dlg = ResponseCostDialog(self)
    if (dlg.ShowModal() == armid.RESPONSECOST_BUTTONADD_ID):
      responseName = dlg.response()
      responseCost = dlg.cost()
      idx = self.GetItemCount()
      self.InsertStringItem(idx,responseName)
      self.SetStringItem(idx,1,responseCost)

  def onDeleteResponse(self,evt):
    if (self.theSelectedIdx == -1):
      errorText = 'No ' + self.dimName + ' selected'
      errorLabel = 'Delete Response Cost'
      dlg = wx.MessageDialog(self,errorText,errorLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
    else:
      selectedValue = self.GetItemText(self.theSelectedIdx)
      self.DeleteItem(self.theSelectedIdx)

  def load(self,responseCosts):
    for idx,responseCost in enumerate(responseCosts):
      response = responseCost[0]
      cost = responseCost[1]
      self.InsertStringItem(idx,response)
      self.SetStringItem(idx,1,cost)

  def responses(self):
    responseCosts = []
    for x in range(self.GetItemCount()):
      responseName = self.GetItemText(x)
      cost = (self.GetItem(x,1)).GetText()
      responseCosts.append( (responseName,cost) )
    return responseCosts
