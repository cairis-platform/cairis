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
from cairis.core.Borg import Borg

__author__ = 'Shamal Faily'

class SecurityPatternEnvironmentPanel(wx.Panel):
  def __init__(self,parent,patternId,cmEnvs = []):
    wx.Panel.__init__(self,parent,-1)
    b = Borg()
    self.dbProxy = b.dbProxy
    
    if (len(cmEnvs) == 0):
      self.envs = self.dbProxy.getEnvironmentNames()
    else:
      self.envs = cmEnvs
    self.patternAssets = self.dbProxy.patternAssets(patternId)

    mainSizer = wx.BoxSizer(wx.VERTICAL)
    assetSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(assetSizer,1,wx.EXPAND)
    for assetName in self.patternAssets:
      aBox = wx.StaticBox(self,-1,assetName)
      aBoxSizer = wx.StaticBoxSizer(aBox,wx.HORIZONTAL)
      assetSizer.Add(aBoxSizer,0,wx.EXPAND)
      for envName in self.envs:
        cb = wx.CheckBox(self,-1,envName)
        aBoxSizer.Add(cb,0,wx.EXPAND)
      
    buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
    buttonSizer.Add(wx.Button(self,SPENVIRONMENT_BUTTONCOMMIT_ID))
    buttonSizer.Add(wx.Button(parent,wx.ID_CANCEL,"Close"))
    mainSizer.Add(buttonSizer,0,wx.CENTER)
    self.SetSizer(mainSizer)

  def assetEnvironments(self):
    mainSizer = self.GetSizer()
    mainChildren = mainSizer.GetChildren()
    assetSizerItem = mainChildren[0]
    assetSizer = assetSizerItem.GetSizer()
    assetEnvs = {}
    for aItem in assetSizer.GetChildren():
      rowSizer = aItem.GetSizer()
      assetName = rowSizer.GetStaticBox().GetLabel()
      envs = []
      for colItem in rowSizer.GetChildren():
        checkBox = colItem.GetWindow()
        if (checkBox.GetValue() == True):
          envs.append(checkBox.GetLabel())
      assetEnvs[assetName] = envs
    return assetEnvs
