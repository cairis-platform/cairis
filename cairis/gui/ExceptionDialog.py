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
import WidgetFactory
from ExceptionPanel import ExceptionPanel
from cairis.core.Borg import Borg

__author__ = 'Shamal Faily'

class ExceptionDialog(wx.Dialog):
  def __init__(self,parent,envName,eName = '', eDimType = 'goal', eDimName = '', eCat = '', eDef = ''):
    wx.Dialog.__init__(self,parent,EXCEPTION_ID,'Add Flow Exception',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,500))
    self.theEnvironmentName = envName
    self.theName = eName
    self.theDimensionType = eDimType
    self.theDimensionName = eDimName
    self.theCategory = eCat
    self.theDefinition = eDef
    self.panel = 0
    isCreate = True

    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = ExceptionPanel(self,self.theEnvironmentName)
    mainSizer.Add(self.panel,1,wx.EXPAND)
    if eName != '':
      self.SetLabel('Edit Flow Exception')
      self.commitVerb = 'Edit'
      self.panel.loadControls((eName,eDimType,eDimName,eCat,eDef))
      isCreate = False
    else:
      self.commitVerb = 'Add'
    mainSizer.Add(WidgetFactory.buildCommitButtonSizer(self,EXCEPTION_BUTTONCOMMIT_ID,isCreate),0,wx.CENTER)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,EXCEPTION_BUTTONCOMMIT_ID,self.onCommit)

    

  def onCommit(self,evt):
    commitLabel = self.commitVerb + ' Flow Exception'

    nameCtrl = self.FindWindowById(EXCEPTION_TEXTNAME_ID)
    goalCtrl = self.FindWindowById(EXCEPTION_COMBOGOALS_ID)
    typeCtrl = self.FindWindowById(EXCEPTION_RADIOGOAL_ID)
    catCtrl = self.FindWindowById(EXCEPTION_COMBOCATEGORY_ID)
    defCtrl = self.FindWindowById(EXCEPTION_TEXTDEFINITION_ID)


    self.theName = nameCtrl.GetValue()
    if (typeCtrl.GetValue() == True):
      self.theDimensionType = 'goal'
    else:
      self.theDimensionType = 'requirement'
    self.theDimensionName = goalCtrl.GetValue()
    self.theCategory = catCtrl.GetValue()
    self.theDefinition = defCtrl.GetValue()


    if len(self.theName) == 0:
      dlg = wx.MessageDialog(self,'Exception name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theDimensionName) == 0:
      dlg = wx.MessageDialog(self,self.theDimensionType + ' selection must be selected',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theCategory) == 0:
      dlg = wx.MessageDialog(self,'Category must be selected',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theDefinition) == 0):
      dlg = wx.MessageDialog(self,'Definition cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    self.EndModal(EXCEPTION_BUTTONCOMMIT_ID)

  def parameters(self):
    return (self.theName,self.theDimensionType,self.theDimensionName,self.theCategory,self.theDefinition)
