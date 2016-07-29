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
from CodingTextCtrl import CodingTextCtrl
from cairis.core.armid import *
from cairis.core.ARM import *
from BehaviouralCharacteristicsDialog import BehaviouralCharacteristicsDialog
from cairis.core.Borg import Borg
from AssumptionPersonaModel import AssumptionPersonaModel
from APModelViewer import APModelViewer

__author__ = 'Shamal Faily'

class BVNarrativeTextCtrl(CodingTextCtrl):
  def __init__(self, parent, winId):
    CodingTextCtrl.__init__(self,parent,winId)
    self.ctrlMenu = wx.Menu()
    self.cmItem = self.ctrlMenu.Append(BVNTC_LISTCHARACTERISTICS_ID,'Characteristics')
    self.viItem = self.ctrlMenu.Append(BVNTC_VISCHARACTERISTICS_ID,'Visualise')
    self.ctrlMenu.AppendMenu(BVNTC_MENU_CODING,'Coding',self.codingMenu)

    wx.EVT_MENU(self,BVNTC_LISTCHARACTERISTICS_ID,self.onListCharacteristics)
    wx.EVT_MENU(self,BVNTC_VISCHARACTERISTICS_ID,self.onVisualiseCharacteristics)
    wx.EVT_MENU(self,BVNTC_TEXTOPENCODING_ID,self.onOpenCoding)
    wx.EVT_MENU(self,BVNTC_LISTALPHABET_ID,self.onListAlphabet)
    self.Bind(wx.EVT_RIGHT_DOWN, self.onRightClick)

    self.thePersonaName = ''
    self.theBehaviouralVariable = ''

  def onRightClick(self,evt):
    self.enableCodingCtrls()
    self.PopupMenu(self.ctrlMenu)

  def onListCharacteristics(self,evt):
    try:
      dialog = BehaviouralCharacteristicsDialog(self,self.thePersonaName,self.theBehaviouralVariable)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Persona Characteristics',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def Set(self,pName,bvName,ctrlVal):
    self.thePersonaName = pName
    self.theBehaviouralVariable = bvName
    self.SetValue(ctrlVal)
    if (pName == ''):
      self.cmItem.Enable(False)
      self.viItem.Enable(False)
    else:
      self.cmItem.Enable(True)
      self.viItem.Enable(True)

  def onListCharacteristics(self,evt):
    try:
      dialog = BehaviouralCharacteristicsDialog(self,self.thePersonaName,self.theBehaviouralVariable)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Persona Characteristics',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onVisualiseCharacteristics(self,evt):
    dialog = None
    try:
      b = Borg()
      modelAssocs = b.dbProxy.assumptionPersonaModel(self.thePersonaName,self.theBehaviouralVariable)
      if (len(modelAssocs) > 0):
        associations = AssumptionPersonaModel(modelAssocs)
        dialog = APModelViewer(self.thePersonaName,self.theBehaviouralVariable)
        dialog.ShowModal(associations)
      else:
        errorTxt = 'No assumption persona associations defined'
        dlg = wx.MessageDialog(self,errorTxt,'View Assumption Persona Model',wx.OK | wx.ICON_EXCLAMATION)
        dlg.ShowModal()
        dlg.Destroy()
    except ARMException,errorText:
      dialog.destroy()
      dlg = wx.MessageDialog(self,str(errorText),'Edit Persona Characteristics',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
