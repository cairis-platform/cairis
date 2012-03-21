#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/DimensionNameDialog.py $ $Id: DimensionNameDialog.py 469 2011-05-14 22:36:20Z shaf $
import wx
import armid
import os
import ARM

class DimensionNameDialog(wx.Dialog):
  def __init__(self,parent,dimensionName,dimensions,actionVerb,dialogSize=wx.DefaultSize):
    wx.Dialog.__init__(self,parent,armid.DIMNAME_ID,actionVerb + ' ' + dimensionName,style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=dialogSize)

    mainSizer = wx.BoxSizer(wx.VERTICAL)
    if (dimensionName == 'usecase_contribution'):
      self.theDimensionName = 'usecase'
    elif (dimensionName != 'reference'):
      self.theDimensionName = dimensionName
    else:
      self.theDimensionName = 'persona'


    self.theSelectedDimensions = []
    self.theDimensions = dimensions

    self.dimList = wx.ListBox(self,armid.DIMNAME_LISTDIM_ID,choices=dimensions,style=wx.LB_MULTIPLE)
    mainSizer.Add(self.dimList,1,wx.EXPAND)
    
    buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(buttonSizer,0,wx.CENTER)
    actionButton = wx.Button(self,armid.DIMNAME_BUTTONACTION_ID,actionVerb)
    buttonSizer.Add(actionButton)
    cancelButton = wx.Button(self,wx.ID_CANCEL,"Cancel")
    buttonSizer.Add(cancelButton)
    self.SetSizer(mainSizer)

    wx.EVT_LIST_ITEM_SELECTED(self.dimList,armid.DIMNAME_LISTDIM_ID,self.onItemSelected)
    wx.EVT_LIST_ITEM_DESELECTED(self.dimList,armid.DIMNAME_LISTDIM_ID,self.onItemDeselected)
    wx.EVT_BUTTON(self,armid.DIMNAME_BUTTONACTION_ID,self.onAdd)

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


  def onItemSelected(self,evt):
    self.theSelectedDimensions = self.dimList.GetStrings()

  def onItemDeselected(self,evt):
    self.theSelectedDimensions = []

  def onAdd(self,evt):
    self.theSelectedDimensions = self.dimList.GetSelections()
    if len(self.theSelectedDimensions) == 0:
      errorString = 'No ' + self.theDimensionName + 's selected'
      errorLabel = 'Add ' + self.theDimensionName
      dlg = wx.MessageDialog(self,errorString,errorLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(armid.DIMNAME_BUTTONACTION_ID)

  def dimensionNames(self): 
    dimensionNames = []
    for selection in self.theSelectedDimensions:
      dimensionNames.append( self.dimList.GetString(selection))
    return dimensionNames

  def dimensionName(self):
    return self.dimList.GetString(self.theSelectedDimensions[0])
