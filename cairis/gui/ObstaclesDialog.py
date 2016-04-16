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
import cairis.core.Obstacle
from ObstacleDialog import ObstacleDialog
from DialogClassParameters import DialogClassParameters
from cairis.core.ARM import *
from DimensionBaseDialog import DimensionBaseDialog

class ObstaclesDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,OBSTACLES_ID,'Obstacles',(930,300),'obstacle.png')
    idList = [OBSTACLES_OBSTACLELIST_ID,OBSTACLES_BUTTONADD_ID,OBSTACLES_BUTTONDELETE_ID]
    columnList = ['Name']
    self.buildControls(idList,columnList,self.dbProxy.getObstacles,'obstacle')
    listCtrl = self.FindWindowById(OBSTACLES_OBSTACLELIST_ID)
    listCtrl.SetColumnWidth(0,300)


  def addObjectRow(self,listCtrl,listRow,obstacle):
    listCtrl.InsertStringItem(listRow,obstacle.name())


  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters(OBSTACLE_ID,'Add obstacle',ObstacleDialog,OBSTACLE_BUTTONCOMMIT_ID,self.dbProxy.addObstacle,True)
      self.addObject(addParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add obstacle',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.selectedLabel]
    try:
      updateParameters = DialogClassParameters(OBSTACLE_ID,'Edit obstacle',ObstacleDialog,OBSTACLE_BUTTONCOMMIT_ID,self.dbProxy.updateObstacle,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit obstacle',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No obstacle','Delete obstacle',self.dbProxy.deleteObstacle)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete obstacle',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy
