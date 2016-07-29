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
from cairis.core.ARM import *
from QuotationPanel import QuotationPanel
from cairis.core.Borg import Borg

__author__ = 'Shamal Faily'

class QuotationDialog(wx.Dialog):
  def __init__(self,parent):
    wx.Dialog.__init__(self,parent,-1,'Edit Quotation',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,500))
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theOldStartIdx = -1 
    self.theOldEndIdx = -1 
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = QuotationPanel(self)
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,QUOTATION_BUTTONCOMMIT_ID,self.onCommit)

  def load(self,codeName,atName,aName,startIdx,endIdx,synopsis,label):
    self.theOldStartIdx = startIdx
    self.theOldEndIdx = endIdx
    codeCtrl = self.FindWindowById(QUOTATION_TEXTCODE_ID)
    atCtrl = self.FindWindowById(QUOTATION_TEXTARTIFACTTYPE_ID)
    anCtrl = self.FindWindowById(QUOTATION_TEXTARTIFACTNAME_ID)
    srcCtrl = self.FindWindowById(QUOTATION_TEXTSOURCE_ID)
    synCtrl = self.FindWindowById(QUOTATION_TEXTSYNOPSIS_ID)
    lblCtrl = self.FindWindowById(QUOTATION_TEXTLABEL_ID)

    codeCtrl.SetValue(codeName)
    atCtrl.SetValue(atName)
    anCtrl.SetValue(aName)
    srcTxt = self.dbProxy.artifactText(atName,aName)
    srcCtrl.SetValue(srcTxt)
    srcCtrl.SetSelection(startIdx,endIdx)
    synCtrl.SetValue(synopsis)
    lblCtrl.SetValue(label)

  def onCommit(self,evt):
    commitLabel = 'Update quotation'

    codeCtrl = self.FindWindowById(QUOTATION_TEXTCODE_ID)
    atCtrl = self.FindWindowById(QUOTATION_TEXTARTIFACTTYPE_ID)
    anCtrl = self.FindWindowById(QUOTATION_TEXTARTIFACTNAME_ID)
    srcCtrl = self.FindWindowById(QUOTATION_TEXTSOURCE_ID)
    synCtrl = self.FindWindowById(QUOTATION_TEXTSYNOPSIS_ID)
    lblCtrl = self.FindWindowById(QUOTATION_TEXTLABEL_ID)

    codeName = codeCtrl.GetValue()
    atName = atCtrl.GetValue()
    aName = anCtrl.GetValue()
    synopsis = synCtrl.GetValue()
    label = lblCtrl.GetValue()
    
    startIdx,endIdx = srcCtrl.GetSelection()
    if (startIdx == endIdx):
      dlg = wx.MessageDialog(self,'Selection must be made',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif startIdx == self.theOldStartIdx and endIdx == self.theOldEndIdx:
      self.EndModal(wx.ID_CLOSE)
    b = Borg()
    b.dbProxy.updateQuotation(codeName,atName,aName,self.theOldStartIdx,self.theOldEndIdx,startIdx,endIdx,synopsis,label)
    self.EndModal(QUOTATION_BUTTONCOMMIT_ID)
