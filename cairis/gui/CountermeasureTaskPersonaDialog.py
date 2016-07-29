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
import cairis.core.MySQLDatabaseProxy

__author__ = 'Shamal Faily'

class CountermeasureTaskPersonaDialog(wx.Dialog):
  def __init__(self,parent,taskName,personaName,duration,frequency,demands,goalSupport):
    wx.Dialog.__init__(self,parent,TASKPERSONA_ID,'Add Task Persona',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,400))
    self.theDuration = ''
    self.theFrequency = ''
    self.theDemands = ''
    self.theGoalSupport = ''
    mainSizer = wx.BoxSizer(wx.VERTICAL)

    suPropertyValues = ['High Help','Medium Help','Low Help','None','Low Hindrance','Medium Hindrance','High Hindrance']
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Task',(87,30),COUNTERMEASURETASKPERSONA_TEXTTASK_ID,isReadOnly = True),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Persona',(87,30),COUNTERMEASURETASKPERSONA_TEXTPERSONA_ID,isReadOnly = True),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Duration',(87,30),COUNTERMEASURETASKPERSONA_COMBODURATION_ID,suPropertyValues),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Frequency',(87,30),COUNTERMEASURETASKPERSONA_COMBOFREQUENCY_ID,suPropertyValues),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Demands',(87,30),COUNTERMEASURETASKPERSONA_COMBODEMANDS_ID,suPropertyValues),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Goal Conflict',(87,30),COUNTERMEASURETASKPERSONA_COMBOGOALSUPPORT_ID,suPropertyValues),0,wx.EXPAND)
    mainSizer.Add(wx.StaticText(self,-1),1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildAddCancelButtonSizer(self,COUNTERMEASURETASKPERSONA_BUTTONADD_ID),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

    wx.EVT_BUTTON(self,COUNTERMEASURETASKPERSONA_BUTTONADD_ID,self.onAdd)
   
    taskCtrl = self.FindWindowById(COUNTERMEASURETASKPERSONA_TEXTTASK_ID)
    taskCtrl.SetValue(taskName)
    personaCtrl = self.FindWindowById(COUNTERMEASURETASKPERSONA_TEXTPERSONA_ID)
    personaCtrl.SetValue(personaName)
    durCtrl = self.FindWindowById(COUNTERMEASURETASKPERSONA_COMBODURATION_ID)
    durCtrl.SetStringSelection(duration)
    freqCtrl = self.FindWindowById(COUNTERMEASURETASKPERSONA_COMBOFREQUENCY_ID)
    freqCtrl.SetStringSelection(frequency)
    demCtrl = self.FindWindowById(COUNTERMEASURETASKPERSONA_COMBODEMANDS_ID)
    demCtrl.SetStringSelection(demands)
    gsupCtrl = self.FindWindowById(COUNTERMEASURETASKPERSONA_COMBOGOALSUPPORT_ID)
    gsupCtrl.SetStringSelection(goalSupport)

  def onAdd(self,evt):
    durCtrl = self.FindWindowById(COUNTERMEASURETASKPERSONA_COMBODURATION_ID)
    freqCtrl = self.FindWindowById(COUNTERMEASURETASKPERSONA_COMBOFREQUENCY_ID)
    demCtrl = self.FindWindowById(COUNTERMEASURETASKPERSONA_COMBODEMANDS_ID)
    gsupCtrl = self.FindWindowById(COUNTERMEASURETASKPERSONA_COMBOGOALSUPPORT_ID)
    self.theDuration = durCtrl.GetStringSelection()
    self.theFrequency = freqCtrl.GetStringSelection()
    self.theDemands = demCtrl.GetStringSelection()
    self.theGoalSupport = gsupCtrl.GetStringSelection()

    if (len(self.theDuration) == 0):
      dlg = wx.MessageDialog(self,'No duration selected','Add Task Persona',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theFrequency) == 0):
      dlg = wx.MessageDialog(self,'No frequency selected','Add Task Persona',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theDemands) == 0):
      dlg = wx.MessageDialog(self,'No demands selected','Add Task Persona',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theGoalSupport) == 0):
      dlg = wx.MessageDialog(self,'No goal support selected','Add Task Persona',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(COUNTERMEASURETASKPERSONA_BUTTONADD_ID)

  def duration(self): return self.theDuration
  def frequency(self): return self.theFrequency
  def demands(self): return self.theDemands
  def goalsupport(self): return self.theGoalSupport
