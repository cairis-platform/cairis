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
from BehaviouralCharacteristicsDialog import BehaviouralCharacteristicsDialog
from cairis.core.Borg import Borg
from AssumptionTaskModel import AssumptionTaskModel
from ATModelViewer import ATModelViewer

class TCNarrativeTextCtrl(wx.TextCtrl):
  def __init__(self, parent, winId):
    wx.TextCtrl.__init__(self,parent,winId,size=(150,100),style=wx.TE_MULTILINE)
    self.ctrlMenu = wx.Menu()
    self.cmItem = self.ctrlMenu.Append(TCNTC_LISTCHARACTERISTICS_ID,'Characteristics')
    self.viItem = self.ctrlMenu.Append(TCNTC_VISCHARACTERISTICS_ID,'Visualise')
    wx.EVT_MENU(self,TCNTC_LISTCHARACTERISTICS_ID,self.onListCharacteristics)
    wx.EVT_MENU(self,TCNTC_VISCHARACTERISTICS_ID,self.onVisualiseCharacteristics)
    self.Bind(wx.EVT_RIGHT_DOWN, self.onRightClick)

    self.theTaskName = ''

    self.cmItem.Enable(False)
    self.viItem.Enable(False)

  def onRightClick(self,evt):
    self.PopupMenu(self.ctrlMenu)

  def onListCharacteristics(self,evt):
    try:
      dialog = BehaviouralCharacteristicsDialog(self,self.theTaskName)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Task Characteristics',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def Set(self,tName,ctrlVal):
    self.theTaskName = tName
    self.SetValue(ctrlVal)
    if (tName == ''):
      self.cmItem.Enable(False)
      self.viItem.Enable(False)
    else:
      self.cmItem.Enable(True)
      self.viItem.Enable(True)

  def onListCharacteristics(self,evt):
    try:
      dialog = BehaviouralCharacteristicsDialog(self,self.theTaskName)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Task Characteristics',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onVisualiseCharacteristics(self,evt):
    dialog = None
    try:
      b = Borg()
      modelAssocs = b.dbProxy.assumptionTaskModel(self.theTaskName)
      if (len(modelAssocs) > 0):
        associations = AssumptionTaskModel(modelAssocs)
        dialog = ATModelViewer(self.theTaskName)
        dialog.ShowModal(associations)
      else:
        errorTxt = 'No assumption task associations defined'
        dlg = wx.MessageDialog(self,errorTxt,'View Assumption Task Model',wx.OK | wx.ICON_EXCLAMATION)
        dlg.ShowModal()
        dlg.Destroy()
    except ARMException,errorText:
      dialog.destroy()
      dlg = wx.MessageDialog(self,str(errorText),'Edit Task Characteristics',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
