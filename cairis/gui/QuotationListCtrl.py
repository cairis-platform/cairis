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
# coding: latin1


import wx
from cairis.core.armid import *
from cairis.core.ARM import *
from QuotationDialog import QuotationDialog
from cairis.core.Borg import Borg

__author__ = 'Shamal Faily'

class QuotationListCtrl(wx.ListCtrl):
  def __init__(self,parent,winId,boxSize=wx.DefaultSize):
    wx.ListCtrl.__init__(self,parent,winId,size=boxSize,style=wx.LC_REPORT)
    self.theQuoteIndices = {}
    self.InsertColumn(0,'Code')
    self.SetColumnWidth(0,150)
    self.InsertColumn(1,'Artifact Type')
    self.SetColumnWidth(1,150)
    self.InsertColumn(2,'Artifact')
    self.SetColumnWidth(2,150)
    self.InsertColumn(3,'Section')
    self.SetColumnWidth(3,150)
    self.InsertColumn(4,'Quote')
    self.SetColumnWidth(4,400)
    self.theDimMenu = wx.Menu()
    self.theDimMenu.Append(QUOTATIONLISTCTRL_MENUDELETE_ID,'Delete')
    self.theSelectedValue = ''
    self.theSelectedIdx = -1
    self.Bind(wx.EVT_RIGHT_DOWN,self.OnRightDown)
    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.onItemActivated)
    wx.EVT_MENU(self.theDimMenu,QUOTATIONLISTCTRL_MENUDELETE_ID,self.onDeleteQuotation)

  def OnItemSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()

  def OnItemDeselected(self,evt):
    self.theSelectedIdx = -1

  def OnRightDown(self,evt):
    self.PopupMenu(self.theDimMenu)

  def onDeleteQuotation(self,evt):
    if (self.theSelectedIdx == -1):
      errorText = 'No quote selected'
      errorLabel = 'Delete Quotation'
      dlg = wx.MessageDialog(self,errorText,errorLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
    else:
      codeName = self.GetItemText(self.theSelectedIdx)
      atItem = self.GetItem(self.theSelectedIdx,1)
      atName = atItem.GetText()
      aItem = self.GetItem(self.theSelectedIdx,2)
      aName = aItem.GetText()
      qTxtItem = self.GetItem(self.theSelectedIdx,4)
      qTxt = qTxtItem.GetText()
      startIdx,endIdx,synopsis,label = self.theQuoteIndices[(codeName,atName,aName,qTxt)]
 
      b = Borg()
      b.dbProxy.deleteQuotation(codeName,atName,aName,startIdx,endIdx)
      del self.theQuoteIndices[(codeName,atName,aName,qTxt)]
      self.DeleteItem(self.theSelectedIdx)

  def load(self,quotations):
    for code,aType,aName,sectName,qTxt,startIdx,endIdx,synopsis,label in quotations:
      idx = self.GetItemCount()
      self.InsertStringItem(idx,code)
      self.SetStringItem(idx,1,aType)
      self.SetStringItem(idx,2,aName)
      self.SetStringItem(idx,3,sectName)
      self.SetStringItem(idx,4,qTxt)
      self.theQuoteIndices[(code,aType,aName,qTxt)] = (startIdx,endIdx,synopsis,label)

  def onItemActivated(self,evt):
    x = evt.GetIndex()
    codeName = self.GetItemText(x)
    atItem = self.GetItem(x,1)
    atName = atItem.GetText()
    aItem = self.GetItem(x,2)
    aName = aItem.GetText()
    qTxtItem = self.GetItem(x,4)
    qTxt = qTxtItem.GetText()
    startIdx,endIdx,synopsis,label = self.theQuoteIndices[(codeName,atName,aName,qTxt.encode('utf-8'))]
    dlg = QuotationDialog(self)
    dlg.load(codeName,atName,aName,startIdx,endIdx,synopsis,label)
    if (dlg.ShowModal() == QUOTATION_BUTTONCOMMIT_ID):
      # update list and quotation index entry here
      pass
    dlg.Destroy()
