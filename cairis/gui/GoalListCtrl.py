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
import GoalRequirementFactory
from cairis.core.Borg import Borg
from DimensionNameDialog import DimensionNameDialog
from cairis.core.ARM import *

__author__ = 'Shamal Faily'

class GoalListCtrl(wx.ListCtrl):

  def __init__(self,parent,winId):
    wx.ListCtrl.__init__(self,parent,winId,style=wx.LC_REPORT)
    self.theParentDialog = parent
    self.theTraceMenu = wx.Menu()
    self.theTraceMenu.Append(TRACE_MENUTRACE_GENERATESPECIFIC_ID,'Generate Requirement')
    self.theRequirementGrid = parent.theMainWindow.requirementGrid()
    wx.EVT_MENU(self,TRACE_MENUTRACE_GENERATESPECIFIC_ID,self.onSelectGenerate)
    self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onRightClick)


  def onRightClick(self,evt):
    self.PopupMenu(self.theTraceMenu)

  def onSelectGenerate(self,evt):
    objt = self.theParentDialog.objts[self.theParentDialog.selectedLabel]
#    objtId = objt.id()
    try:
      b = Borg()
      dbProxy = b.dbProxy
      domains = dbProxy.getDimensionNames('domain',False)
      cDlg = DimensionNameDialog(self,'domain',domains,'Select')
      if (cDlg.ShowModal() == DIMNAME_BUTTONACTION_ID):
        domainName = cDlg.dimensionName()
        GoalRequirementFactory.build(objt,domainName,self.theParentDialog.theMainWindow)
# Change domain in panel
# Add requirement
# add goalrequirement_goalassociation
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Generate goal requirement',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return
