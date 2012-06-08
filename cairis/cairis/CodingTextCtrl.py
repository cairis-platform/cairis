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
import armid
from ARM import *
from Borg import Borg
from DimensionNameDialog import DimensionNameDialog

class CodingTextCtrl(wx.richtext.RichTextCtrl):
  def __init__(self, parent, winId):
    wx.richtext.RichTextCtrl.__init__(self,parent,winId,style=wx.TE_MULTILINE)
    self.codingMenu = wx.Menu()
    self.ocItem = self.codingMenu.Append(armid.BVNTC_TEXTOPENCODING_ID,'Open Coding')
    self.clItem = self.codingMenu.Append(armid.BVNTC_LISTALPHABET_ID,'Alphabet')
    self.dcItem = self.codingMenu.Append(armid.BVNTC_CMDUNLINKCODES_ID,'Unlink codes')

    wx.EVT_MENU(self,armid.BVNTC_TEXTOPENCODING_ID,self.onOpenCoding)
    wx.EVT_MENU(self,armid.BVNTC_LISTALPHABET_ID,self.onListAlphabet)
    self.Bind(wx.EVT_RIGHT_DOWN, self.onRightClick)
    self.Bind(wx.EVT_TEXT_URL,self.onUrl)

    self.theSelectionStart = -1
    self.theSelectionEnd = -1
    self.theSelection = ''
    self.clItem.Enable(False)
    self.dcItem.Enable(False)
    self.theCodes = {}

  def codes(self):
    return self.theCodes

  def onRightClick(self,evt):
    self.enableCodingCtrls()
    self.PopupMenu(self.codingMenu)


  def enableCodingCtrls(self):
    self.theSelection = self.GetStringSelection()
    selRange = self.GetSelectionRange()
    self.theSelectionStart = selRange.GetStart()
    self.theSelectionEnd = selRange.GetEnd()
    if (self.theSelection == ''):
      self.codingMenu.Enable(armid.BVNTC_TEXTOPENCODING_ID,False) 
      self.codingMenu.Enable(armid.BVNTC_LISTALPHABET_ID,False) 
      self.codingMenu.Enable(armid.BVNTC_CMDUNLINKCODES_ID,False) 
    else:
      self.codingMenu.Enable(armid.BVNTC_TEXTOPENCODING_ID,True) 
      self.codingMenu.Enable(armid.BVNTC_LISTALPHABET_ID,True) 
      
      if ((self.theSelectionStart,self.theSelectionEnd) in self.theCodes):
        self.codingMenu.Enable(armid.BVNTC_CMDUNLINKCODES_ID,True) 
      else:
        self.codingMenu.Enable(armid.BVNTC_CMDUNLINKCODES_ID,False) 

  def addCode(self,codeName):
    self.theSelection = self.GetStringSelection()
    selRange = self.GetSelectionRange()
    self.theSelectionStart = selRange.GetStart()
    self.theSelectionEnd = selRange.GetEnd()
    urlStyle = wx.richtext.TextAttrEx()
    urlStyle.SetTextColour(wx.LIGHT_GREY)
    urlStyle.SetFontUnderlined(True)
    codeRef = str(self.theSelectionStart) + ',' + str(self.theSelectionEnd)
    urlStyle.SetURL(codeRef)
    self.theCodes[(self.theSelectionStart,self.theSelectionEnd)] = codeName
    self.SetStyle(wx.richtext.RichTextRange(self.theSelectionStart,self.theSelectionEnd),urlStyle)

  def onListAlphabet(self,evt):
    b = Borg()
    codes = b.dbProxy.getDimensionNames('code',False)
    cDlg = DimensionNameDialog(self,'code',codes,'Select')
    if (cDlg.ShowModal() == armid.DIMNAME_BUTTONACTION_ID):
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

  def onUrl(self,evt):
    urlValue = evt.GetString()
    codeRefs = urlValue.split(',')
    codeValue = self.theCodes[(int(codeRefs[0]),int(codeRefs[1]))]
    wx.MessageBox(codeValue,"Alphabet code")

  def setCodes(self,codes):
    self.theCodes = codes
    for startIdx,endIdx in codes:
      codeName = self.theCodes[(startIdx,endIdx)] 
      urlStyle = wx.richtext.TextAttrEx()
      urlStyle.SetTextColour(wx.LIGHT_GREY)
      urlStyle.SetFontUnderlined(True)
      codeRef = str(startIdx) + ',' + str(endIdx)
      urlStyle.SetURL(codeRef)
      self.SetStyle(wx.richtext.RichTextRange(startIdx,endIdx),urlStyle)
