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
import WidgetFactory
from cairis.core.Borg import Borg
from numpy import *
from cairis.core.ResponseParameters import ResponseParameters

class TransferPanel(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,RESPONSE_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theDescription = ''
    self.theCommitVerb = 'Create'
    self.theRisks = []

  def buildControls(self,isCreate,isUpdateable = True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(WidgetFactory.buildDimensionListSizer(self,'Risks',(100,82),RESPONSE_LISTRISKS_ID,'risk',self.dbProxy),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildMLTextSizer(self,'Description',(87,60),RESPONSE_TEXTDESCRIPTION_ID),1,wx.EXPAND)
    self.SetSizer(mainSizer)

  def loadControls(self,response,isReadOnly = False):
    risksCtrl = self.FindWindowById(RESPONSE_LISTRISKS_ID)
    descriptionCtrl = self.FindWindowById(RESPONSE_TEXTDESCRIPTION_ID)
    
    risksCtrl.Set(response.risks())
    descriptionCtrl.SetValue(response.description())
    if (isReadOnly):
      rationaleCtrl.Disable()
      risksCtrl.Disable()
    self.theCommitVerb = 'Edit'

  def commit(self):
    risksCtrl = self.FindWindowById(RESPONSE_LISTRISKS_ID)
    descriptionCtrl = self.FindWindowById(RESPONSE_TEXTDESCRIPTION_ID)

    commitLabel = self.theCommitVerb + ' transfer'

    self.theDescription = descriptionCtrl.GetValue()

    if (risksCtrl.GetCount() == 0):
      dlg = wx.MessageDialog(self,'At least one risk needs to be accepted',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return -1
    elif (len(self.theDescription) == 0):
      dlg = wx.MessageDialog(self,'No transfer description',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return -1
    else:
      for x in range(risksCtrl.GetCount()):
        riskName = risksCtrl.GetString(x)
        self.theRisks.append(riskName)
      return 0


  def parameters(self,responseName,responseCost,responseRoles):
   responseType = 'Transfer'
   responseProperties =  array((0,0,0,3,0,0,0,0))
   detectionPoint = 'none'
   detectionMechanism = -1
   targets = []
   return ResponseParameters(responseName,responseType,self.theDescription,responseCost,responseProperties,detectionPoint,detectionMechanism,self.theRisks,targets,responseRoles)
