#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/AssetAssociationListCtrl.py $ $Id: AssetAssociationListCtrl.py 439 2011-03-19 22:01:02Z shaf $
import wx
import armid
import ARM
from AssetAssociationDialog import AssetAssociationDialog

class AssetAssociationListCtrl(wx.ListCtrl):
  def __init__(self,parent,winId,dp,pList,boxSize=wx.DefaultSize):
    wx.ListCtrl.__init__(self,parent,winId,size=boxSize,style=wx.LC_REPORT)
    self.dbProxy = dp
    self.assetPropertyList = pList
    self.theCurrentEnvironment = ''
    self.InsertColumn(0,'Nav')
    self.SetColumnWidth(0,50)
    self.InsertColumn(1,'Type')
    self.SetColumnWidth(1,75)
    self.InsertColumn(2,'Nry')
    self.SetColumnWidth(2,50)
    self.InsertColumn(3,'Role')
    self.SetColumnWidth(3,50)
    self.InsertColumn(4,'Tail Role')
    self.SetColumnWidth(4,50)
    self.InsertColumn(5,'Tail Nry')
    self.SetColumnWidth(5,50)
    self.InsertColumn(6,'Tail Type')
    self.SetColumnWidth(6,75)
    self.InsertColumn(7,'Tail Nav')
    self.SetColumnWidth(7,50)
    self.InsertColumn(8,'Tail Asset')
    self.SetColumnWidth(8,100)
    self.theSelectedIdx = -1
    self.theDimMenu = wx.Menu()
    self.theDimMenu.Append(armid.AA_MENUADD_ID,'Add')
    self.theDimMenu.Append(armid.AA_MENUDELETE_ID,'Delete')
    self.Bind(wx.EVT_RIGHT_DOWN,self.OnRightDown)
    wx.EVT_MENU(self.theDimMenu,armid.AA_MENUADD_ID,self.onAddAssociation)
    wx.EVT_MENU(self.theDimMenu,armid.AA_MENUDELETE_ID,self.onDeleteAssociation)

    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.onAssetActivated)

  def setEnvironment(self,environmentName):
    self.theCurrentEnvironment = environmentName

  def OnRightDown(self,evt):
    self.PopupMenu(self.theDimMenu)

  def onAddAssociation(self,evt):
    syProperties,syRationale = self.assetPropertyList.properties()
    dlg = AssetAssociationDialog(self,self.dbProxy,self.theCurrentEnvironment,syProperties)
    if (dlg.ShowModal() == armid.ASSETASSOCIATION_BUTTONCOMMIT_ID):
      self.theSelectedIdx = self.GetItemCount()
      self.InsertStringItem(self.theSelectedIdx,str(dlg.headNavigation()))
      self.SetStringItem(self.theSelectedIdx,1,dlg.headAdornment())
      self.SetStringItem(self.theSelectedIdx,2,dlg.headMultiplicity())
      self.SetStringItem(self.theSelectedIdx,3,dlg.headRole())
      self.SetStringItem(self.theSelectedIdx,4,dlg.tailRole())
      self.SetStringItem(self.theSelectedIdx,5,dlg.tailMultiplicity())
      self.SetStringItem(self.theSelectedIdx,6,dlg.tailAdornment())
      self.SetStringItem(self.theSelectedIdx,7,str(dlg.tailNavigation()))
      self.SetStringItem(self.theSelectedIdx,8,dlg.tailAsset())

  def onDeleteAssociation(self,evt):
    if (self.theSelectedIdx == -1):
      errorText = 'No association selected'
      errorLabel = 'Delete asset association'
      dlg = wx.MessageDialog(self,errorText,errorLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
    else:
      selectedValue = self.GetItemText(self.theSelectedIdx)
      self.DeleteItem(self.theSelectedIdx)

  
  def OnItemSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()

  def OnItemDeselected(self,evt):
    self.theSelectedIdx = -1

  def onAssetActivated(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    headNav = int(self.GetItemText(self.theSelectedIdx))
    headAdornment = self.GetItem(self.theSelectedIdx,1)
    headNry = self.GetItem(self.theSelectedIdx,2)
    headRole = self.GetItem(self.theSelectedIdx,3)
    tailRole = self.GetItem(self.theSelectedIdx,4)
    tailNry = self.GetItem(self.theSelectedIdx,5)
    tailAdornment = self.GetItem(self.theSelectedIdx,6)
    tailNav = self.GetItem(self.theSelectedIdx,7)
    tailAsset = self.GetItem(self.theSelectedIdx,8)
     
    syProperties,syRationale = self.assetPropertyList.properties()
    dlg = AssetAssociationDialog(self,self.dbProxy,self.theCurrentEnvironment,syProperties,headNav,headAdornment.GetText(),headNry.GetText(),headRole.GetText(),tailRole.GetText(),tailNry.GetText(),tailAdornment.GetText(),int(tailNav.GetText()),tailAsset.GetText())
    if (dlg.ShowModal() == armid.ASSETASSOCIATION_BUTTONCOMMIT_ID):
      self.SetStringItem(self.theSelectedIdx,0,str(dlg.headNavigation()))
      self.SetStringItem(self.theSelectedIdx,1,dlg.headAdornment())
      self.SetStringItem(self.theSelectedIdx,2,dlg.headMultiplicity())
      self.SetStringItem(self.theSelectedIdx,3,dlg.headRole())
      self.SetStringItem(self.theSelectedIdx,4,dlg.tailRole())
      self.SetStringItem(self.theSelectedIdx,5,dlg.tailMultiplicity())
      self.SetStringItem(self.theSelectedIdx,6,dlg.tailAdornment())
      self.SetStringItem(self.theSelectedIdx,7,str(dlg.tailNavigation()))
      self.SetStringItem(self.theSelectedIdx,8,dlg.tailAsset())

  def load(self,assets):
    for headNav,headAdornment,headNry,headRole,tailRole,tailNry,tailAdornment,tailNav,tailAsset in assets:
      idx = self.GetItemCount()
      self.InsertStringItem(idx,str(headNav))
      self.SetStringItem(idx,1,headAdornment)
      self.SetStringItem(idx,2,headNry)
      self.SetStringItem(idx,3,headRole)
      self.SetStringItem(idx,4,tailRole)
      self.SetStringItem(idx,5,tailNry)
      self.SetStringItem(idx,6,tailAdornment)
      self.SetStringItem(idx,7,str(tailNav))
      self.SetStringItem(idx,8,tailAsset)

  def dimensions(self):
    assets = []
    for x in range(self.GetItemCount()):
      headNav = int(self.GetItemText(x))
      headAdornment = self.GetItem(x,1)
      headNry = self.GetItem(x,2)
      headRole = self.GetItem(x,3)
      tailRole = self.GetItem(x,4)
      tailNry = self.GetItem(x,5)
      tailAdornment = self.GetItem(x,6)
      tailNav = self.GetItem(x,7)
      tailAsset = self.GetItem(x,8)
      assets.append((headNav,headAdornment.GetText(),headNry.GetText(),headRole.GetText(),tailRole.GetText(),tailNry.GetText(),tailAdornment.GetText(),int(tailNav.GetText()),tailAsset.GetText()))
    return assets
