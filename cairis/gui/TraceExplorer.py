#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.


from cairis.core.armid import *
import wx
from cairis.core.Borg import Borg
from cairis.core.VulnerabilityParameters import VulnerabilityParameters

#import DimensionPanelFactory

class TraceExplorer(wx.Dialog):
  def __init__(self,parent,traceDimension,isFrom,envName=''):
    wx.Dialog.__init__(self,parent,TRACE_ID,'Contributions',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(800,300))
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
    self.dimensionList = wx.ListBox(self,TRACE_LISTDIM_ID,choices=dimensions,style=wx.LB_SINGLE)
    dimensionSizer.Add(self.dimensionList,1,wx.EXPAND)

    valueSizer = wx.BoxSizer(wx.VERTICAL)
    frameSizer.Add(valueSizer,1,wx.EXPAND)
    valueLabel = wx.StaticText(self,-1,'Value:')
    valueSizer.Add(valueLabel)
    self.valueList = wx.ListBox(self,TRACE_LISTVALUES_ID,style=wx.LB_SINGLE)
    valueSizer.Add(self.valueList,1,wx.EXPAND)
    
    labelBox = wx.StaticBox(self,-1,'Label')
    labelBoxSizer = wx.StaticBoxSizer(labelBox,wx.HORIZONTAL)
    mainSizer.Add(labelBoxSizer,0,wx.EXPAND)
    self.labelCtrl = wx.TextCtrl(self,TRACE_TEXTLABEL_ID,'')
    labelBoxSizer.Add(self.labelCtrl,1,wx.EXPAND)
    self.labelCtrl.Disable()

    buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(buttonSizer,0,wx.ALIGN_CENTER)
    addButton = wx.Button(self,TRACE_BUTTONADD_ID,"Add")
    buttonSizer.Add(addButton)
    cancelButton = wx.Button(self,wx.ID_CANCEL,"Cancel")
    buttonSizer.Add(cancelButton)
    self.SetSizer(mainSizer)

    wx.EVT_LISTBOX(self.dimensionList,TRACE_LISTDIM_ID,self.onDimItemSelected)
    wx.EVT_LISTBOX(self.valueList,TRACE_LISTVALUES_ID,self.onValueItemSelected)
    wx.EVT_BUTTON(self,TRACE_BUTTONADD_ID,self.onAdd)
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
      self.EndModal(TRACE_BUTTONADD_ID)

  def onClose(self,evt):
    idx = self.dimensionList.GetSelection()
    self.dimensionList.Deselect(idx)
    self.EndModal(wx.ID_CLOSE)
