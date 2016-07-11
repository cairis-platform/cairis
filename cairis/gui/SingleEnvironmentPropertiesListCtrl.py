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

class SingleEnvironmentPropertiesListCtrl(wx.ListCtrl):
  def __init__(self,parent,winId,values,boxSize=wx.DefaultSize):
    wx.ListCtrl.__init__(self,parent,winId,size=boxSize,style=wx.LC_REPORT)
    self.theCurrentEnvironment = ''
    self.InsertColumn(0,'Property')
    self.SetColumnWidth(0,150)
    self.InsertColumn(1,'Value')
    self.SetColumnWidth(1,300)
    self.InsertColumn(2,'Rationale')
    self.SetColumnWidth(1,300)
    self.theDimMenu = wx.Menu()
    self.theDimMenu.Append(PROPERTIESLISTCTRL_MENUADD_ID,'Add')
    self.theDimMenu.Append(PROPERTIESLISTCTRL_MENUDELETE_ID,'Delete')
    self.theSelectedValue = ''
    self.theSelectedIdx = -1
    self.valueLookup = values

    self.setProperties = set([])
    self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK,self.OnRightDown)
    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.onItemActivated)

    wx.EVT_MENU(self.theDimMenu,PROPERTIESLISTCTRL_MENUADD_ID,self.onAddProperty)
    wx.EVT_MENU(self.theDimMenu,PROPERTIESLISTCTRL_MENUDELETE_ID,self.onDeleteProperty)

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
    dlg = PropertyDialog(self,self.setProperties,self.valueLookup.values())
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
      self.setProperties.add(propertyName)


  def onAddProperty(self,evt):
    dlg = PropertyDialog(self,self.setProperties,self.valueLookup.values())
    if (dlg.ShowModal() == PROPERTY_BUTTONADD_ID):
      propertyName = dlg.property()
      propertyValue = dlg.value()
      pRationale = dlg.rationale()
      idx = self.GetItemCount()
      self.InsertStringItem(idx,propertyName)
      self.SetStringItem(idx,1,propertyValue)
      self.SetStringItem(idx,2,pRationale)
      self.theSelectedValue = propertyName
      self.setProperties.add(propertyName)

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
      self.setProperties.remove(selectedValue)

  def load(self,syProperties):
    cProperty = syProperties[C_PROPERTY][0]
    cRationale = syProperties[C_PROPERTY][1]
    if (cProperty != NONE_VALUE):
      idx = self.GetItemCount()
      self.InsertStringItem(idx,'Confidentiality')
      self.SetStringItem(idx,1,self.valueLookup.name(cProperty))
      self.SetStringItem(idx,2,cRationale)
      self.setProperties.add('Confidentiality')

    iProperty = syProperties[I_PROPERTY][0]
    iRationale = syProperties[I_PROPERTY][1]
    if (iProperty != NONE_VALUE):
      idx = self.GetItemCount()
      self.InsertStringItem(idx,'Integrity')
      self.SetStringItem(idx,1,self.valueLookup.name(iProperty))
      self.SetStringItem(idx,2,iRationale)
      self.setProperties.add('Integrity')

    avProperty = syProperties[AV_PROPERTY][0]
    avRationale = syProperties[AV_PROPERTY][1]
    if (avProperty != NONE_VALUE):
      idx = self.GetItemCount()
      self.InsertStringItem(idx,'Availability')
      self.SetStringItem(idx,1,self.valueLookup.name(avProperty))
      self.SetStringItem(idx,2,avRationale)
      self.setProperties.add('Availability')

    acProperty = syProperties[AC_PROPERTY][0]
    acRationale = syProperties[AC_PROPERTY][1]
    if (acProperty != NONE_VALUE):
      idx = self.GetItemCount()
      self.InsertStringItem(idx,'Accountability')
      self.SetStringItem(idx,1,self.valueLookup.name(acProperty))
      self.SetStringItem(idx,2,acRationale)
      self.setProperties.add('Accountability')

    anProperty = syProperties[AN_PROPERTY][0]
    anRationale = syProperties[AN_PROPERTY][1]
    if (anProperty != NONE_VALUE):
      idx = self.GetItemCount()
      self.InsertStringItem(idx,'Anonymity')
      self.SetStringItem(idx,1,self.valueLookup.name(anProperty))
      self.SetStringItem(idx,2,anRationale)
      self.setProperties.add('Anonymity')

    panProperty = syProperties[PAN_PROPERTY][0]
    panRationale = syProperties[PAN_PROPERTY][1]
    if (panProperty != NONE_VALUE):
      idx = self.GetItemCount()
      self.InsertStringItem(idx,'Pseudonymity')
      self.SetStringItem(idx,1,self.valueLookup.name(panProperty))
      self.SetStringItem(idx,2,panRationale)
      self.setProperties.add('Pseudonymity')

    unlProperty = syProperties[UNL_PROPERTY][0]
    unlRationale = syProperties[UNL_PROPERTY][1]
    if (unlProperty != NONE_VALUE):
      idx = self.GetItemCount()
      self.InsertStringItem(idx,'Unlinkability')
      self.SetStringItem(idx,1,self.valueLookup.name(unlProperty))
      self.SetStringItem(idx,2,unlRationale)
      self.setProperties.add('Unlinkability')

    unoProperty = syProperties[UNO_PROPERTY][0]
    unoRationale = syProperties[UNO_PROPERTY][1]
    if (unoProperty != NONE_VALUE):
      idx = self.GetItemCount()
      self.InsertStringItem(idx,'Unobservability')
      self.SetStringItem(idx,1,self.valueLookup.name(unoProperty))
      self.SetStringItem(idx,2,unoRationale)
      self.setProperties.add('Unobservability')


  def properties(self):
    cProp = iProp = avProp = acProp = anProp = panProp = unlProp = unoProp = 0
    cRat = iRat = avRat = acRat = anRat = panRat = unlRat = unoRat = 0
    for x in range(self.GetItemCount()):
      propertyName = self.GetItemText(x)
      valueItem = self.GetItem(x,1)
      rItem = self.GetItem(x,2)
      propertyValue = valueItem.GetText()
      propertyRationale = rItem.GetText()
      if (propertyName == 'Confidentiality'):
        cProp = self.valueLookup.id(propertyValue)
        cRat = propertyRationale
      elif (propertyName == 'Integrity'):
        iProp = self.valueLookup.id(propertyValue)
        iRat = propertyRationale
      elif (propertyName == 'Availability'):
        avProp = self.valueLookup.id(propertyValue)
        avRat = propertyRationale
      elif (propertyName == 'Accountability'):
        acProp = self.valueLookup.id(propertyValue)
        acRat = propertyRationale
      elif (propertyName == 'Anonymity'):
        anProp = self.valueLookup.id(propertyValue)
        anRat = propertyRationale
      elif (propertyName == 'Pseudonymity'):
        panProp = self.valueLookup.id(propertyValue)
        panRat = propertyRationale
      elif (propertyName == 'Unlinkability'):
        unlProp = self.valueLookup.id(propertyValue)
        unlRat = propertyRationale
      elif (propertyName == 'Unobservability'):
        unoProp = self.valueLookup.id(propertyValue)
        unoRat = propertyRationale
    return [(cProp,cRat),(iProp,iRat),(avProp,avRat),(acProp,acRat),(anProp,anRat),(panProp,panRat),(unlProp,unlRat),(unoProp,unoRat)]
