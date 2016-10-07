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
from PropertiesListCtrl import PropertiesListCtrl
from AssetAssociationListCtrl import AssetAssociationListCtrl

__author__ = 'Shamal Faily'

class PropertiesPage(wx.Panel):
  def __init__(self,parent,dp):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)
    pBox = wx.StaticBox(self,-1)
    pBoxSizer = wx.StaticBoxSizer(pBox,wx.HORIZONTAL)
    topSizer.Add(pBoxSizer,1,wx.EXPAND)
    values = ['None','Low','Medium','High']
    valueLookup = ValueDictionary(values)
    self.propertiesList = PropertiesListCtrl(self,ASSETENVIRONMENT_LISTPROPERTIES_ID,valueLookup)
    pBoxSizer.Add(self.propertiesList,1,wx.EXPAND)

    self.SetSizer(topSizer)

class AssociationsPage(wx.Panel):
  def __init__(self,parent,winId,dp,pp):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    asBox = wx.StaticBox(self,-1)
    asBoxSizer = wx.StaticBoxSizer(asBox,wx.HORIZONTAL)
    topSizer.Add(asBoxSizer,1,wx.EXPAND)
    self.associationList = AssetAssociationListCtrl(self,winId,dp,pp.propertiesList)
    asBoxSizer.Add(self.associationList,1,wx.EXPAND)
    self.SetSizer(topSizer)


class AssetEnvironmentNotebook(wx.Notebook):
  def __init__(self,parent,dp):
    wx.Notebook.__init__(self,parent,ASSET_NOTEBOOKENVIRONMENT_ID)
    p1 = PropertiesPage(self,dp)
    p2 = AssociationsPage(self,ASSET_LISTASSOCIATIONS_ID,dp,p1)
    self.AddPage(p1,'Properties')
    self.AddPage(p2,'Associations')
