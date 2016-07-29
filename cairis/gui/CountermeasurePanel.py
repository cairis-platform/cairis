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
from cairis.core.ARM import *
from cairis.core.armid import *
from BasePanel import BasePanel
from cairis.core.Borg import Borg
from cairis.core.CountermeasureParameters import CountermeasureParameters
from CountermeasureEnvironmentPanel import CountermeasureEnvironmentPanel

__author__ = 'Shamal Faily'

class CountermeasurePanel(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,COUNTERMEASURE_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theCountermeasureName = ''
    self.theTags = []
    self.theCountermeasureDescription = ''
    self.theCountermeasureType = ''
    self.theCommitVerb = 'Create'
    self.environmentPanel = CountermeasureEnvironmentPanel(self,self.dbProxy)
    self.theEnvironmentProperties = []

  def buildControls(self,isCreate,isUpdateable = True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(self.buildTextSizer('Name',(87,60),COUNTERMEASURE_TEXTNAME_ID),0,wx.EXPAND)
    mainSizer.Add(self.buildTagCtrlSizer((87,30),COUNTERMEASURE_TAGS_ID),0,wx.EXPAND)
    typeList = ['Information','Systems','Software','Hardware','People']
    mainSizer.Add(self.buildComboSizerList('Type',(87,30),COUNTERMEASURE_COMBOTYPE_ID,typeList),0,wx.EXPAND)
    mainSizer.Add(self.buildMLTextSizer('Description',(87,60),COUNTERMEASURE_TEXTDESCRIPTION_ID),0,wx.EXPAND)
    mainSizer.Add(self.environmentPanel,1,wx.EXPAND)
    mainSizer.Add(self.buildCommitButtonSizer(COUNTERMEASURE_BUTTONCOMMIT_ID,isCreate),0,wx.CENTER)
    self.SetSizer(mainSizer)

  def loadControls(self,countermeasure,isReadOnly = False):
    nameCtrl = self.FindWindowById(COUNTERMEASURE_TEXTNAME_ID)
    tagsCtrl = self.FindWindowById(COUNTERMEASURE_TAGS_ID)
    tagsCtrl.set(countermeasure.tags())

    descriptionCtrl = self.FindWindowById(COUNTERMEASURE_TEXTDESCRIPTION_ID)
    nameCtrl.SetValue(countermeasure.name())
    descriptionCtrl.SetValue(countermeasure.description())
    typeCtrl = self.FindWindowById(COUNTERMEASURE_COMBOTYPE_ID)
    typeCtrl.SetValue(countermeasure.type())

    self.environmentPanel.loadControls(countermeasure)
    self.theCommitVerb = 'Edit'

  def commit(self):
    commitLabel = self.theCommitVerb + ' countermeasure'
    nameCtrl = self.FindWindowById(COUNTERMEASURE_TEXTNAME_ID)
    tagsCtrl = self.FindWindowById(COUNTERMEASURE_TAGS_ID)
    self.theTags = tagsCtrl.tags()
    descriptionCtrl = self.FindWindowById(COUNTERMEASURE_TEXTDESCRIPTION_ID)
    typeCtrl = self.FindWindowById(COUNTERMEASURE_COMBOTYPE_ID)
    self.theCountermeasureName = nameCtrl.GetValue()
    if (self.theCommitVerb == 'Create'):
      b = Borg()
      try:
        b.dbProxy.nameCheck(self.theCountermeasureName,'countermeasure')
      except ARMException,errorText:
        dlg = wx.MessageDialog(self,str(errorText),'Add countermeasure',wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
        return

    self.theCountermeasureType = typeCtrl.GetValue()
    self.theCountermeasureDescription = descriptionCtrl.GetValue()
    try:
      self.theEnvironmentProperties = self.environmentPanel.environmentProperties()
    except EnvironmentValidationError, errorText:
      dlg = wx.MessageDialog(self,str(errorText),commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return -1
    
    commitLabel = self.theCommitVerb + ' countermeasure'

    if (len(self.theCountermeasureName) == 0):
      dlg = wx.MessageDialog(self,'No name entered',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return -1
    elif (len(self.theCountermeasureType) == 0):
      dlg = wx.MessageDialog(self,'No name selected',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return -1
    elif (len(self.theCountermeasureDescription) == 0):
      dlg = wx.MessageDialog(self,'No description entered',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return -1
    elif (len(self.theEnvironmentProperties) == 0):
      dlg = wx.MessageDialog(self,'No environment specific properties set',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return -1
    else:
      return 0

  def parameters(self):
    return CountermeasureParameters(self.theCountermeasureName,self.theCountermeasureDescription,self.theCountermeasureType,self.theTags,self.theEnvironmentProperties)
