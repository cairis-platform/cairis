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

class CountermeasureTaskListCtrl(wx.ListCtrl):
  def __init__(self,parent,dp):
    wx.ListCtrl.__init__(self,parent,COUNTERMEASURE_LISTTASKS_ID,size=wx.DefaultSize,style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
    self.dbProxy = dp
    self.theCurrentEnvironment = ''
    self.InsertColumn(0,'Task')
    self.SetColumnWidth(0,150)

  def setEnvironment(self,environmentName):
    self.theCurrentEnvironment = environmentName

  def load(self,dims):
    self.DeleteAllItems()
    for idx,dim in enumerate(dims):
      self.InsertStringItem(idx,str(dim))

  def dimensions(self):
    dimList = []
    for x in range(self.GetItemCount()):
      dimList.append(self.GetItemText(x))
    return dimList
