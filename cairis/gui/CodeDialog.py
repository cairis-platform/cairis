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
from CodePanel import CodePanel
from cairis.core.CodeParameters import CodeParameters
import DialogClassParameters

__author__ = 'Shamal Faily'

class CodeDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,parameters.id(),parameters.label(),style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,300))
    self.theName = ''
    self.theType = ''
    self.theDescription = ''
    self.theInclusionCriteria = ''
    self.theExample = ''
    self.theId = -1
    self.panel = 0
    self.buildControls(parameters)
    self.commitVerb = 'Add'
    
  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = CodePanel(self)
    self.panel.buildControls(parameters.createFlag(),parameters.label())
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,CODE_BUTTONCOMMIT_ID,self.onCommit)
    wx.EVT_BUTTON(self,wx.ID_CLOSE,self.onClose)

  def onClose(self,evt):
    self.Destroy()

  def load(self,objt):
    self.theId = objt.id()
    self.panel.loadControls(objt)
    self.commitVerb = 'Edit'

  def onCommit(self,evt):
    commitLabel = self.commitVerb + ' code'
    nameCtrl = self.FindWindowById(CODE_TEXTNAME_ID)
    typeCtrl = self.FindWindowById(CODE_COMBOTYPE_ID)
    descCtrl = self.FindWindowById(CODE_TEXTDESCRIPTION_ID)
    incCritCtrl = self.FindWindowById(CODE_TEXTINCLUSIONCRITERIA_ID)
    codeEgCtrl = self.FindWindowById(CODE_TEXTEXAMPLE_ID)
    self.theName = nameCtrl.GetValue()
    self.theType = typeCtrl.GetValue()
    self.theDescription = descCtrl.GetValue()
    self.theInclusionCriteria = incCritCtrl.GetValue()
    self.theExample = codeEgCtrl.GetValue()

    if len(self.theName) == 0:
      dlg = wx.MessageDialog(self,'Name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theType) == 0:
      dlg = wx.MessageDialog(self,'Type must be selected',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theDescription) == 0:
      dlg = wx.MessageDialog(self,'Description cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theInclusionCriteria) == 0):
      dlg = wx.MessageDialog(self,'Inclusion criteria cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theExample) == 0):
      dlg = wx.MessageDialog(self,'Code example cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(CODE_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = CodeParameters(self.theName,self.theType,self.theDescription,self.theInclusionCriteria,self.theExample)
    parameters.setId(self.theId)
    return parameters
