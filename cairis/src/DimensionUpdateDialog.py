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


import wx
import armid
import os
import ARM
from DimensionNameDialog import DimensionNameDialog
from Borg import *

class DimensionUpdateDialog(wx.Dialog):
  def __init__(self,parent,dp,currentDims,dimensionName):
    wx.Dialog.__init__(self,parent,armid.DIMUPDATE_ID,'Edit ' + dimensionName,style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(300,200))
    self.dbProxy = dp
    b = Borg()
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
    dimIconFile = self.theDimensionName + '.png'
    dimIcon = wx.Icon(b.imageDir + '/' + dimIconFile,wx.BITMAP_TYPE_PNG)
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
  
