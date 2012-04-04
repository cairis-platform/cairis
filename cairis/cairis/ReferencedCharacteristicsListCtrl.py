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
from Borg import Borg

from ARM import *

class ReferencedCharacteristicsListCtrl(wx.ListCtrl):

  def __init__(self,parent,winId,dimName):
    wx.ListCtrl.__init__(self,parent,winId,style=wx.LC_REPORT)
    self.theParentDialog = parent
    self.theTraceMenu = wx.Menu()
    self.theDimensionName = dimName
    self.theTraceMenu.Append(armid.DRLC_MENU_REFERENCEDCHARACTERISTICS_ID,'Referenced Characteristics')
    wx.EVT_MENU(self,armid.DRLC_MENU_REFERENCEDCHARACTERISTICS_ID,self.onReferencedCharacteristics)
    self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onRightClick)


  def onRightClick(self,evt):
    self.PopupMenu(self.theTraceMenu)

  def onReferencedCharacteristics(self,evt):
    docRef = self.theParentDialog.objts[self.theParentDialog.selectedLabel]
    refName = docRef.name()
    try:
      b = Borg()
      dbProxy = b.dbProxy
      refChars = dbProxy.referenceUse(refName,self.theDimensionName)
      print refChars
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Referenced characteristics',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return
