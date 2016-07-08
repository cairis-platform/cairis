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
from cairis.core.armid import *
import os
from cairis.core.ARM import *
from cairis.core.Borg import Borg
from cairis.core.VulnerabilityParameters import VulnerabilityParameters
from cairis.core.ThreatParameters import ThreatParameters
from DirectoryEntryDialog import DirectoryEntryDialog
from cairis.core.ObjectFactory import *

class DirectoryDialog(wx.Dialog):
  def __init__(self,parent,dimensionName):
    wx.Dialog.__init__(self,parent,DIRECTORYDIALOG_ID,'Import ' + dimensionName,style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(600,400))
    b = Borg()
    self.dbProxy = b.dbProxy
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.theSelectedIdx = -1
    self.theDimensionName = dimensionName
    self.entries = []
    self.typedEntries = []
    if (self.theDimensionName == 'vulnerability'):
      self.entries = self.dbProxy.getVulnerabilityDirectory() 
    elif (self.theDimensionName == 'threat'):
      self.entries = self.dbProxy.getThreatDirectory() 
    
    self.typeDictionary = {}
    for entry in self.entries:
      entryType = entry[3]
      if entryType not in self.typeDictionary:
        self.typeDictionary[entryType] = []
      self.typeDictionary[entryType].append(entry)
    typeBox = wx.StaticBox(parent,-1,'Type')
    comboSizer = wx.StaticBoxSizer(typeBox,wx.HORIZONTAL)
    mainSizer.Add(comboSizer,0,wx.EXPAND)
    typeNames = self.typeDictionary.keys()
    typeNames.sort()
    typeNames = [''] + typeNames
    self.typeCtrl = wx.ComboBox(self,DIRECTORYDIALOG_COMBOTYPE_ID,"",choices=typeNames,size=wx.DefaultSize,style=wx.CB_READONLY)
    comboSizer.Add(self.typeCtrl,1,wx.EXPAND)

    self.entryList = wx.ListCtrl(self,DIRECTORYDIALOG_LISTENTRIES_ID,style=wx.LC_REPORT)
    self.entryList.InsertColumn(0,'Label')
    self.entryList.InsertColumn(1,'Name')
    self.entryList.SetColumnWidth(0,200)
    self.entryList.SetColumnWidth(1,500)
    for idx,dirEntry in enumerate(self.entries):
      self.entryList.InsertStringItem(idx,dirEntry[0])
      self.entryList.SetStringItem(idx,1,dirEntry[1])
    mainSizer.Add(self.entryList,1,wx.EXPAND)
    self.typedEntries = self.entries

    buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(buttonSizer,0,wx.CENTER)
    importButton = wx.Button(self,DIRECTORYDIALOG_BUTTONIMPORT_ID,'Import')
    buttonSizer.Add(importButton)
    cancelButton = wx.Button(self,wx.ID_CANCEL,"Cancel")
    buttonSizer.Add(cancelButton)
    self.SetSizer(mainSizer)

    wx.EVT_LIST_ITEM_SELECTED(self.entryList,DIRECTORYDIALOG_LISTENTRIES_ID,self.onItemSelected)
    wx.EVT_LIST_ITEM_DESELECTED(self.entryList,DIRECTORYDIALOG_LISTENTRIES_ID,self.onItemDeselected)
    wx.EVT_LIST_ITEM_ACTIVATED(self.entryList,DIRECTORYDIALOG_LISTENTRIES_ID,self.onItemActivated)
    wx.EVT_COMBOBOX(self.typeCtrl,DIRECTORYDIALOG_COMBOTYPE_ID,self.onTypeSelected)
    wx.EVT_BUTTON(self,DIRECTORYDIALOG_BUTTONIMPORT_ID,self.onImport)

    dimIconFile = dimensionName + '.png'
    dimIcon = wx.Icon(b.imageDir + '/' + dimIconFile,wx.BITMAP_TYPE_PNG)
    self.SetIcon(dimIcon)


  def onItemSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()

  def onItemDeselected(self,evt):
    self.theSelectedIdx = evt.GetIndex()

  def onImport(self,evt):
    if (self.theSelectedIdx == -1):
      errorString = 'No ' + self.theDimensionName + 's selected'
      errorLabel = 'Add ' + self.theDimensionName
      dlg = wx.MessageDialog(self,errorString,errorLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(DIRECTORYDIALOG_BUTTONIMPORT_ID)

  def object(self): 
    row = self.typedEntries[self.theSelectedIdx]
    p = None
    if (self.theDimensionName == 'vulnerability'):
      vulName = row[0]
      vulDesc = row[1] + '\n\n' + row[2]
      vulType = row[3]
      p = VulnerabilityParameters(vulName,vulDesc,vulType,[])
    else:
      thrName = row[0]
      thrMethod = row[1] + '\n\n' + row[2]
      thrType = row[3]
      p = ThreatParameters(thrName,thrType,thrMethod,[])
    return cairis.core.ObjectFactory.build(-1,p)

  def onItemActivated(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    row = self.typedEntries[self.theSelectedIdx]
    dLabel = row[0]
    dName = row[1]
    dType = row[3]
    dDesc = row[2]
    dlg = DirectoryEntryDialog(self,dLabel,dName,dType,dDesc)
    dlg.ShowModal()
    dlg.Destroy()

  def onTypeSelected(self,evt):
    typeName = evt.GetString()
    self.entryList.DeleteAllItems()
    if (typeName == ''):
      self.typedEntries = self.entries
    else:
      self.typedEntries = self.typeDictionary[typeName]
    for idx,dirEntry in enumerate(self.typedEntries):
      self.entryList.InsertStringItem(idx,dirEntry[0])
      self.entryList.SetStringItem(idx,1,dirEntry[1])
