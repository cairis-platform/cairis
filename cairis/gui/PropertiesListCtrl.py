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
from PropertyDialog import PropertyDialog
from cairis.core.ValueDictionary import ValueDictionary

__author__ = 'Shamal Faily'

class PropertiesListCtrl(wx.ListCtrl):
  def __init__(self,parent,winId,values,boxSize=wx.DefaultSize):
    wx.ListCtrl.__init__(self,parent,winId,size=boxSize,style=wx.LC_REPORT)
    self.theCurrentEnvironment = ''
    self.InsertColumn(0,'Property')
    self.SetColumnWidth(0,150)
    self.InsertColumn(1,'Value')
    self.SetColumnWidth(1,300)
    self.InsertColumn(2,'Rationale')
    self.SetColumnWidth(2,300)
    self.theDimMenu = wx.Menu()
    self.theDimMenu.Append(PROPERTIESLISTCTRL_MENUADD_ID,'Add')
    self.theDimMenu.Append(PROPERTIESLISTCTRL_MENUDELETE_ID,'Delete')
    self.theSelectedValue = ''
    self.theSelectedIdx = -1
    self.setProperties = {}
    self.valueLookup = values
    self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK,self.OnRightDown)
    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.onItemActivated)
    wx.EVT_MENU(self.theDimMenu,PROPERTIESLISTCTRL_MENUADD_ID,self.onAddProperty)
    wx.EVT_MENU(self.theDimMenu,PROPERTIESLISTCTRL_MENUDELETE_ID,self.onDeleteProperty)

  def setEnvironment(self,environmentName):
    self.theCurrentEnvironment = environmentName
    if ((self.theCurrentEnvironment in self.setProperties) == False):
      self.setProperties[self.theCurrentEnvironment] = set([])

  def OnItemSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()

  def OnItemDeselected(self,evt):
    self.theSelectedIdx = -1

  def OnRightDown(self,evt):
    self.PopupMenu(self.theDimMenu)

  def onItemActivated(self,evt):
    x = evt.GetIndex()
    propertyName = self.GetItemText(x)
    valueItem = self.GetItem(x,1)
    rItem = self.GetItem(x,2)
    dlg = PropertyDialog(self,self.setProperties[self.theCurrentEnvironment],self.valueLookup.values())
    dlg.load(propertyName,valueItem.GetText(),rItem.GetText())
    if (dlg.ShowModal() == PROPERTY_BUTTONADD_ID):
      pName = dlg.property()
      pValue = dlg.value()
      pRationale = dlg.rationale()
      idx = self.GetItemCount()
      self.SetStringItem(x,0,pName)
      self.SetStringItem(x,1,pValue)
      self.SetStringItem(x,2,pRationale)
      self.theSelectedValue = propertyName
      (self.setProperties[self.theCurrentEnvironment]).add(propertyName)

  def onAddProperty(self,evt):
    dlg = PropertyDialog(self,self.setProperties[self.theCurrentEnvironment],self.valueLookup.values())
    if (dlg.ShowModal() == PROPERTY_BUTTONADD_ID):
      propertyName = dlg.property()
      propertyValue = dlg.value()
      propertyRationale = dlg.rationale()
      idx = self.GetItemCount()
      self.InsertStringItem(idx,propertyName)
      self.SetStringItem(idx,1,propertyValue)
      self.SetStringItem(idx,2,propertyRationale)
      self.theSelectedValue = propertyName
      (self.setProperties[self.theCurrentEnvironment]).add(propertyName)

  def onDeleteProperty(self,evt):
    if (self.theSelectedIdx == -1):
      errorText = 'No property selected'
      errorLabel = 'Delete Security Property'
      dlg = wx.MessageDialog(self,errorText,errorLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
    else:
      selectedValue = self.GetItemText(self.theSelectedIdx)
      self.DeleteItem(self.theSelectedIdx)
      (self.setProperties[self.theCurrentEnvironment]).remove(selectedValue)

  def load(self,syProperties,pRationale):
    cProperty = syProperties[C_PROPERTY]
    cRationale = pRationale[C_PROPERTY]
    if (cProperty != NONE_VALUE):
      idx = self.GetItemCount()
      self.InsertStringItem(idx,'Confidentiality')
      self.SetStringItem(idx,1,self.valueLookup.name(cProperty))
      self.SetStringItem(idx,2,cRationale)
      (self.setProperties[self.theCurrentEnvironment]).add('Confidentiality')

    iProperty = syProperties[I_PROPERTY]
    iRationale = pRationale[I_PROPERTY]
    if (iProperty != NONE_VALUE):
      idx = self.GetItemCount()
      self.InsertStringItem(idx,'Integrity')
      self.SetStringItem(idx,1,self.valueLookup.name(iProperty))
      self.SetStringItem(idx,2,iRationale)
      (self.setProperties[self.theCurrentEnvironment]).add('Integrity')

    avProperty = syProperties[AV_PROPERTY]
    avRationale = pRationale[AV_PROPERTY]
    if (avProperty != NONE_VALUE):
      idx = self.GetItemCount()
      self.InsertStringItem(idx,'Availability')
      self.SetStringItem(idx,1,self.valueLookup.name(avProperty))
      self.SetStringItem(idx,2,avRationale)
      (self.setProperties[self.theCurrentEnvironment]).add('Availability')

    acProperty = syProperties[AC_PROPERTY]
    acRationale = pRationale[AC_PROPERTY]
    if (acProperty != NONE_VALUE):
      idx = self.GetItemCount()
      self.InsertStringItem(idx,'Accountability')
      self.SetStringItem(idx,1,self.valueLookup.name(acProperty))
      self.SetStringItem(idx,2,acRationale)
      (self.setProperties[self.theCurrentEnvironment]).add('Accountability')

    anProperty = syProperties[AN_PROPERTY]
    anRationale = pRationale[AN_PROPERTY]
    if (anProperty != NONE_VALUE):
      idx = self.GetItemCount()
      self.InsertStringItem(idx,'Anonymity')
      self.SetStringItem(idx,1,self.valueLookup.name(anProperty))
      self.SetStringItem(idx,2,anRationale)
      (self.setProperties[self.theCurrentEnvironment]).add('Anonymity')

    panProperty = syProperties[PAN_PROPERTY]
    panRationale = pRationale[PAN_PROPERTY]
    if (panProperty != NONE_VALUE):
      idx = self.GetItemCount()
      self.InsertStringItem(idx,'Pseudonymity')
      self.SetStringItem(idx,1,self.valueLookup.name(panProperty))
      self.SetStringItem(idx,2,panRationale)
      (self.setProperties[self.theCurrentEnvironment]).add('Pseudonymity')

    unlProperty = syProperties[UNL_PROPERTY]
    unlRationale = pRationale[UNL_PROPERTY]
    if (unlProperty != NONE_VALUE):
      idx = self.GetItemCount()
      self.InsertStringItem(idx,'Unlinkability')
      self.SetStringItem(idx,1,self.valueLookup.name(unlProperty))
      self.SetStringItem(idx,2,unlRationale)
      (self.setProperties[self.theCurrentEnvironment]).add('Unlinkability')

    unoProperty = syProperties[UNO_PROPERTY]
    unoRationale = pRationale[UNO_PROPERTY]
    if (unoProperty != NONE_VALUE):
      idx = self.GetItemCount()
      self.InsertStringItem(idx,'Unobservability')
      self.SetStringItem(idx,1,self.valueLookup.name(unoProperty))
      self.SetStringItem(idx,2,unoRationale)
      (self.setProperties[self.theCurrentEnvironment]).add('Unobservability')

  def properties(self):
    workingProperties = [0,0,0,0,0,0,0,0]
    workingRationale = ['None','None','None','None','None','None','None','None']
    for x in range(self.GetItemCount()):
      propertyName = self.GetItemText(x)
      valueItem = self.GetItem(x,1)
      rItem = self.GetItem(x,2)
      propertyValue = valueItem.GetText()
      propertyRationale = rItem.GetText()
      if (propertyName == 'Confidentiality'):
        workingProperties[C_PROPERTY] = self.valueLookup.id(propertyValue)
        workingRationale[C_PROPERTY] = propertyRationale
      elif (propertyName == 'Integrity'):
        workingProperties[I_PROPERTY] = self.valueLookup.id(propertyValue)
        workingRationale[I_PROPERTY] = propertyRationale
      elif (propertyName == 'Availability'):
        workingProperties[AV_PROPERTY] = self.valueLookup.id(propertyValue)
        workingRationale[AV_PROPERTY] = propertyRationale
      elif (propertyName == 'Accountability'):
        workingProperties[AC_PROPERTY] = self.valueLookup.id(propertyValue)
        workingRationale[AC_PROPERTY] = propertyRationale
      elif (propertyName == 'Anonymity'):
        workingProperties[AN_PROPERTY] = self.valueLookup.id(propertyValue)
        workingRationale[AN_PROPERTY] = propertyRationale
      elif (propertyName == 'Pseudonymity'):
        workingProperties[PAN_PROPERTY] = self.valueLookup.id(propertyValue)
        workingRationale[PAN_PROPERTY] = propertyRationale
      elif (propertyName == 'Unlinkability'):
        workingProperties[UNL_PROPERTY] = self.valueLookup.id(propertyValue)
        workingRationale[UNL_PROPERTY] = propertyRationale
      elif (propertyName == 'Unobservability'):
        workingProperties[UNO_PROPERTY] = self.valueLookup.id(propertyValue)
        workingRationale[UNO_PROPERTY] = propertyRationale
    return (workingProperties,workingRationale)
