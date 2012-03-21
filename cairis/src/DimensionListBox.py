#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/DimensionListBox.py $ $Id: DimensionListBox.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
import ARM

class DimensionListBox(wx.ListBox):
  def __init__(self,parent,winId,boxSize,dimensionTable,dp):
    wx.ListBox.__init__(self,parent,winId,size=boxSize)
    self.dbProxy = dp
    self.theDimensionTable = dimensionTable
    self.theDimMenu = wx.Menu()
    self.theDimMenu.Append(armid.DIMLIST_MENUADD_ID,'Add')
    self.theDimMenu.Append(armid.DIMLIST_MENUDELETE_ID,'Delete')
    self.Bind(wx.EVT_RIGHT_DOWN,self.OnRightDown)
    wx.EVT_MENU(self.theDimMenu,armid.DIMLIST_MENUADD_ID,self.onAddDimension)
    wx.EVT_MENU(self.theDimMenu,armid.DIMLIST_MENUDELETE_ID,self.onDeleteDimension)

  def OnRightDown(self,evt):
    self.PopupMenu(self.theDimMenu)

  def onAddDimension(self,evt):
    dimensions = self.dbProxy.getDimensionNames(self.theDimensionTable)
    from DimensionNameDialog import DimensionNameDialog
    dlg = DimensionNameDialog(self,self.theDimensionTable,dimensions,'Add')
    if (dlg.ShowModal() == armid.DIMNAME_BUTTONACTION_ID):
      for additionalDimension in dlg.dimensionNames():
        self.Append(additionalDimension)

  def onDeleteDimension(self,evt):
    idx = self.GetSelection()
    if (idx == -1):
      errorText = 'No ' + self.theDimensionTable + ' selected'
      errorLabel = 'Delete ' + self.theDimensionTable
      dlg = wx.MessageDialog(self,errorText,errorLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
    else:
      selectedValue = self.GetSelection()
      self.Delete(selectedValue)
