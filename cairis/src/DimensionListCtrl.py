#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/DimensionListCtrl.py $ $Id: DimensionListCtrl.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid

class DimensionListCtrl(wx.ListCtrl):
  def __init__(self,parent,winId,boxSize,columnLabel,dimensionTable,dp,toolTipTxt='',listStyle=wx.LC_REPORT):
    wx.ListCtrl.__init__(self,parent,winId,size=boxSize,style=listStyle)
    self.dbProxy = dp
    self.theDimensionTable = dimensionTable
    self.theCurrentEnvironment = ''
    self.InsertColumn(0,columnLabel)
    self.SetColumnWidth(0,150)
    self.theDimMenu = wx.Menu()
    self.theDimMenu.Append(armid.DIMLIST_MENUADD_ID,'Add')
    self.theDimMenu.Append(armid.DIMLIST_MENUDELETE_ID,'Delete')
    self.Bind(wx.EVT_RIGHT_DOWN,self.OnRightDown)
    wx.EVT_MENU(self.theDimMenu,armid.DIMLIST_MENUADD_ID,self.onAddDimension)
    wx.EVT_MENU(self.theDimMenu,armid.DIMLIST_MENUDELETE_ID,self.onDeleteDimension)
   
    if (toolTipTxt != ''):
      self.SetToolTip(wx.ToolTip(toolTipTxt))

  def setEnvironment(self,environmentName):
    self.theCurrentEnvironment = environmentName

  def OnRightDown(self,evt):
    self.PopupMenu(self.theDimMenu)

  def onAddDimension(self,evt):
    if (self.theDimensionTable == 'environment'):
      dimensions = self.dbProxy.getEnvironmentNames()
    else:
      dimensions = self.dbProxy.getDimensionNames(self.theDimensionTable,self.theCurrentEnvironment)
    from DimensionNameDialog import DimensionNameDialog
    dlg = DimensionNameDialog(self,self.theDimensionTable,dimensions,'Add')
    if (dlg.ShowModal() == armid.DIMNAME_BUTTONACTION_ID):
      for additionalDimension in dlg.dimensionNames():
        idx = self.GetItemCount()
        self.InsertStringItem(idx,additionalDimension)

  def onDeleteDimension(self,evt):
    idx = self.GetFocusedItem()
    if (idx == -1):
      errorText = 'No ' + self.theDimensionTable + ' selected'
      errorLabel = 'Delete ' + self.theDimensionTable
      dlg = wx.MessageDialog(self,errorText,errorLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
    else:
      self.DeleteItem(idx)


  def load(self,dims):
    self.DeleteAllItems()
    if len(dims) > 0:
      dims.sort()
      for idx,dim in enumerate(dims):
        self.InsertStringItem(idx,str(dim))

  def dimensions(self):
    dimList = []
    for x in range(self.GetItemCount()):
      dimList.append(self.GetItemText(x))
    return dimList
