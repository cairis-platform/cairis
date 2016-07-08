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
import wx.lib.imagebrowser
import wx.combo
from cairis.core.armid import *

from GoalListCtrl import GoalListCtrl
from DimensionListBox import DimensionListBox
from ThreatListBox import ThreatListBox
from VulnerabilityListBox import VulnerabilityListBox
from ResponsibilityListBox import ResponsibilityListBox
from AssociationComboBox import AssociationComboBox
from cairis.core.Borg import Borg
import cairis.core.Trace

def buildComboSizer(parent,labelTxt,widgetSize,winId,objtDictionary):
  csBox = wx.StaticBox(parent,-1,labelTxt)
  comboSizer = wx.StaticBoxSizer(csBox,wx.HORIZONTAL)
  objtList = []
  for key,objt in objtDictionary.iteritems():
    objtList.append(key)
  objtComboCtrl = wx.ComboBox(parent,winId,"",choices=objtList,size=widgetSize,style=wx.CB_READONLY)
  comboSizer.Add(objtComboCtrl,1,wx.EXPAND)
  return comboSizer

def buildComboSizerList(parent,labelTxt,widgetSize,winId,objtList):
  cslBox = wx.StaticBox(parent,-1,labelTxt)
  comboSizer = wx.StaticBoxSizer(cslBox,wx.HORIZONTAL)
  objtComboCtrl = wx.ComboBox(parent,winId,"",choices=objtList,size=widgetSize,style=wx.CB_READONLY)
  comboSizer.Add(objtComboCtrl,1,wx.EXPAND)
  return comboSizer

def buildBitmapComboSizerList(parent,labelTxt,widgetSize,winId,objtList):
  cslBox = wx.StaticBox(parent,-1,labelTxt)
  comboSizer = wx.StaticBoxSizer(cslBox,wx.HORIZONTAL)
  objtComboCtrl = AssociationComboBox(parent,winId,"",pos=wx.DefaultPosition,size=widgetSize,choices=objtList,style=wx.CB_READONLY)
  comboSizer.Add(objtComboCtrl,1,wx.EXPAND)
  return comboSizer

def buildComboLookupSizer(parent,labelTxt,widgetSize,comboId,txtId,objtList):
  comboSizer = wx.BoxSizer(wx.HORIZONTAL)
  labelWidget = wx.StaticText(parent,-1,labelTxt,size=widgetSize)
  comboSizer.Add(labelWidget)
  stringChoices = []
  for choice in objtList: stringChoices.append( str(choice) )
  objtComboCtrl = wx.ComboBox(parent,comboId,"",choices=stringChoices,size=widgetSize,style=wx.CB_READONLY)
  comboSizer.Add(objtComboCtrl,0)
  comboSizer.Add(wx.TextCtrl(parent,txtId,"",size=widgetSize,style=wx.TE_READONLY | wx.TE_MULTILINE),1,wx.EXPAND)
  return comboSizer

def buildTextSizer(parent,labelTxt,widgetSize,winId,toolTip='',isReadOnly=False):
  tBox = wx.StaticBox(parent,-1,labelTxt)
  textSizer = wx.StaticBoxSizer(tBox,wx.HORIZONTAL)
  textCtrl = 0
  if (isReadOnly):
    textCtrl = wx.TextCtrl(parent,winId,"",style=wx.TE_READONLY)
  else:
    textCtrl = wx.TextCtrl(parent,winId,"")

  if (toolTip != ''):
    textCtrl.SetToolTip(wx.ToolTip(toolTip))
  textSizer.Add(textCtrl,1,wx.EXPAND)
  return textSizer

def buildMLTextSizer(parent,labelTxt,widgetSize,winId,isReadOnly=False):
  mltBox = wx.StaticBox(parent,-1,labelTxt)
  textSizer = wx.StaticBoxSizer(mltBox,wx.HORIZONTAL)
  if (isReadOnly):
    textCtrl = wx.TextCtrl(parent,winId,"",size=widgetSize,style=wx.TE_MULTILINE | wx.TE_READONLY)
  else:
    textCtrl = wx.TextCtrl(parent,winId,"",size=widgetSize,style=wx.TE_MULTILINE)
  textSizer.Add(textCtrl,1,wx.EXPAND)
  return textSizer

def buildImageSizer(parent,labelTxt,winId):
  iBox = wx.StaticBox(parent,-1,labelTxt)
  iSizer = wx.StaticBoxSizer(iBox,wx.HORIZONTAL)
  imagePanel = wx.lib.imagebrowser.ImageView(parent,winId)
  iSizer.Add(imagePanel,1,wx.EXPAND)
  return iSizer


def buildCommitButtonSizer(parent,winId,isCreate):
  buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
  commitLabel = ''
  if (isCreate):
    commitLabel = 'Create'
  else:
    commitLabel = 'Update'
  createButton = wx.Button(parent,winId,commitLabel)
  buttonSizer.Add(createButton)
  cancelButton = wx.Button(parent,wx.ID_CANCEL,"Close")
  buttonSizer.Add(cancelButton)
  return buttonSizer

def buildRiskButtonSizer(parent,winId,mcId,isCreate):
  buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
  commitLabel = ''
  if (isCreate):
    commitLabel = 'Create'
  else:
    commitLabel = 'Update'
  createButton = wx.Button(parent,winId,commitLabel)
  buttonSizer.Add(createButton)
  mcButton = wx.Button(parent,mcId,'Create Misuse Case')
  buttonSizer.Add(mcButton)
  cancelButton = wx.Button(parent,wx.ID_CANCEL,"Close")
  buttonSizer.Add(cancelButton)
  return buttonSizer

def buildCheckSizer(parent,labelTxt,winId,isChecked):
  checkBox = wx.StaticBox(parent,-1,labelTxt)
  checkSizer = wx.StaticBoxSizer(checkBox,wx.HORIZONTAL)
  ctrl = wx.CheckBox(parent,winId,"")
  ctrl.SetValue(isChecked)
  checkSizer.Add(ctrl,1,wx.EXPAND)
  return checkSizer

def buildAddDeleteCloseButtonSizer(parent,addId,deleteId,orientation=wx.VERTICAL):
  buttonSizer = wx.BoxSizer(orientation)
  addButton = wx.Button(parent,addId,"Add")
  buttonSizer.Add(addButton)
  if (parent.__class__.__name__ == 'VulnerabilitiesDialog' or parent.__class__.__name__ == 'ThreatsDialog'):
    importButton = wx.Button(parent,CC_DIRECTORYIMPORT_ID,'Import')
    buttonSizer.Add(importButton)
  deleteButton = wx.Button(parent,deleteId,"Delete")
  buttonSizer.Add(deleteButton)
  closeButton = wx.Button(parent,wx.ID_CLOSE,"Close")
  buttonSizer.Add(closeButton)
  return buttonSizer

def buildAddDeleteButtonSizer(parent,addId,deleteId,orientation=wx.VERTICAL):
  buttonSizer = wx.BoxSizer(orientation)
  addButton = wx.Button(parent,addId,"Add")
  buttonSizer.Add(addButton)
  deleteButton = wx.Button(parent,deleteId,"Delete")
  buttonSizer.Add(deleteButton)
  return buttonSizer

def buildAddCancelButtonSizer(parent,addId,orientation=wx.HORIZONTAL):
  buttonSizer = wx.BoxSizer(orientation)
  addButton = wx.Button(parent,addId,"Add")
  buttonSizer.Add(addButton)
  cancelButton = wx.Button(parent,wx.ID_CANCEL,"Cancel")
  buttonSizer.Add(cancelButton)
  return buttonSizer

def buildDetailsConfirmCancelButtonSizer(parent,detailsId,confirmId,orientation=wx.HORIZONTAL):
  buttonSizer = wx.BoxSizer(orientation)
  detailsButton = wx.Button(parent,detailsId,"Details >>")
  buttonSizer.Add(detailsButton)
  confirmButton = wx.Button(parent,confirmId,"Confirm")
  buttonSizer.Add(confirmButton)
  cancelButton = wx.Button(parent,wx.ID_CANCEL,"Cancel")
  buttonSizer.Add(cancelButton)
  return buttonSizer

def buildDimensionListSizer(parent,winLabel,widgetSize,winId,dimTable,dbProxy,contextualise=True):
  dlBox = wx.StaticBox(parent,-1,winLabel)
  dlSizer = wx.StaticBoxSizer(dlBox,wx.HORIZONTAL)
  dimList = 0
  if (parent.__class__.__name__ == 'MisuseCasePanel'):
    if (dimTable == 'threat'):
      dimList = ThreatListBox(parent,winId,widgetSize,dimTable,dbProxy)
    elif (dimTable == 'vulnerability'):
      dimList = VulnerabilityListBox(parent,winId,widgetSize,dimTable,dbProxy)
  elif (parent.__class__.__name__ == 'RoleDialog'):
    dimList = ResponsibilityListBox(parent,winId,widgetSize,dbProxy)
  else:
    dimList = DimensionListBox(parent,winId,widgetSize,dimTable,dbProxy)
  dlSizer.Add(dimList,1,wx.EXPAND)
  return dlSizer

def buildAttackerAssetSizer(parent,atId,asId):
  aaSizer = wx.BoxSizer(wx.HORIZONTAL)
  atList = wx.ListCtrl(parent,atId,style=wx.LC_REPORT)
  atList.InsertColumn(0,'Attacker')
  atList.SetColumnWidth(0,200)
  aaSizer.Add(atList,1,wx.EXPAND)
  asList = wx.ListCtrl(parent,asId,style=wx.LC_REPORT)
  asList.InsertColumn(0,'Asset')
  asList.SetColumnWidth(0,200)
  aaSizer.Add(asList,1,wx.EXPAND)
  return aaSizer

def buildListBoxSizer(parent,winLabel,widgetSize,winId):
  lSizer = wx.BoxSizer(wx.HORIZONTAL)
  lLabel = wx.StaticText(parent,-1,winLabel)
  lSizer.Add(lLabel)
  lList = wx.ListBox(parent,winId,widgetSize)
  lSizer.Add(lList,1,wx.EXPAND)
  return lSizer


def buildRadioButtonSizer(parent,winLabel,labelSize,ctrlList):
  radioBox = wx.StaticBox(parent,-1,winLabel)
  radioSizer = wx.StaticBoxSizer(radioBox,wx.HORIZONTAL)
  for idx, ctrlTuple in enumerate(ctrlList):
    radioStyle = 0
    if (idx == 0):
      radioStyle = wx.RB_GROUP
    radio = wx.RadioButton(parent,ctrlTuple[0],ctrlTuple[1],style=radioStyle)
    radioSizer.Add(radio)
  return radioSizer
