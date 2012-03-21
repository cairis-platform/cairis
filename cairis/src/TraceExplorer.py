#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/TraceExplorer.py $ $Id: TraceExplorer.py 567 2012-03-13 22:31:40Z shaf $
import armid
import wx
from Borg import Borg
from VulnerabilityParameters import VulnerabilityParameters

#import DimensionPanelFactory

class TraceExplorer(wx.Dialog):
  def __init__(self,parent,traceDimension,isFrom,envName=''):
    wx.Dialog.__init__(self,parent,armid.TRACE_ID,'Contributions',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(800,300))
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theTraceDimension = traceDimension
    self.isFromIndicator = isFrom
    self.theSelectedValue = ''
    self.theToDimension = ''
    self.theLabel = ''
    self.theEnvironmentName = envName

    mainSizer = wx.BoxSizer(wx.VERTICAL)
    frameSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(frameSizer,1,wx.EXPAND)

    dimensionSizer = wx.BoxSizer(wx.VERTICAL)
    frameSizer.Add(dimensionSizer,0,wx.EXPAND)
    dimensionLabel = wx.StaticText(self,-1,'Dimension:')
    dimensionSizer.Add(dimensionLabel)
    dimensions = self.dbProxy.getTraceDimensions(self.theTraceDimension,self.isFromIndicator)
    self.dimensionList = wx.ListBox(self,armid.TRACE_LISTDIM_ID,choices=dimensions,style=wx.LB_SINGLE)
    dimensionSizer.Add(self.dimensionList,1,wx.EXPAND)

    valueSizer = wx.BoxSizer(wx.VERTICAL)
    frameSizer.Add(valueSizer,1,wx.EXPAND)
    valueLabel = wx.StaticText(self,-1,'Value:')
    valueSizer.Add(valueLabel)
    self.valueList = wx.ListBox(self,armid.TRACE_LISTVALUES_ID,style=wx.LB_SINGLE)
    valueSizer.Add(self.valueList,1,wx.EXPAND)
    
    labelBox = wx.StaticBox(self,-1,'Label')
    labelBoxSizer = wx.StaticBoxSizer(labelBox,wx.HORIZONTAL)
    mainSizer.Add(labelBoxSizer,0,wx.EXPAND)
    self.labelCtrl = wx.TextCtrl(self,armid.TRACE_TEXTLABEL_ID,'')
    labelBoxSizer.Add(self.labelCtrl,1,wx.EXPAND)
    self.labelCtrl.Disable()

    buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(buttonSizer,0,wx.ALIGN_CENTER)
    addButton = wx.Button(self,armid.TRACE_BUTTONADD_ID,"Add")
    buttonSizer.Add(addButton)
    cancelButton = wx.Button(self,wx.ID_CANCEL,"Cancel")
    buttonSizer.Add(cancelButton)
    self.SetSizer(mainSizer)

    wx.EVT_LISTBOX(self.dimensionList,armid.TRACE_LISTDIM_ID,self.onDimItemSelected)
    wx.EVT_LISTBOX(self.valueList,armid.TRACE_LISTVALUES_ID,self.onValueItemSelected)
    wx.EVT_BUTTON(self,armid.TRACE_BUTTONADD_ID,self.onAdd)
    wx.EVT_BUTTON(self,wx.ID_CANCEL,self.onClose)

  def onDimItemSelected(self,evt):
    valueIdx = self.valueList.GetSelection()
    self.valueList.Deselect(valueIdx)
    self.theToDimension = self.dimensionList.GetStringSelection()
    if (self.theToDimension == 'requirement'):
      self.labelCtrl.Enable()
    else:
      self.labelCtrl.Disable()

    if (self.theToDimension):
      dimensionValues = self.dbProxy.getDimensionNames(self.theToDimension,self.theEnvironmentName)
      self.valueList.Set(dimensionValues)

  def onValueItemSelected(self,evt):
    self.theSelectedValue = self.valueList.GetStringSelection()

  def toDimension(self): return self.theToDimension
  def fromDimension(self): 
    if (self.isFromIndicator == True): 
      return self.toDimension()

  def toValue(self): return self.theSelectedValue

  def label(self): return self.labelCtrl.GetValue()

  def toId(self):
    return self.dbProxy.getDimensionId(self.theSelectedValue,self.theToDimension)
    
  
  def onAdd(self,evt):
    if len(self.theToDimension) == 0:
      dlg = wx.MessageDialog(self,'No target dimension has been selected','Add trace',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theSelectedValue) == 0):
      dlg = wx.MessageDialog(self,'No dimension value has been selected','Add trace',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      idx = self.dimensionList.GetSelection()
      self.dimensionList.Deselect(idx)
      idx = self.valueList.GetSelection()
      self.valueList.Deselect(idx)
      self.EndModal(armid.TRACE_BUTTONADD_ID)

  def onClose(self,evt):
    idx = self.dimensionList.GetSelection()
    self.dimensionList.Deselect(idx)
    self.EndModal(wx.ID_CLOSE)
