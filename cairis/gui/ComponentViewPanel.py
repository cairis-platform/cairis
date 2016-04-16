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
from BasePanel import BasePanel
import cairis.core.ComponentView
from cairis.core.Borg import Borg
from ComponentViewNotebook import ComponentViewNotebook

class ComponentViewPanel(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,COMPONENTVIEW_ID)
    self.theComponentId = None
    b = Borg()
    self.dbProxy = b.dbProxy
    
  def buildControls(self,isCreate,isUpdateable=True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(self.buildTextSizer('Name',(87,30),COMPONENTVIEW_TEXTNAME_ID),0,wx.EXPAND)

    nbBox = wx.StaticBox(self,-1)
    nbSizer = wx.StaticBoxSizer(nbBox,wx.VERTICAL)
    mainSizer.Add(nbSizer,1,wx.EXPAND)
    nbSizer.Add(ComponentViewNotebook(self),1,wx.EXPAND)

    mainSizer.Add(self.buildCommitButtonSizer(COMPONENTVIEW_BUTTONCOMMIT_ID,isCreate),0,wx.CENTER)
    self.SetSizer(mainSizer)

  def loadControls(self,cv,isReadOnly=False):
    self.theComponentId = cv.id()
    nbCtrl = self.FindWindowById(COMPONENTVIEW_NOTEBOOKCOMPONENTVIEW_ID)
    nameCtrl = self.FindWindowById(COMPONENTVIEW_TEXTNAME_ID)
    synCtrl = self.FindWindowById(COMPONENTVIEW_TEXTSYNOPSIS_ID)
    comCtrl = self.FindWindowById(COMPONENTVIEW_LISTCOMPONENTS_ID)
    conCtrl = self.FindWindowById(COMPONENTVIEW_LISTCONNECTORS_ID)

    nbCtrl.setView(cv.name())
    nameCtrl.SetValue(cv.name())
    synCtrl.SetValue(cv.synopsis())
    comCtrl.load(cv.components())
    conCtrl.load(cv.connectors())
