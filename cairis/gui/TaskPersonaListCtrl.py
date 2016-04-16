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
from TaskPersonaDialog import TaskPersonaDialog

class TaskPersonaListCtrl(wx.ListCtrl):
  def __init__(self,parent,winId,dp,boxSize=wx.DefaultSize):
    wx.ListCtrl.__init__(self,parent,winId,size=boxSize,style=wx.LC_REPORT)
    self.dbProxy = dp

    self.durationLookup = {}
    self.durationLookup['Seconds'] = 'Low'
    self.durationLookup['Minutes'] = 'Medium'
    self.durationLookup['Hours or longer'] = 'High'
    self.durationLookup['None'] = 'None'

    self.durationReverseLookup = {}
    self.durationReverseLookup['Low'] = 'Seconds'
    self.durationReverseLookup['Medium'] = 'Minutes'
    self.durationReverseLookup['High'] = 'Hours or longer'
    self.durationReverseLookup['None'] = 'None'

    self.frequencyLookup = {}
    self.frequencyLookup['Hourly or more'] = 'High'
    self.frequencyLookup['Daily - Weekly'] = 'Medium'
    self.frequencyLookup['Monthly or less'] = 'Low'
    self.frequencyLookup['None'] = 'None'

    self.frequencyReverseLookup = {}
    self.frequencyReverseLookup['High'] = 'Hourly or more'
    self.frequencyReverseLookup['Medium'] = 'Daily - Weekly'
    self.frequencyReverseLookup['Low'] = 'Monthly or less'
    self.frequencyReverseLookup['None'] = 'None'

    self.theCurrentEnvironment = ''
    self.InsertColumn(0,'Persona')
    self.SetColumnWidth(0,150)
    self.InsertColumn(1,'Duration')
    self.SetColumnWidth(1,100)
    self.InsertColumn(2,'Frequency')
    self.SetColumnWidth(2,100)
    self.InsertColumn(3,'Demands')
    self.SetColumnWidth(3,100)
    self.InsertColumn(4,'Goals')
    self.SetColumnWidth(4,100)
    self.theDimMenu = wx.Menu()
    self.theDimMenu.Append(TASKPERSONALISTCTRL_MENUADD_ID,'Add')
    self.theDimMenu.Append(TASKPERSONALISTCTRL_MENUDELETE_ID,'Delete')
    self.theSelectedValue = ''
    self.theSelectedIdx = -1
    self.setPersonas = {}
    self.Bind(wx.EVT_RIGHT_DOWN,self.OnRightDown)
    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.onPersonaActivated)
    wx.EVT_MENU(self.theDimMenu,TASKPERSONALISTCTRL_MENUADD_ID,self.onAddTaskPersona)
    wx.EVT_MENU(self.theDimMenu,TASKPERSONALISTCTRL_MENUDELETE_ID,self.onDeleteTaskPersona)

  def setEnvironment(self,environmentName):
    self.theCurrentEnvironment = environmentName
    if ((self.theCurrentEnvironment in self.setPersonas) == False):
      self.setPersonas[self.theCurrentEnvironment] = set([])

  def OnItemSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()

  def OnItemDeselected(self,evt):
    self.theSelectedIdx = -1

  def OnRightDown(self,evt):
    self.PopupMenu(self.theDimMenu)

  def onPersonaActivated(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    pName = self.GetItemText(self.theSelectedIdx)
    pDur = self.GetItem(self.theSelectedIdx,1)
    pFreq = self.GetItem(self.theSelectedIdx,2)
    pDem = self.GetItem(self.theSelectedIdx,3)
    pGsup = self.GetItem(self.theSelectedIdx,4)

    dlg = TaskPersonaDialog(self,self.setPersonas[self.theCurrentEnvironment],self.theCurrentEnvironment,self.dbProxy,pName,pDur.GetText(),pFreq.GetText(),pDem.GetText(),pGsup.GetText())
    if (dlg.ShowModal() == TASKPERSONA_BUTTONADD_ID):
      self.SetStringItem(self.theSelectedIdx,0,dlg.persona())
      self.SetStringItem(self.theSelectedIdx,1,dlg.duration())
      self.SetStringItem(self.theSelectedIdx,2,dlg.frequency())
      self.SetStringItem(self.theSelectedIdx,3,dlg.demands())
      self.SetStringItem(self.theSelectedIdx,4,dlg.goalsupport())

  def onAddTaskPersona(self,evt):
    dlg = TaskPersonaDialog(self,self.setPersonas[self.theCurrentEnvironment],self.theCurrentEnvironment,self.dbProxy)
    if (dlg.ShowModal() == TASKPERSONA_BUTTONADD_ID):
      pName = dlg.persona()
      pDur = dlg.duration()
      pFreq = dlg.frequency()
      pDem = dlg.demands()
      pGsup = dlg.goalsupport()
      idx = self.GetItemCount()
      self.InsertStringItem(idx,pName)
      self.SetStringItem(idx,1,pDur)
      self.SetStringItem(idx,2,pFreq)
      self.SetStringItem(idx,3,pDem)
      self.SetStringItem(idx,4,pGsup)
      self.theSelectedValue = pName
      (self.setPersonas[self.theCurrentEnvironment]).add(pName)

  def onDeleteTaskPersona(self,evt):
    if (self.theSelectedIdx == -1):
      errorText = 'No Task Persona selected'
      errorLabel = 'Delete Task Persona'
      dlg = wx.MessageDialog(self,errorText,errorLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
    else:
      selectedValue = self.GetItemText(self.theSelectedIdx)
      self.DeleteItem(self.theSelectedIdx)
      (self.setPersonas[self.theCurrentEnvironment]).remove(selectedValue)

  def load(self,personas):
    for persona,dur,freq,dem,gsup in personas:
      idx = self.GetItemCount()
      self.InsertStringItem(idx,persona)
      self.SetStringItem(idx,1,self.durationReverseLookup[dur])
      self.SetStringItem(idx,2,self.frequencyReverseLookup[freq])
      self.SetStringItem(idx,3,dem)
      self.SetStringItem(idx,4,gsup)
      (self.setPersonas[self.theCurrentEnvironment]).add(persona)

  def dimensions(self):
    personas = []
    for x in range(self.GetItemCount()):
      persona = self.GetItemText(x)
      pDur = self.GetItem(x,1)
      pFreq = self.GetItem(x,2)
      pDem = self.GetItem(x,3)
      pGsup = self.GetItem(x,4)
      personas.append((persona,self.durationLookup[pDur.GetText()],self.frequencyLookup[pFreq.GetText()],pDem.GetText(),pGsup.GetText()))
    return personas
