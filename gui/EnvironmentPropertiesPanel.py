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
import armid
from DimensionListCtrl import DimensionListCtrl
from Environment import Environment

class EnvironmentPropertiesPanel(wx.Panel):
  def __init__(self,parent,dp):
    wx.Panel.__init__(self,parent,armid.ENVIRONMENT_PANELENVIRONMENTPROPERTIES_ID)
    self.theEnvironmentPanel= parent

    mainSizer = wx.BoxSizer(wx.VERTICAL)

    environmentBox = wx.StaticBox(self,-1,)
    environmentFrameSizer = wx.StaticBoxSizer(environmentBox,wx.VERTICAL)
    mainSizer.Add(environmentFrameSizer,1,wx.EXPAND)
    self.environmentList = DimensionListCtrl(self,armid.ENVIRONMENT_LISTENVIRONMENTS_ID,wx.DefaultSize,'Environment','environment',dp,'Adding one or more environments indicates that this is a composite environment')
    environmentFrameSizer.Add(self.environmentList,1,wx.EXPAND)

    propertiesBox = wx.StaticBox(self,-1,'Duplication properties')
    propertiesFrameSizer = wx.StaticBoxSizer(propertiesBox,wx.VERTICAL)
    mainSizer.Add(propertiesFrameSizer,1,wx.EXPAND)
    propertiesSizer = wx.FlexGridSizer(rows = 2, cols = 3)
    propertiesFrameSizer.Add(propertiesSizer,1,wx.EXPAND)
    propertiesSizer.Add(wx.StaticText(self,-1,'Override'))
    self.overrideRadio = wx.RadioButton(self,armid.ENVIRONMENT_RADIOOVERRIDE_ID,style=wx.RB_GROUP)
    self.overrideRadio.SetToolTip(wx.ToolTip('If an artifact exists in multiple environments, choose the artifact\'s value for the overriding environment.'))
    propertiesSizer.Add(self.overrideRadio)
    self.overrideCombo = wx.ComboBox(self,armid.ENVIRONMENT_COMBOOVERRIDE_ID,'',choices=[],style=wx.CB_READONLY | wx.CB_DROPDOWN)
    propertiesSizer.Add(self.overrideCombo,0,wx.EXPAND)
    propertiesSizer.Add(wx.StaticText(self,-1,'Maximise'))
    self.maxRadio = wx.RadioButton(self,armid.ENVIRONMENT_RADIOMAXIMISE_ID)
    self.maxRadio.SetToolTip(wx.ToolTip('If an artifact exists in multiple environments, choose the artifact\'s maximal values.'))
    propertiesSizer.Add(self.maxRadio)
    propertiesSizer.AddGrowableCol(2)
    self.SetSizer(mainSizer)
    self.environmentList.Bind(wx.EVT_LIST_INSERT_ITEM,self.onEnvironmentAdded)
    self.environmentList.Bind(wx.EVT_LIST_DELETE_ITEM,self.onEnvironmentDeleted)
    self.overrideRadio.Bind(wx.EVT_RADIOBUTTON,self.onOverrideClick)
    self.maxRadio.Bind(wx.EVT_RADIOBUTTON,self.onMaximiseClick)
    self.overrideRadio.Disable()
    self.overrideCombo.Disable()
    self.maxRadio.Disable()

  def load(self,environment):
    environments = environment.environments()
    if (len(environments) > 0):
      self.environmentList.load(environments)
      if (environment.duplicateProperty() == 'Maximise'):
        self.maxRadio.Enable()
        self.maxRadio.SetValue(True)
        self.overrideCombo.Disable()
      else:
        self.overrideRadio.Enable()
        self.overrideCombo.Enable()
        self.overrideRadio.SetValue(True)
        self.overrideCombo.SetStringSelection(environment.overridingEnvironment())

  def onOverrideClick(self,evt):
    if (self.overrideRadio.GetValue() == True):
      self.overrideCombo.Enable()
    else: 
      self.overrideCombo.Disable()

  def onMaximiseClick(self,evt):
    if (self.maxRadio.GetValue() == True):
      self.overrideCombo.Disable()
    else: 
      self.overrideCombo.Enable()

  def onEnvironmentAdded(self,evt):
    currentEnvironmentSelection = ''
    if (self.overrideCombo.GetCount() > 0):
      currentEnvironmentSelection =  self.overrideCombo.GetStringSelection() 
    newItem = self.environmentList.GetItemText(evt.GetIndex())
    if (self.overrideCombo.FindString(newItem) == wx.NOT_FOUND):
      self.overrideCombo.Append(newItem)
    if (len(currentEnvironmentSelection) > 0):
      self.overrideCombo.SetStringSelection(currentEnvironmentSelection)
    self.overrideRadio.Enable()
    self.overrideCombo.Enable()
    self.maxRadio.Enable()
    evt.Skip()

  def onEnvironmentDeleted(self,evt):
    currentEnvironmentSelection = ''
    if (self.overrideCombo.GetCount() > 0):
      currentEnvironmentSelection =  self.overrideCombo.GetStringSelection() 
    deletedItem = self.environmentList.GetItemText(evt.GetIndex())
    self.overrideCombo.Delete(self.overrideCombo.FindString(deletedItem))

    environmentCount = self.overrideCombo.GetCount()
    if ((deletedItem == currentEnvironmentSelection) or (environmentCount == 0)):
      self.overrideCombo.SetValue('')
    else:
      self.overrideCombo.SetStringSelection(currentEnvironmentSelection)

    if (environmentCount == 0):
      self.overrideRadio.Disable()
      self.overrideCombo.Disable()
      self.maxRadio.Disable()
    evt.Skip()


  def environments(self):
    return self.environmentList.dimensions()

  def duplicateProperty(self):
    if (self.maxRadio.GetValue() == True):
      return 'Maximise'
    else: 
      return 'Override'
  
  def overridingEnvironment(self):
    if (self.maxRadio.GetValue() == True):
      return ''
    else:
      return self.overrideCombo.GetValue()
