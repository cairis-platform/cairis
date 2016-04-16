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

class PropertyDialog(wx.Dialog):
  def __init__(self,parent,setProperties,values):
    wx.Dialog.__init__(self,parent,PROPERTY_ID,'Add Security Property',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,300))

    weights = {"Confidentiality":0,"Integrity":1,"Availability":2,"Accountability":3,"Anonymity":4,"Pseudonymity":5,"Unlinkability":6,"Unobservability":7}
    self.thePropertyName = ''
    self.thePropertyValue = ''
    self.thePropertyRationale = 'None'
    self.commitLabel = 'Add'
    mainSizer = wx.BoxSizer(wx.VERTICAL)
#    defaultProperties = set(['Confidentiality','Integrity','Availability','Accountability','Anonymity','Pseudonymity','Unlinkability','Unobservability'])
    defaultProperties = set(weights.keys())
    propertyList = sorted(list(defaultProperties.difference(setProperties)), key=lambda x:weights[x])
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Property',(87,30),PROPERTY_COMBOPROPERTY_ID,propertyList),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Value',(87,30),PROPERTY_COMBOVALUE_ID,values),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildMLTextSizer(self,'Rationale',(87,60),PROPERTY_TEXTRATIONALE_ID),1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildAddCancelButtonSizer(self,PROPERTY_BUTTONADD_ID),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,PROPERTY_BUTTONADD_ID,self.onCommit)

  def load(self,pName,pValue,pRationale):
    propertyCtrl = self.FindWindowById(PROPERTY_COMBOPROPERTY_ID)
    valueCtrl = self.FindWindowById(PROPERTY_COMBOVALUE_ID)
    ratCtrl = self.FindWindowById(PROPERTY_TEXTRATIONALE_ID)
    commitCtrl = self.FindWindowById(PROPERTY_BUTTONADD_ID)
    commitCtrl.SetLabel('Edit')
    propertyCtrl.SetValue(pName)
    valueCtrl.SetValue(pValue)
    ratCtrl.SetValue(pRationale)
    self.commitLabel = 'Edit'
    
  def onCommit(self,evt):
    propertyCtrl = self.FindWindowById(PROPERTY_COMBOPROPERTY_ID)
    valueCtrl = self.FindWindowById(PROPERTY_COMBOVALUE_ID)
    ratCtrl = self.FindWindowById(PROPERTY_TEXTRATIONALE_ID)
    self.thePropertyName = propertyCtrl.GetValue()
    self.thePropertyValue = valueCtrl.GetValue()
    self.thePropertyRationale = ratCtrl.GetValue()

    commitTxt = self.commitLabel + ' Security Property' 
    if len(self.thePropertyName) == 0:
      dlg = wx.MessageDialog(self,'No property selected',commitTxt,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.thePropertyValue) == 0):
      dlg = wx.MessageDialog(self,'No value selected',commitTxt,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.thePropertyRationale) == 0):
      dlg = wx.MessageDialog(self,'No rationale',commitTxt,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(PROPERTY_BUTTONADD_ID)

  def property(self): return self.thePropertyName
  def value(self): return self.thePropertyValue
  def rationale(self): return self.thePropertyRationale
