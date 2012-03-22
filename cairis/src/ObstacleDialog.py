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
import ARM
from ObstaclePanel import ObstaclePanel
from ObstacleParameters import ObstacleParameters
from Borg import Borg
import DialogClassParameters

class ObstacleDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,parameters.id(),parameters.label(),style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(600,400))
    self.theObstacleId = -1
    self.theObstacleName = ''
    self.theObstacleOriginator = ''
    self.theEnvironmentProperties = []
    self.panel = 0
    self.buildControls(parameters)
    self.commitVerb = 'Add'
    
  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = ObstaclePanel(self)
    self.panel.buildControls(parameters.createFlag())
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.OBSTACLE_BUTTONCOMMIT_ID,self.onCommit)

  def load(self,obstacle):
    self.theObstacleId = obstacle.id()
    self.panel.loadControls(obstacle)
    self.commitVerb = 'Edit'

  def onCommit(self,evt):
    nameCtrl = self.FindWindowById(armid.OBSTACLE_TEXTNAME_ID)
    origCtrl = self.FindWindowById(armid.OBSTACLE_TEXTORIGINATOR_ID)
    environmentCtrl = self.FindWindowById(armid.OBSTACLE_PANELENVIRONMENT_ID)

    self.theObstacleName = nameCtrl.GetValue()
    self.theObstacleOriginator = origCtrl.GetValue()
    if (self.commitVerb == 'Add'):
      b = Borg()
      try:
        b.dbProxy.nameCheck(self.theObstacleName,'obstacle')
      except ARM.ARMException,errorText:
        dlg = wx.MessageDialog(self,str(errorText),'Add obstacle',wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
        return

    self.theEnvironmentProperties = environmentCtrl.environmentProperties()

    commitLabel = self.commitVerb + ' obstacle'
    if len(self.theObstacleName) == 0:
      dlg = wx.MessageDialog(self,'Obstacle name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif len(self.theObstacleOriginator) == 0:
      dlg = wx.MessageDialog(self,'Obstacle originator cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theEnvironmentProperties) == 0):
      dlg = wx.MessageDialog(self,'No environments have been associated with this obstacle',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      for environmentProperties in self.theEnvironmentProperties:
        if len(environmentProperties.category()) == 0:
          errorTxt = 'No category associated with environment ' + environmentProperties.name()
          dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK)
          dlg.ShowModal()
          dlg.Destroy()
          return
        if len(environmentProperties.definition()) == 0:
          errorTxt = 'No definition associated with environment ' + environmentProperties.name()
          dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK)
          dlg.ShowModal()
          dlg.Destroy()
          return
      self.EndModal(armid.OBSTACLE_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = ObstacleParameters(self.theObstacleName,self.theObstacleOriginator,self.theEnvironmentProperties)
    parameters.setId(self.theObstacleId)
    return parameters
