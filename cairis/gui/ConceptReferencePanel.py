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
import cairis.core.ConceptReference
from cairis.core.Borg import Borg

__author__ = 'Shamal Faily'

class ConceptReferencePanel(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,CONCEPTREFERENCE_ID)
    self.theId = None
    b = Borg()
    self.dbProxy = b.dbProxy
    
  def buildControls(self,isCreate,isUpdateable=True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(self.buildTextSizer('Name',(87,30),CONCEPTREFERENCE_TEXTNAME_ID),0,wx.EXPAND)

    dims = ['asset','attacker','countermeasure','domainproperty','environment','goal','misusecase','obstacle','persona','requirement','response','risk','role','task','threat','vulnerability']
    mainSizer.Add(self.buildComboSizerList('Concept',(87,30),CONCEPTREFERENCE_COMBODIMNAME_ID,dims),0,wx.EXPAND)
    mainSizer.Add(self.buildComboSizerList('Object',(87,30),CONCEPTREFERENCE_COMBOOBJTNAME_ID,[]),0,wx.EXPAND)
    mainSizer.Add(self.buildMLTextSizer('Description',(87,30),CONCEPTREFERENCE_TEXTDESCRIPTION_ID),1,wx.EXPAND)
    mainSizer.Add(self.buildCommitButtonSizer(CONCEPTREFERENCE_BUTTONCOMMIT_ID,isCreate),0,wx.CENTER)
    wx.EVT_COMBOBOX(self,CONCEPTREFERENCE_COMBODIMNAME_ID,self.onDimensionChange)
    self.SetSizer(mainSizer)

  def loadControls(self,objt,isReadOnly=False):
    self.theId = objt.id()
    nameCtrl = self.FindWindowById(CONCEPTREFERENCE_TEXTNAME_ID)
    dimCtrl = self.FindWindowById(CONCEPTREFERENCE_COMBODIMNAME_ID)
    objtCtrl = self.FindWindowById(CONCEPTREFERENCE_COMBOOBJTNAME_ID)
    descCtrl = self.FindWindowById(CONCEPTREFERENCE_TEXTDESCRIPTION_ID)

    nameCtrl.SetValue(objt.name())
    dimCtrl.SetValue(objt.dimension())
    objtCtrl.SetValue(objt.objectName())
    descCtrl.SetValue(objt.description())

  def onDimensionChange(self,evt):
    dimName = evt.GetString()
    objts = self.dbProxy.getDimensionNames(dimName)
    objtCtrl = self.FindWindowById(CONCEPTREFERENCE_COMBOOBJTNAME_ID)
    objtCtrl.SetItems(objts)
