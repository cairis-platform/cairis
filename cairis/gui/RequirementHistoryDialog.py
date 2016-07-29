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

__author__ = 'Shamal Faily'

class RequirementHistoryDialog(wx.Dialog):
  def __init__(self,parent,history):
    wx.Dialog.__init__(self,parent,REQUIREMENTHISTORY_ID,'Requirement History',style=wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.RESIZE_BORDER|wx.MAXIMIZE_BOX,size=(1000,300))
    self.theId = -1
    self.panel = wx.Panel(self,-1)
    panelSizer = wx.BoxSizer(wx.VERTICAL)
    reqList = wx.ListCtrl(self,-1,style=wx.LC_REPORT)
    reqList.InsertColumn(0,'Version')
    reqList.SetColumnWidth(0,50)
    reqList.InsertColumn(1,'Label')
    reqList.SetColumnWidth(1,50)
    reqList.InsertColumn(2,'Name')
    reqList.SetColumnWidth(2,75)
    reqList.InsertColumn(3,'Description')
    reqList.SetColumnWidth(3,150)
    reqList.InsertColumn(4,'Priority')
    reqList.SetColumnWidth(4,50)
    reqList.InsertColumn(5,'Rationale')
    reqList.SetColumnWidth(5,150)
    reqList.InsertColumn(6,'Fit Criterion')
    reqList.SetColumnWidth(6,150)
    reqList.InsertColumn(7,'Originator')
    reqList.SetColumnWidth(7,100)
    reqList.InsertColumn(8,'Type')
    reqList.SetColumnWidth(8,100)
    reqList.InsertColumn(9,'Rev. Date')
    reqList.SetColumnWidth(9,150)
 
    for version,label,name,desc,priority,rationale,fitCriterion,originator,reqType,revDate in history:
      idx = reqList.GetItemCount()
      reqList.InsertStringItem(idx,str(version))
      reqList.SetStringItem(idx,1,str(label))
      reqList.SetStringItem(idx,2,name)
      reqList.SetStringItem(idx,3,desc)
      reqList.SetStringItem(idx,4,str(priority))
      reqList.SetStringItem(idx,5,rationale)
      reqList.SetStringItem(idx,6,fitCriterion)
      reqList.SetStringItem(idx,7,originator)
      reqList.SetStringItem(idx,8,reqType)
      reqList.SetStringItem(idx,9,revDate)

    panelSizer.Add(reqList,1,wx.EXPAND)
    self.panel.SetSizer(panelSizer)
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
