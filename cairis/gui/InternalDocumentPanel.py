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
import cairis.core.InternalDocument
from InternalDocumentNotebook import InternalDocumentNotebook

__author__ = 'Shamal Faily'

class InternalDocumentPanel(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,EXTERNALDOCUMENT_ID)
    self.theId = None
    
  def buildControls(self,isCreate,isUpdateable=True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)

    nb = InternalDocumentNotebook(self)
    mainSizer.Add(nb,1,wx.EXPAND)
    mainSizer.Add(self.buildCommitButtonSizer(INTERNALDOCUMENT_BUTTONCOMMIT_ID,isCreate),0,wx.CENTER)
    self.SetSizer(mainSizer)

  def loadControls(self,objt,isReadOnly=False):
    self.theId = objt.id()
    nameCtrl = self.FindWindowById(INTERNALDOCUMENT_TEXTNAME_ID)
    descCtrl = self.FindWindowById(INTERNALDOCUMENT_TEXTDESCRIPTION_ID)
    contCtrl = self.FindWindowById(INTERNALDOCUMENT_TEXTCONTENT_ID)

    nameCtrl.SetValue(objt.name())
    descCtrl.SetValue(objt.description())
    contCtrl.SetValue(objt.content())
    contCtrl.setCodes(objt.codes())
    contCtrl.setMemos(objt.memos())
