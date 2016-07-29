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
import wx.richtext
from cairis.core.armid import *
from cairis.core.ARM import *
from cairis.core.Borg import Borg
from DimensionNameDialog import DimensionNameDialog
from CodeDialog import CodeDialog
from MemoDialog import MemoDialog
from cairis.core.MemoParameters import MemoParameters
from DialogClassParameters import DialogClassParameters

__author__ = 'Shamal Faily'

class CodingTextCtrl(wx.richtext.RichTextCtrl):
  def __init__(self, parent, winId):
    wx.richtext.RichTextCtrl.__init__(self,parent,winId,style=wx.TE_MULTILINE)
    self.codingMenu = wx.Menu()
    self.ocItem = self.codingMenu.Append(BVNTC_TEXTOPENCODING_ID,'Open Coding')
    self.clItem = self.codingMenu.Append(BVNTC_LISTALPHABET_ID,'Alphabet')
    self.dcItem = self.codingMenu.Append(BVNTC_CMDUNLINKCODES_ID,'Unlink codes')
    self.meItem = self.codingMenu.Append(BVNTC_CMDMEMO_ID,'Memo')

    wx.EVT_MENU(self,BVNTC_TEXTOPENCODING_ID,self.onOpenCoding)
    wx.EVT_MENU(self,BVNTC_LISTALPHABET_ID,self.onListAlphabet)
    wx.EVT_MENU(self,BVNTC_CMDMEMO_ID,self.onMemo)
    self.Bind(wx.EVT_RIGHT_DOWN, self.onRightClick)
    self.Bind(wx.EVT_TEXT_URL,self.onUrl)

    self.theSelectionStart = -1
    self.theSelectionEnd = -1
    self.theSelection = ''
    self.clItem.Enable(False)
    self.dcItem.Enable(False)
    self.theCodes = {}
    self.theMemos = {}

  def codes(self):
    return self.theCodes

  def memos(self):
    return self.theMemos

  def onRightClick(self,evt):
    self.enableCodingCtrls()
    self.PopupMenu(self.codingMenu)


  def enableCodingCtrls(self):
    self.theSelection = self.GetStringSelection()
    selRange = self.GetSelectionRange()
    self.theSelectionStart = selRange.GetStart()
    self.theSelectionEnd = selRange.GetEnd()
    if (self.theSelection == ''):
      self.codingMenu.Enable(BVNTC_TEXTOPENCODING_ID,False) 
      self.codingMenu.Enable(BVNTC_LISTALPHABET_ID,False) 
      self.codingMenu.Enable(BVNTC_CMDUNLINKCODES_ID,False) 
    else:
      self.codingMenu.Enable(BVNTC_TEXTOPENCODING_ID,True) 
      self.codingMenu.Enable(BVNTC_LISTALPHABET_ID,True) 
      
      if ((self.theSelectionStart,self.theSelectionEnd) in self.theCodes):
        self.codingMenu.Enable(BVNTC_CMDUNLINKCODES_ID,True) 
      else:
        self.codingMenu.Enable(BVNTC_CMDUNLINKCODES_ID,False) 

  def getTextSelection(self):
    self.theSelection = self.GetStringSelection()
    selRange = self.GetSelectionRange()
    self.theSelectionStart = selRange.GetStart()
    self.theSelectionEnd = selRange.GetEnd()

  def addCode(self,codeName):
    self.getTextSelection()
    urlStyle = wx.richtext.TextAttrEx()
    urlStyle.SetTextColour(wx.BLUE)
    urlStyle.SetFontUnderlined(True)
    codeRef = str(self.theSelectionStart) + ',' + str(self.theSelectionEnd) + ',code'
    urlStyle.SetURL(codeRef)
    self.theCodes[(self.theSelectionStart,self.theSelectionEnd)] = codeName
    self.SetStyle(wx.richtext.RichTextRange(self.theSelectionStart,self.theSelectionEnd),urlStyle)

  def addMemo(self,memoName,memoTxt):
    self.getTextSelection()
    urlStyle = wx.richtext.TextAttrEx()
    urlStyle.SetTextColour(wx.LIGHT_GREY)
    urlStyle.SetFontUnderlined(True)
    memoRef = str(self.theSelectionStart) + ',' + str(self.theSelectionEnd) + ',memo'
    urlStyle.SetURL(memoRef)
    self.theMemos[(self.theSelectionStart,self.theSelectionEnd)] = (memoName,memoTxt)
    self.SetStyle(wx.richtext.RichTextRange(self.theSelectionStart,self.theSelectionEnd),urlStyle)

  def onListAlphabet(self,evt):
    b = Borg()
    codes = b.dbProxy.getDimensionNames('code',False)
    cDlg = DimensionNameDialog(self,'code',codes,'Select')
    if (cDlg.ShowModal() == DIMNAME_BUTTONACTION_ID):
      codeName = cDlg.dimensionName()
      self.addCode(codeName)
    cDlg.Destroy()

  def onOpenCoding(self,evt):
    dlg = wx.TextEntryDialog(self,'Enter alphabet code','Alphabet code')
    if (dlg.ShowModal() == wx.ID_OK):
      codeName = dlg.GetValue()
      if codeName != '':
        self.addCode(codeName)
    dlg.Destroy()

  def onMemo(self,evt):
    dlg = MemoDialog(self,DialogClassParameters(MEMO_ID,'Add/Edit Memo'))
    if (dlg.ShowModal() == MEMO_BUTTONCOMMIT_ID):
      memoName = dlg.name()
      memoTxt = dlg.memo()
      self.addMemo(memoName,memoTxt)
    dlg.Destroy()

  def onUrl(self,evt):
    urlValue = evt.GetString()
    refs = urlValue.split(',')
    isCode = True
    cmValue = None
    fromIdx = int(refs[0])
    toIdx = int(refs[1])
    self.displayCode(fromIdx,toIdx)
    self.displayMemo(fromIdx,toIdx)

  def displayCode(self,fromIdx,toIdx):
    try:
      cmValue = self.theCodes[(fromIdx,toIdx)]
      b = Borg() 
      cmObjt = b.dbProxy.dimensionObject(cmValue,'code') 
      dlg = CodeDialog(self,DialogClassParameters(CODE_ID,'View Code'))
      dlg.load(cmObjt)
      dlg.ShowModal()
    except KeyError:
      return

  def displayMemo(self,fromIdx,toIdx):
    try:
      cmValue = self.theMemos[(fromIdx,toIdx)]
      b = Borg() 
      cmObjt = b.dbProxy.dimensionObject(cmValue[0],'memo') 
      dlg = MemoDialog(self,DialogClassParameters(MEMO_ID,'View Memo'))
      dlg.load(cmObjt)
      if (dlg.ShowModal() == MEMO_BUTTONCOMMIT_ID):
        memoName = dlg.name()
        memoTxt = dlg.memo()
        self.theMemos[(fromIdx,toIdx)] = (memoName,memoTxt)
        b = Borg()
        p = MemoParameters(memoName,memoTxt)
        p.setId(cmObjt.id())
        b.dbProxy.updateMemo(p)
      dlg.Destroy()
    except KeyError:
      return


  def setCodes(self,codes):
    self.theCodes = codes
    for startIdx,endIdx in codes:
      codeName = self.theCodes[(startIdx,endIdx)] 
      urlStyle = wx.richtext.TextAttrEx()
      urlStyle.SetTextColour(wx.BLUE)
      urlStyle.SetFontUnderlined(True)
      codeRef = str(startIdx) + ',' + str(endIdx)
      urlStyle.SetURL(codeRef)
      codeRange = wx.richtext.RichTextRange(startIdx,endIdx)
      self.SetStyle(codeRange,urlStyle)

  def setMemos(self,memos):
    self.theMemos = memos
    for startIdx,endIdx in memos:
      memoName,memoTxt = self.theMemos[(startIdx,endIdx)] 
      urlStyle = wx.richtext.TextAttrEx()
      urlStyle.SetTextColour(wx.LIGHT_GREY)
      urlStyle.SetFontUnderlined(True)
      codeRef = str(startIdx) + ',' + str(endIdx)
      urlStyle.SetURL(codeRef)
      codeRange = wx.richtext.RichTextRange(startIdx,endIdx)
      self.SetStyle(codeRange,urlStyle)
