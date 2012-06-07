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

    self.theSelectionStart = -1
    self.theSelectionEnd = -1
    self.theSelection = ''
    self.clItem.Enable(False)
    self.dcItem.Enable(False)
    self.theCodes = {}

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

  def onOpenCoding(self,evt):
    dlg = wx.TextEntryDialog(self,'Enter alphabet code','Alphabet code')
    if (dlg.ShowModal() == wx.ID_OK):
      codeName = dlg.GetValue()
      if codeName != '':
        urlStyle = wx.richtext.TextAttrEx()
        urlStyle.SetTextColour(wx.LIGHT_GREY)
        urlStyle.SetFontUnderlined(True)
        codeRef = str(self.theSelectionStart) + ',' + str(self.theSelectionEnd)
        urlStyle.SetURL(codeRef)
        self.Bind(wx.EVT_TEXT_URL,self.onUrl)
        self.theCodes[(self.theSelectionStart,self.theSelectionEnd)] = codeName
        self.SetStyle(wx.richtext.RichTextRange(self.theSelectionStart,self.theSelectionEnd),urlStyle)
    dlg.Destroy()

  def onListAlphabet(self,evt):
    pass

  def onUrl(self,evt):
    urlValue = evt.GetString()
    codeRefs = urlValue.split(',')
    codeValue = self.theCodes[(int(codeRefs[0]),int(codeRefs[1]))]
    wx.MessageBox(codeValue,"Alphabet code")
