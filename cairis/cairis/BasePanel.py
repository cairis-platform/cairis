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
from TagCtrl import TagCtrl

class BasePanel(wx.Panel):
  def init(self,parent,winId):
    wx.Panel.__init__(self,parent,winId)

  def buildTextSizer(self,labelTxt,widgetSize,winId,toolTip='',isReadOnly=False):
    tBox = wx.StaticBox(self,-1,labelTxt)
    textSizer = wx.StaticBoxSizer(tBox,wx.HORIZONTAL)
    textCtrl = 0
    if (isReadOnly):
      textCtrl = wx.TextCtrl(self,winId,"",style=wx.TE_READONLY)
    else:
      textCtrl = wx.TextCtrl(self,winId,"")

    if (toolTip != ''):
      textCtrl.SetToolTip(wx.ToolTip(toolTip))
    textSizer.Add(textCtrl,1,wx.EXPAND)
    return textSizer

  def buildTagCtrlSizer(self,widgetSize,winId):
    tBox = wx.StaticBox(self,-1,'Tags')
    tagSizer = wx.StaticBoxSizer(tBox,wx.HORIZONTAL)
    tagCtrl = TagCtrl(self,winId)
    tagSizer.Add(tagCtrl,1,wx.EXPAND)
    return tagSizer

  def buildComboSizer(self,labelTxt,widgetSize,winId,objtDictionary):
    csBox = wx.StaticBox(self,-1,labelTxt)
    comboSizer = wx.StaticBoxSizer(csBox,wx.HORIZONTAL)
    objtList = []
    for key,objt in objtDictionary.iteritems():
      objtList.append(key)
    objtComboCtrl = wx.ComboBox(self,winId,"",choices=objtList,size=widgetSize,style=wx.CB_READONLY)
    comboSizer.Add(objtComboCtrl,1,wx.EXPAND)
    return comboSizer

  def buildComboSizerList(self,labelTxt,widgetSize,winId,objtList):
    cslBox = wx.StaticBox(self,-1,labelTxt)
    comboSizer = wx.StaticBoxSizer(cslBox,wx.HORIZONTAL)
    objtComboCtrl = wx.ComboBox(self,winId,"",choices=objtList,size=widgetSize,style=wx.CB_READONLY)
    comboSizer.Add(objtComboCtrl,1,wx.EXPAND)
    return comboSizer

  def buildCommitButtonSizer(self,winId,isCreate):
    buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
    commitLabel = ''
    if (isCreate):
      commitLabel = 'Create'
    else:
      commitLabel = 'Update'
    createButton = wx.Button(self,winId,commitLabel)
    buttonSizer.Add(createButton)
    cancelButton = wx.Button(self,wx.ID_CANCEL,"Close")
    buttonSizer.Add(cancelButton)
    return buttonSizer

  def buildAddDeleteCloseButtonSizer(self,addId,deleteId,orientation=wx.VERTICAL):
    buttonSizer = wx.BoxSizer(orientation)
    addButton = wx.Button(self,addId,"Add")
    buttonSizer.Add(addButton)
    deleteButton = wx.Button(self,deleteId,"Delete")
    buttonSizer.Add(deleteButton)
    closeButton = wx.Button(self,wx.ID_CLOSE,"Close")
    buttonSizer.Add(closeButton)
    return buttonSizer

  def buildTraceListCtrl(self,winId,columnNames,traces):
    listCtrl = wx.ListCtrl(self,winId,style=wx.LC_REPORT)
    for idx,columnName in enumerate(columnNames):
      listCtrl.InsertColumn(idx,columnName)

    b = Borg()
    dbProxy = b.dbProxy
    listRow  = 0
    for idx, objt in enumerate(traces):
      listCtrl.InsertStringItem(objt.fromObject())
      listCtrl.SetColumnWidth(0,75)
      listCtrl.SetStringItem(listRow,1,objt.fromName())
      listCtrl.SetColumnWidth(1,250)
      listCtrl.SetStringItem(objt.toObject())
      listCtrl.SetColumnWidth(2,75)
      listCtrl.SetStringItem(listRow,3,objt.toName())
      listCtrl.SetColumnWidth(3,125)
      listRow += 1
    return listCtrl

  def buildMLTextSizer(self,labelTxt,widgetSize,winId,isReadOnly=False):
    mltBox = wx.StaticBox(self,-1,labelTxt)
    textSizer = wx.StaticBoxSizer(mltBox,wx.HORIZONTAL)
    if (isReadOnly):
      textCtrl = wx.TextCtrl(self,winId,"",size=widgetSize,style=wx.TE_MULTILINE | wx.TE_READONLY)
    else:
      textCtrl = wx.TextCtrl(self,winId,"",size=widgetSize,style=wx.TE_MULTILINE)
    textSizer.Add(textCtrl,1,wx.EXPAND)
    return textSizer

  def buildCheckSizer(self,labelTxt,winId,isChecked):
    checkBox = wx.StaticBox(self,-1,labelTxt)
    checkSizer = wx.StaticBoxSizer(checkBox,wx.HORIZONTAL)
    ctrl = wx.CheckBox(self,winId,"")
    ctrl.SetValue(isChecked)
    checkSizer.Add(ctrl,1,wx.EXPAND)
    return checkSizer

  def buildRiskButtonSizer(self,winId,mcId,isCreate):
    buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
    commitLabel = ''
    if (isCreate):
      commitLabel = 'Create'
    else:
      commitLabel = 'Update'
    createButton = wx.Button(self,winId,commitLabel)
    buttonSizer.Add(createButton)
    mcButton = wx.Button(self,mcId,'Create Misuse Case')
    buttonSizer.Add(mcButton)
    cancelButton = wx.Button(self,wx.ID_CANCEL,"Close")
    buttonSizer.Add(cancelButton)
    return buttonSizer

