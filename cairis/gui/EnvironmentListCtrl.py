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
from DimensionListCtrl import DimensionListCtrl
from SingleEnvironmentDialog import SingleEnvironmentDialog
from cairis.core.Borg import Borg

__author__ = 'Shamal Faily'

class EnvironmentListCtrl(DimensionListCtrl):
  def __init__(self,parent,winId,dp):
    DimensionListCtrl.__init__(self,parent,winId,wx.DefaultSize,'Environment','environment',dp,'Context of use',wx.LC_REPORT | wx.LC_SINGLE_SEL)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theInheritedEnvironment = ''
    self.theDimMenu.Append(ENVLIST_MENUNEWENVIRONMENT_ID,'New Environment')
    self.theDimMenu.Append(ENVLIST_MENUINHERITENVIRONMENT_ID,'Inherit Environment')
    wx.EVT_MENU(self.theDimMenu,ENVLIST_MENUNEWENVIRONMENT_ID,self.onNewEnvironment)
    wx.EVT_MENU(self.theDimMenu,ENVLIST_MENUINHERITENVIRONMENT_ID,self.onInheritEnvironment)

  def onNewEnvironment(self,evt):
    dlg = SingleEnvironmentDialog(self)
    if (dlg.ShowModal() == ENVIRONMENT_BUTTONCOMMIT_ID):
      self.dbProxy.addEnvironment(dlg.parameters())   
      idx = self.GetItemCount()
      self.InsertStringItem(idx,dlg.name())

  def onInheritEnvironment(self,evt):
    from DimensionNameDialog import DimensionNameDialog
    dimensions = self.dbProxy.getEnvironmentNames()
    dlg = DimensionNameDialog(self,'environment',dimensions,'Inherit from ')
    if (dlg.ShowModal() == DIMNAME_BUTTONACTION_ID):
      self.theInheritedEnvironment = dlg.dimensionName()
      adddlg = DimensionNameDialog(self,'environment',dimensions,'Add')
      if (adddlg.ShowModal() == DIMNAME_BUTTONACTION_ID):
        idx = self.GetItemCount()
        self.InsertStringItem(idx,adddlg.dimensionName())

  def inheritedEnvironment(self):
    return self.theInheritedEnvironment
