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
import WidgetFactory
from Borg import Borg

class ExposedCountermeasurePanel(wx.Panel):
  def __init__(self,parent,exposedCMs):
    wx.Panel.__init__(self,parent,-1)
    b = Borg()
    self.dbProxy = b.dbProxy
    eValues = ['Low','Medium','High']
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    cmSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(cmSizer,1,wx.EXPAND)
    isFirst = True
    self.cmAssets = {}
    for envName,cmName,assetName,cmEffectiveness in exposedCMs:
      cmKey = envName + '/' + cmName + ' (' + assetName + ')'
      self.cmAssets[cmKey] = assetName
      ecBox = wx.StaticBox(self,-1,cmKey)
      ecBoxSizer = wx.StaticBoxSizer(ecBox,wx.HORIZONTAL)
      cmSizer.Add(ecBoxSizer,0,wx.EXPAND)
      for eValue in eValues:
        if (isFirst == True):
          rb = wx.RadioButton(self,-1,eValue,pos=wx.DefaultPosition,style=wx.RB_GROUP)
          isFirst = False
        else:
          rb = wx.RadioButton(self,-1,eValue)
        ecBoxSizer.Add(rb,0,wx.EXPAND)
        if (eValue == cmEffectiveness):
          rb.SetValue(True)
        else:
          rb.SetValue(False)
          isFirst = False
      isFirst = True
    mainSizer.Add(WidgetFactory.buildCommitButtonSizer(self,armid.EXPOSEDCOUNTERMEASURE_BUTTONCOMMIT_ID,True),0,wx.CENTER)
    self.SetSizer(mainSizer)

  def countermeasureEffectiveness(self):
    mainSizer = self.GetSizer()
    mainChildren = mainSizer.GetChildren()
    cmSizerItem = mainChildren[0]
    ceSizer = cmSizerItem.GetSizer()
    cmEffectivenessList = []
    for ceItem in ceSizer.GetChildren():
      rowSizer = ceItem.GetSizer()
      envCmName = rowSizer.GetStaticBox().GetLabel()
      assetName = self.cmAssets[envCmName]
      ecTxt = envCmName[0:envCmName.find('(')]
      envName,cmName = ecTxt.split('/')
      for colItem in rowSizer.GetChildren():
        rBox = colItem.GetWindow()
        if (rBox.GetValue() == True):
          cmEffectiveness = rBox.GetLabel()
      cmEffectivenessList.append((envName,cmName,assetName,cmEffectiveness))
    return cmEffectivenessList
