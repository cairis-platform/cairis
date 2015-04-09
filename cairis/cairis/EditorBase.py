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
import os
import armid
from Borg import Borg

class EditorBase(wx.Panel):
  def __init__(self,parent,id):
    wx.Panel.__init__(self,parent,id,size=(1150,400))
    self.theCurrentEnvironment = -1
    b = Borg()
    self.dbProxy = b.dbProxy
    directoryPrefix = b.imageDir + '/'
    contextModelBmp = wx.Image(directoryPrefix + 'contextModel.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    environmentModelBmp = wx.Image(directoryPrefix + 'environmentModel.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    assetModelBmp = wx.Image(directoryPrefix + 'classModel.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    goalModelBmp = wx.Image(directoryPrefix + 'goalModel.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    obstacleModelBmp = wx.Image(directoryPrefix + 'obstacleModel.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    responsibilityModelBmp = wx.Image(directoryPrefix + 'responsibilityModel.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    taskModelBmp = wx.Image(directoryPrefix + 'taskModel.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    apModelBmp = wx.Image(directoryPrefix + 'apModel.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    atModelBmp = wx.Image(directoryPrefix + 'atModel.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    classAssociationsBmp = wx.Image(directoryPrefix + 'classassociation.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    dependenciesBmp = wx.Image(directoryPrefix + 'dependencyassociation.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    goalAssociationsBmp = wx.Image(directoryPrefix + 'goalassociation.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    cmModelBmp = wx.Image(directoryPrefix + 'conceptMapModel.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    componentModelBmp = wx.Image(directoryPrefix + 'component_view.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()

    self.visToolbar = wx.ToolBar(self,style=wx.TB_HORIZONTAL | wx.TB_DOCKABLE)
    self.visToolbar.AddSimpleTool(armid.RMFRAME_TOOL_DEPENDENCIES,dependenciesBmp,'Edit Dependencies')
    self.visToolbar.AddSimpleTool(armid.RMFRAME_TOOL_GOALASSOCIATIONS,goalAssociationsBmp,'Edit Goal Associations')
    self.visToolbar.AddSimpleTool(armid.RMFRAME_TOOL_CLASSASSOCIATIONS,classAssociationsBmp,'Edit Asset Associations')
    self.visToolbar.AddSeparator()
    self.visToolbar.AddSimpleTool(armid.RMFRAME_TOOL_ENVIRONMENTMODEL,environmentModelBmp,'View Risk Analysis Model')
    self.visToolbar.AddSimpleTool(armid.RMFRAME_TOOL_GOALMODEL,goalModelBmp,'View Goal Model')
    self.visToolbar.AddSimpleTool(armid.RMFRAME_TOOL_OBSTACLEMODEL,obstacleModelBmp,'View Obstacle Model')
    self.visToolbar.AddSimpleTool(armid.RMFRAME_TOOL_RESPONSIBILITYMODEL,responsibilityModelBmp,'View Responsibility Model')
    self.visToolbar.AddSimpleTool(armid.RMFRAME_TOOL_ASSETMODEL,assetModelBmp,'View Asset Model')
    self.visToolbar.AddSimpleTool(armid.RMFRAME_TOOL_TASKMODEL,taskModelBmp,'View Task Model')
    self.visToolbar.AddSimpleTool(armid.RMFRAME_TOOL_APMODEL,apModelBmp,'View Assumption Persona Model')
    self.visToolbar.AddSimpleTool(armid.RMFRAME_TOOL_ATMODEL,atModelBmp,'View Assumption Task Model')
    self.visToolbar.AddSimpleTool(armid.RMFRAME_TOOL_CMMODEL,cmModelBmp,'View Concept Map Model')
    self.visToolbar.AddSimpleTool(armid.RMFRAME_TOOL_COMPONENTMODEL,componentModelBmp,'View Component Model')

    self.visToolbar.Realize()

    self.sizer = wx.BoxSizer(wx.VERTICAL)
    reqMods = ['']
    reqMods += self.dbProxy.getDimensionNames(self.objectDimension)
    reqMods.sort()
    envMods = [''] + self.dbProxy.getDimensionNames('environment')
    envMods.sort()
    filterSizer = wx.BoxSizer(wx.HORIZONTAL)
    self.sizer.Add(filterSizer,0,wx.EXPAND)

    modBox = wx.StaticBox(self,-1,self.objectLabel)
    modSizer = wx.StaticBoxSizer(modBox,wx.HORIZONTAL)
    if len(reqMods) == 0:
      self.modCombo = wx.ComboBox(self,armid.RMFRAME_TOOL_COMBOOBJECT,'',choices=[],size=(200,-1),style=wx.CB_DROPDOWN)
    else:
      self.modCombo = wx.ComboBox(self,armid.RMFRAME_TOOL_COMBOOBJECT,reqMods[0],choices=reqMods,size=(200,-1),style=wx.CB_DROPDOWN)
    modSizer.Add(self.modCombo,0,wx.EXPAND)
    filterSizer.Add(modSizer,0,wx.ALL | wx.ALIGN_LEFT,4)

    envBox = wx.StaticBox(self,-1,'Environments')
    envSizer = wx.StaticBoxSizer(envBox,wx.HORIZONTAL)
    if len(envMods) == 0:
      self.envCombo = wx.ComboBox(self,armid.RMFRAME_TOOL_COMBOENVIRONMENT,'',choices=[],size=(200,-1),style=wx.CB_DROPDOWN)
    else:
      self.envCombo = wx.ComboBox(self,armid.RMFRAME_TOOL_COMBOENVIRONMENT,envMods[0],choices=envMods,size=(200,-1),style=wx.CB_DROPDOWN)
    envSizer.Add(self.envCombo,0,wx.EXPAND)
    filterSizer.Add(envSizer,0,wx.ALL | wx.ALIGN_LEFT,4)
    filterSizer.Add(self.visToolbar,0,wx.ALL | wx.ALIGN_LEFT,4)
    
    filteredReqMods = filter(None, reqMods)
    filteredEnvMods = filter(None, envMods)
    if len(filteredReqMods) > 0:
      self.modCombo.SetStringSelection(filteredReqMods[0])
    else:
      if len(filteredEnvMods) > 0:
        self.envCombo.SetStringSelection(filteredEnvMods[0])

  def reload(self):
    self.grid.reload()
    self.resizeColumns()

  def refresh(self):
    self.grid.reloadView()
    self.resizeColumns()

  def updateObjectSelection(self,selectedObject = ''):
    self.modCombo.Clear()
    p = self.dbProxy
    goalMods = p.getDimensionNames(self.objectDimension)
    goalMods.sort()
    self.modCombo.SetItems(goalMods)
    if (selectedObject == ''):
      self.modCombo.SetSelection(0)
      self.envCombo.SetValue('')
    else:
      self.modCombo.SetStringSelection(selectedObject)
      self.envCombo.SetValue('')
      self.refresh()

  def updateEnvironmentSelection(self,selectedEnvironment = ''):
    self.envCombo.Clear()
    p = self.dbProxy
    envMods = p.getDimensionNames('environment')
    envMods.sort()
    self.envCombo.SetItems(envMods)
    if (selectedEnvironment == ''):
      self.envCombo.SetSelection(0)
      self.modCombo.SetValue('')
    else:
      self.envCombo.SetStringSelection(selectedEnvironment)
      self.modCombo.SetValue('')
      self.refresh()

  def selectedObject(self):
    return self.modCombo.GetValue()

