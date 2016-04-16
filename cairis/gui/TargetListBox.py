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

class TargetListBox(wx.ListBox):
  def __init__(self,parent,winId,boxSize,dp,rl):
    wx.ListBox.__init__(self,parent,winId,size=boxSize)
    self.dbProxy = dp
    self.theDimMenu = wx.Menu()
    self.theDimMenu.Append(DIMLIST_MENUADD_ID,'Add')
    self.theDimMenu.Append(DIMLIST_MENUDELETE_ID,'Delete')
    self.theRiskList = rl
    self.theSelectedValue = ''
    self.Bind(wx.EVT_RIGHT_DOWN,self.OnRightDown)
    wx.EVT_MENU(self.theDimMenu,DIMLIST_MENUADD_ID,self.onAddDimension)
    wx.EVT_MENU(self.theDimMenu,DIMLIST_MENUDELETE_ID,self.onDeleteDimension)

  def OnRightDown(self,evt):
    self.PopupMenu(self.theDimMenu)

  def onAddDimension(self,evt):
    targetList = self.dbProxy.targetNames(self.theRiskList.GetItems())
    from DimensionNameDialog import DimensionNameDialog
    dlg = DimensionNameDialog(self,'Target',targetList,'Add')
    if (dlg.ShowModal() == DIMNAME_BUTTONACTION_ID):
      additionalDimension = dlg.dimensionName()
      self.Append(additionalDimension)
      self.theSelectedValue = additionalDimension

  def onDeleteDimension(self,evt):
    idx = self.GetSelection()
    if (idx == -1):
      errorText = 'No ' + self.theDimensionTable + ' selected'
      errorLabel = 'Delete ' + self.theDimensionTable
      dlg = wx.MessageDialog(self,errorText,errorLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
    else:
      self.theSelectedValue = self.GetSelection()
      self.Delete(self.theSelectedValue)
