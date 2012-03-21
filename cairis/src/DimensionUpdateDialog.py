#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/DimensionUpdateDialog.py $ $Id: DimensionUpdateDialog.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
import os
import ARM
from DimensionNameDialog import DimensionNameDialog

class DimensionUpdateDialog(wx.Dialog):
  def __init__(self,parent,dp,currentDims,dimensionName):
    wx.Dialog.__init__(self,parent,armid.DIMUPDATE_ID,'Edit ' + dimensionName,style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(300,200))
    self.dbProxy = dp
    self.theDimensionName = dimensionName
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    dimSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(dimSizer,1,wx.EXPAND)

    self.dimList = wx.ListBox(self,armid.DIMUPDATE_LISTDIM_ID,choices=currentDims,style=wx.LB_SINGLE)
    dimSizer.Add(self.dimList,1,wx.EXPAND)

    buttonSizer = wx.BoxSizer(wx.VERTICAL)
    addButton = wx.Button(self,armid.DIMUPDATE_BUTTONADD_ID,"Add")
    buttonSizer.Add(addButton)
    deleteButton = wx.Button(self,armid.DIMUPDATE_BUTTONDELETE_ID,"Delete")
    buttonSizer.Add(deleteButton)
    dimSizer.Add(buttonSizer,0,wx.EXPAND)

    buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(buttonSizer)
    actionButton = wx.Button(self,armid.DIMUPDATE_BUTTONUPDATE_ID,'Update')
    buttonSizer.Add(actionButton)
    closeButton = wx.Button(self,wx.ID_CLOSE,"Close")
    buttonSizer.Add(closeButton)
    self.SetSizer(mainSizer)

    wx.EVT_BUTTON(self,armid.DIMUPDATE_BUTTONADD_ID,self.onAdd)
    wx.EVT_BUTTON(self,armid.DIMUPDATE_BUTTONDELETE_ID,self.onDelete)
    wx.EVT_BUTTON(self,armid.DIMUPDATE_BUTTONUPDATE_ID,self.onUpdate)
    wx.EVT_BUTTON(self,wx.ID_CLOSE,self.onClose)

    directoryPrefix = ''
    if (os.name == 'nt'):
      directoryPrefix += 'C:\\iris\\'
    elif (os.uname()[0] == 'Linux'):
      directoryPrefix += os.environ['IRIS_IMAGES'] + '/'
    elif (os.uname()[0] == 'Darwin'):
      directoryPrefix += os.environ['IRIS_IMAGES'] + '/'
    else:
      raise ARM.UnsupportedOperatingSystem(os.name)
    dimIconFile = self.theDimensionName + '.png'
    dimIcon = wx.Icon(directoryPrefix + dimIconFile,wx.BITMAP_TYPE_PNG)
    self.SetIcon(dimIcon)


  def onAdd(self,evt):
    dims = self.dbProxy.getDimensionNames(self.theDimensionName,False)
    dlg = DimensionNameDialog(self,self.theDimensionName,dims,'Select',(300,200))
    if (dlg.ShowModal() == armid.DIMNAME_BUTTONACTION_ID):
      self.dimList.Append(dlg.dimensionName())

  def onDelete(self,evt):
    idx = self.dimList.GetSelection()
    if (idx == wx.NOT_FOUND):
      errorString = self.theDimensionName + ' has not been selected'
      errorLabel = 'Edit ' + self.theDimensionName
      dlg = wx.MessageDialog(self,errorString,errorLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.dimList.Delete(idx)

  def onUpdate(self,evt):
    if (self.dimList.GetCount() == 0):
      errorString = 'Need to include at least one ' + self.theDimensionName
      errorLabel = 'Edit ' + self.theDimensionName
      dlg = wx.MessageDialog(self,errorString,errorLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
    else:
      self.EndModal(wx.ID_OK)

  def onClose(self,evt):
    self.EndModal(wx.ID_CLOSE)

  def selection(self):
    selections = []
    for x in range(self.dimList.GetCount()):
      selection = self.dimList.GetString(x)
      selections.append(selection)
    return selections
  
