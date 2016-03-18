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
from ConceptReferencePanel import ConceptReferencePanel
from ConceptReferenceParameters import ConceptReferenceParameters
import DialogClassParameters

class ConceptReferenceDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,parameters.id(),parameters.label(),style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,350))
    self.theName = ''
    self.theDimension = ''
    self.theObject = ''
    self.theDescription = ''
    self.theId = -1
    self.panel = 0
    self.buildControls(parameters)
    self.commitVerb = 'Add'
    
  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = ConceptReferencePanel(self)
    self.panel.buildControls(parameters.createFlag())
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.CONCEPTREFERENCE_BUTTONCOMMIT_ID,self.onCommit)

  def load(self,objt):
    self.theId = objt.id()
    self.panel.loadControls(objt)
    self.commitVerb = 'Edit'

  def onCommit(self,evt):
    commitLabel = self.commitVerb + ' concept reference'

    nameCtrl = self.FindWindowById(armid.CONCEPTREFERENCE_TEXTNAME_ID)
    dimCtrl = self.FindWindowById(armid.CONCEPTREFERENCE_COMBODIMNAME_ID)
    objtCtrl = self.FindWindowById(armid.CONCEPTREFERENCE_COMBOOBJTNAME_ID)
    descCtrl = self.FindWindowById(armid.CONCEPTREFERENCE_TEXTDESCRIPTION_ID)


    self.theName = nameCtrl.GetValue()
    self.theDimension = dimCtrl.GetValue()
    self.theObject = objtCtrl.GetValue()
    self.theDescription = descCtrl.GetValue()

    if len(self.theName) == 0:
      dlg = wx.MessageDialog(self,'Name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theDimension) == 0:
      dlg = wx.MessageDialog(self,'Dimension cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theObject) == 0:
      dlg = wx.MessageDialog(self,'Object cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theDescription) == 0:
      dlg = wx.MessageDialog(self,'Description cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(armid.CONCEPTREFERENCE_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = ConceptReferenceParameters(self.theName,self.theDimension,self.theObject,self.theDescription)
    parameters.setId(self.theId)
    return parameters
