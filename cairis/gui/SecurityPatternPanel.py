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
import cairis.core.SecurityPattern
from cairis.core.Borg import Borg
from SecurityPatternNotebook import SecurityPatternNotebook

class SecurityPatternPanel(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,SECURITYPATTERN_ID)
    self.thePatternId = None
    b = Borg()
    self.dbProxy = b.dbProxy
    
  def buildControls(self,isCreate,isUpdateable=True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(self.buildTextSizer('Name',(87,30),SECURITYPATTERN_TEXTNAME_ID),0,wx.EXPAND)

    nbBox = wx.StaticBox(self,-1)
    nbSizer = wx.StaticBoxSizer(nbBox,wx.VERTICAL)
    mainSizer.Add(nbSizer,1,wx.EXPAND)
    nbSizer.Add(SecurityPatternNotebook(self),1,wx.EXPAND)

    mainSizer.Add(self.buildCommitButtonSizer(SECURITYPATTERN_BUTTONCOMMIT_ID,isCreate),0,wx.CENTER)
    self.SetSizer(mainSizer)

  def loadControls(self,pattern,isReadOnly=False):
    self.thePatternId = pattern.id()
    nameCtrl = self.FindWindowById(SECURITYPATTERN_TEXTNAME_ID)
    contextCtrl = self.FindWindowById(SECURITYPATTERN_TEXTCONTEXT_ID)
    problemCtrl = self.FindWindowById(SECURITYPATTERN_TEXTPROBLEM_ID)
    solutionCtrl = self.FindWindowById(SECURITYPATTERN_TEXTSOLUTION_ID)
    concernsCtrl = self.FindWindowById(SECURITYPATTERN_LISTPATTERNSTRUCTURE_ID)
    reqsCtrl = self.FindWindowById(SECURITYPATTERN_LISTREQUIREMENTS_ID)

    nameCtrl.SetValue(pattern.name())
    contextCtrl.SetValue(pattern.context())
    problemCtrl.SetValue(pattern.problem())
    solutionCtrl.SetValue(pattern.solution())
    concernsCtrl.load(pattern.associations())
    reqsCtrl.load(pattern.requirements()) 
