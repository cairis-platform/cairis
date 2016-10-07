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
from ValueDictionary import ValueDictionary
from DimensionListCtrl import DimensionListCtrl
from TargetListCtrl import TargetListCtrl
from PropertiesListCtrl import PropertiesListCtrl
from CountermeasureTaskPersonaListCtrl import CountermeasureTaskPersonaListCtrl
from CountermeasureRoleListCtrl import CountermeasureRoleListCtrl

__author__ = 'Shamal Faily'

class SecurityPage(wx.Panel):
  def __init__(self,parent,dp):
    wx.Panel.__init__(self,parent)
    self.dbProxy = dp
    topSizer = wx.BoxSizer(wx.VERTICAL)

    targetSizer = wx.BoxSizer(wx.HORIZONTAL)
    topSizer.Add(targetSizer,1,wx.EXPAND)

    reqBox = wx.StaticBox(self,-1)
    reqBoxSizer = wx.StaticBoxSizer(reqBox,wx.HORIZONTAL)
    targetSizer.Add(reqBoxSizer,1,wx.EXPAND)
    self.reqList = DimensionListCtrl(self,COUNTERMEASURE_LISTREQUIREMENTS_ID,wx.DefaultSize,'Requirement','requirement',self.dbProxy,listStyle=wx.LC_REPORT | wx.LC_SINGLE_SEL)
    reqBoxSizer.Add(self.reqList,1,wx.EXPAND)

    targetBox = wx.StaticBox(self,-1)
    targetBoxSizer = wx.StaticBoxSizer(targetBox,wx.HORIZONTAL)
    targetSizer.Add(targetBoxSizer,1,wx.HORIZONTAL | wx.EXPAND)
    self.targetList = TargetListCtrl(self,COUNTERMEASURE_LISTTARGETS_ID)
    targetBoxSizer.Add(self.targetList,1,wx.EXPAND)

    propertiesBox = wx.StaticBox(self,-1)
    propertiesBoxSizer = wx.StaticBoxSizer(propertiesBox,wx.HORIZONTAL)
    topSizer.Add(propertiesBoxSizer,1,wx.EXPAND)
    values = self.dbProxy.getDimensionNames('countermeasure_value')
    valueLookup = ValueDictionary(values)
    self.propertiesList = PropertiesListCtrl(self,COUNTERMEASURE_LISTPROPERTIES_ID,valueLookup)
    propertiesBoxSizer.Add(self.propertiesList,1,wx.EXPAND)

    self.SetSizer(topSizer)

class UsabilityPage(wx.Panel):
  def __init__(self,parent,dp):
    wx.Panel.__init__(self,parent)
    self.dbProxy = dp
    topSizer = wx.BoxSizer(wx.VERTICAL)

    roleBox = wx.StaticBox(self,-1)
    roleBoxSizer = wx.StaticBoxSizer(roleBox,wx.HORIZONTAL)
    topSizer.Add(roleBoxSizer,0,wx.EXPAND)
    self.personaList = CountermeasureTaskPersonaListCtrl(self,COUNTERMEASURE_LISTPERSONAS_ID,self.dbProxy)
    self.roleList = CountermeasureRoleListCtrl(self,self.dbProxy,self.personaList)
    roleBoxSizer.Add(self.roleList,1,wx.EXPAND)

    personaBox = wx.StaticBox(self,-1)
    personaBoxSizer = wx.StaticBoxSizer(personaBox,wx.HORIZONTAL)
    topSizer.Add(personaBoxSizer,1,wx.EXPAND)
    personaBoxSizer.Add(self.personaList,1,wx.EXPAND)

    self.SetSizer(topSizer)

class CountermeasureEnvironmentNotebook(wx.Notebook):
  def __init__(self,parent,dp):
    wx.Notebook.__init__(self,parent,TASK_NOTEBOOKENVIRONMENT_ID)
    p1 = SecurityPage(self,dp)
    p2 = UsabilityPage(self,dp)
    self.AddPage(p1,'Security')
    self.AddPage(p2,'Usability')
