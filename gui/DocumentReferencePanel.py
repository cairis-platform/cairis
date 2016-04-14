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
from BasePanel import BasePanel
import DocumentReference
from Borg import Borg

class DocumentReferencePanel(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,armid.DOCUMENTREFERENCE_ID)
    self.theId = None
    b = Borg()
    self.dbProxy = b.dbProxy
    
  def buildControls(self,isCreate,isUpdateable=True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(self.buildTextSizer('Name',(87,30),armid.DOCUMENTREFERENCE_TEXTNAME_ID),0,wx.EXPAND)

    docs = self.dbProxy.getDimensionNames('external_document')
    mainSizer.Add(self.buildComboSizerList('Document',(87,30),armid.DOCUMENTREFERENCE_COMBODOCNAME_ID,docs),0,wx.EXPAND)

    mainSizer.Add(self.buildTextSizer('Contributor',(87,30),armid.DOCUMENTREFERENCE_TEXTCONTRIBUTOR_ID),0,wx.EXPAND)

    mainSizer.Add(self.buildMLTextSizer('Excerpt',(87,30),armid.DOCUMENTREFERENCE_TEXTEXCERPT_ID),1,wx.EXPAND)
    mainSizer.Add(self.buildCommitButtonSizer(armid.DOCUMENTREFERENCE_BUTTONCOMMIT_ID,isCreate),0,wx.CENTER)
    self.SetSizer(mainSizer)

  def loadControls(self,objt,isReadOnly=False):
    self.theId = objt.id()
    nameCtrl = self.FindWindowById(armid.DOCUMENTREFERENCE_TEXTNAME_ID)
    docCtrl = self.FindWindowById(armid.DOCUMENTREFERENCE_COMBODOCNAME_ID)
    conCtrl = self.FindWindowById(armid.DOCUMENTREFERENCE_TEXTCONTRIBUTOR_ID)
    excCtrl = self.FindWindowById(armid.DOCUMENTREFERENCE_TEXTEXCERPT_ID)

    nameCtrl.SetValue(objt.name())
    docCtrl.SetValue(objt.document())
    conCtrl.SetValue(objt.contributor())
    excCtrl.SetValue(objt.excerpt())
