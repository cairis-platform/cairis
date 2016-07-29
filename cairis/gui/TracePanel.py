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
import WidgetFactory
from cairis.core.Borg import Borg

__author__ = 'Shamal Faily'

class TracePanel(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,TRACE_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theFromObject = -1
    self.theFromId = -1
    self.theToObject = -1
    self.theToId = -1
    self.theFromName = ''
    self.theToName = ''
    self.theSelectedFromDimensions = []
    self.theSelectedToDimensions = []
    self.theSelectedFromDimension = ''

  def buildControls(self,isCreate,isUpdateable=True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    allDimensionNames = self.dbProxy.getDimensionNames('trace_dimension')
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'From artifact',(87,30),TRACE_COMBOFROMOBJECT_ID,allDimensionNames),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'From name',(87,30),TRACE_COMBOFROMNAME_ID,[]),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'To artifact',(87,30),TRACE_COMBOTOOBJECT_ID,allDimensionNames),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'To name',(87,30),TRACE_COMBOTONAME_ID,[]),0,wx.EXPAND)
    mainSizer.Add(wx.StaticText(self,-1,''),1,wx.EXPAND)
    if (isUpdateable):
      mainSizer.Add(WidgetFactory.buildCommitButtonSizer(self,TRACE_BUTTONCOMMIT_ID,isCreate),0,wx.ALIGN_CENTRE)
    self.SetSizer(mainSizer)

    self.fromObjectCombo = self.FindWindowById(TRACE_COMBOFROMOBJECT_ID)
    self.fromNameCombo = self.FindWindowById(TRACE_COMBOFROMNAME_ID)
    self.toObjectCombo = self.FindWindowById(TRACE_COMBOTOOBJECT_ID)
    self.toNameCombo = self.FindWindowById(TRACE_COMBOTONAME_ID)

    self.fromObjectCombo.Bind(wx.EVT_COMBOBOX,self.onFromObjectChange)
    self.fromNameCombo.Bind(wx.EVT_COMBOBOX,self.onFromNameChange)
    self.toObjectCombo.Bind(wx.EVT_COMBOBOX,self.onToObjectChange)
    self.toNameCombo.Bind(wx.EVT_COMBOBOX,self.onToNameChange)

  def loadControls(self,trace,isReadOnly = False):
    self.theFromObject = trace.fromObject()
    self.theFromId = trace.fromId()
    self.theToObject = trace.toObject()
    self.theToId = trace.toId()
    self.theFromName = trace.fromName()
    self.theToName = trace.toName()

    fdCtrl = self.FindWindowById(TRACE_COMBOFROMOBJECT_ID)
    fnCtrl = self.FindWindowById(TRACE_COMBOFROMNAME_ID)
    tdCtrl = self.FindWindowById(TRACE_COMBOTOOBJECT_ID)
    tnCtrl = self.FindWindowById(TRACE_COMBOTONAME_ID)

    self.fromObjectCombo.SetValue(self.theFromObject)
    self.fromNameCombo.SetValue(self.theFromName)
    self.toObjectCombo.SetValue(self.theToObject)
    self.toNameCombo.SetValue(self.theToName)

  def onFromObjectChange(self,evt):
    self.fromNameCombo.Clear()
    fromDimension = self.fromObjectCombo.GetStringSelection()
    self.theFromObject = self.dbProxy.getDimensionId(fromDimension,'trace_dimension')
    self.fromNameCombo.SetItems(self.dbProxy.getDimensionNames(fromDimension))
    self.fromNameCombo.SetSelection(0)
    self.theFromName = self.fromNameCombo.GetStringSelection()
    self.theFromId = self.dbProxy.getDimensionId(self.theFromName,fromDimension)

    toDimension = self.toObjectCombo.GetValue()
    if (toDimension != ''):
      toDimensionId = self.dbProxy.getDimensionId(toDimension,'trace_dimension')
      if (self.dbProxy.allowableTraceDimension(self.theFromObject,toDimensionId)):
        return
    self.toObjectCombo.SetItems(self.dbProxy.traceDimensionList(self.theFromObject,True))
    self.toObjectCombo.SetSelection(0)

  def onFromNameChange(self,evt):
    self.theFromName = self.fromNameCombo.GetStringSelection()
    dimName = self.fromObjectCombo.GetStringSelection()
    self.theFromId = self.dbProxy.getDimensionId(self.theFromName,dimName)

  def onToObjectChange(self,evt):
    self.toNameCombo.Clear()
    toDimension = self.toObjectCombo.GetStringSelection()
    self.theToObject = self.dbProxy.getDimensionId(toDimension,'trace_dimension')
    self.toNameCombo.SetItems(self.dbProxy.getDimensionNames(toDimension))
    self.toNameCombo.SetSelection(0)
    self.theToName = self.toNameCombo.GetStringSelection()
    self.theToId = self.dbProxy.getDimensionId(self.theToName,toDimension)

    fromDimension = self.fromObjectCombo.GetValue()
    if (fromDimension != ''):
      fromDimensionId = self.dbProxy.getDimensionId(fromDimension,'trace_dimension')
      if (self.dbProxy.allowableTraceDimension(fromDimensionId,self.theToObject)):
        return
    self.fromObjectCombo.SetItems(self.dbProxy.traceDimensionList(self.theToObject,False))
    self.fromObjectCombo.SetSelection(0)

  def onToNameChange(self,evt):
    self.theToName = self.toNameCombo.GetStringSelection()
    dimName = self.toObjectCombo.GetStringSelection()
    self.theToId = self.dbProxy.getDimensionId(self.theToName,dimName)
